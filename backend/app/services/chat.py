"""Chat turn orchestration: intent + fuzzy ticker + parallel mood/retrieve/memory."""

from __future__ import annotations

import asyncio
from typing import Any

from app.config import Settings
from app.models.schemas import ChatResponse, MoodPayload
from app.services.generate import generate_grounded_answer
from app.services.guardrails import MOOD_INSUFFICIENT, REFUSE_NO_DATA
from app.services.intent import clarify_message, detect_intent, resolve_ticker
from app.services.memory import append_turn, get_turns
from app.services.mood import MoodClassifier, MoodResult, persist_mood_event
from app.services.retrieve import list_tickers, retrieve_subgraph, user_has_portfolio


def _fmt_money(value: Any) -> str:
    try:
        n = float(value)
    except (TypeError, ValueError):
        return "—"
    return f"Rs.{n:,.2f}"


def _fmt_pct(value: Any) -> str:
    try:
        n = float(value)
    except (TypeError, ValueError):
        return "—"
    return f"{n:.2f}%"


def _fmt_qty(value: Any) -> str:
    try:
        n = float(value)
    except (TypeError, ValueError):
        return "—"
    if n == int(n):
        return str(int(n))
    return f"{n:g}"


def _template_answer(intent: str, context: dict[str, Any]) -> str | None:
    """Deterministic grounded answers for common intents (no LLM drift)."""
    metrics = context.get("portfolio_metrics") or {}
    holdings = context.get("holdings") or []

    if intent == "count_holdings" and metrics.get("total_stocks") is not None:
        n = metrics["total_stocks"]
        qty = _fmt_qty(metrics.get("total_quantity"))
        return (
            f"You currently hold {n} different stocks in this portfolio snapshot.\n"
            f"Across all of them, your total share quantity is {qty}.\n\n"
            'Tip: ask about a specific stock next, e.g. "How many ADANIPOWER shares do I hold?"'
        )

    if intent == "top_performers" and holdings:
        lines = [
            "Top holdings by profit so far (from your portfolio snapshot)",
            "",
            "How to read this:",
            "- Ticker = stock symbol on the exchange (short code for the company)",
            "- Profit = money gained or lost vs what you paid (also called P&L)",
            "- Return % = that profit as a percent of your investment",
            "- Shares = how many units you hold",
            "- Last price = latest price in the snapshot (not a live market quote)",
            "",
        ]
        for i, h in enumerate(holdings, 1):
            ticker = h.get("ticker") or "—"
            lines.append(f"{i}. {ticker}")
            lines.append(
                f"   Profit: {_fmt_money(h.get('pnl'))}  ({_fmt_pct(h.get('profit_loss_percent'))} return)"
            )
            lines.append(
                f"   Shares: {_fmt_qty(h.get('quantity'))}  |  "
                f"Last price: {_fmt_money(h.get('last_price'))}"
            )
            lines.append("")
        lines.append(
            'Want details on one of these? Ask e.g. "What is my ADANIPOWER holding?"'
        )
        return "\n".join(lines).rstrip() + "\n"

    if intent == "holding_lookup" and len(holdings) == 1:
        h = holdings[0]
        t = h.get("ticker")
        sector = h.get("stock_sector") or h.get("sector") or "—"
        return (
            f"Holding: {t}\n"
            f"- Shares you hold: {_fmt_qty(h.get('quantity'))}\n"
            f"- Average buy price: {_fmt_money(h.get('average_price'))}\n"
            f"- Last price (snapshot): {_fmt_money(h.get('last_price'))}\n"
            f"- Profit so far (P&L): {_fmt_money(h.get('pnl'))} "
            f"({_fmt_pct(h.get('profit_loss_percent'))} return)\n"
            f"- Sector: {sector}\n\n"
            "Note: prices come from your ingested snapshot, not a live market feed."
        )

    return None


async def run_chat_turn(
    *,
    user_id: str,
    message: str,
    session_id: str,
    driver,
    redis,
    mood_classifier: MoodClassifier,
    settings: Settings,
) -> ChatResponse:
    intent = detect_intent(message)

    async def _mood() -> MoodResult:
        return await asyncio.to_thread(
            mood_classifier.classify,
            message,
            settings.mood_confidence_threshold,
        )

    async def _history() -> list[dict[str, Any]]:
        return await asyncio.to_thread(get_turns, redis, user_id, session_id)

    async def _universe() -> tuple[bool, list[str]]:
        has = await asyncio.to_thread(user_has_portfolio, driver, user_id)
        tickers = await asyncio.to_thread(list_tickers, driver, user_id) if has else []
        return has, tickers

    try:
        mood, history, (has_portfolio, universe) = await asyncio.gather(
            _mood(), _history(), _universe()
        )
    except Exception as exc:
        raise RuntimeError(f"dependency_failure:{exc}") from exc

    resolve = resolve_ticker(message, universe) if has_portfolio else resolve_ticker(message, [])
    clarify = clarify_message(intent=intent, resolve=resolve, has_portfolio=has_portfolio)

    if clarify:
        answer = clarify
        citations: list[dict[str, Any]] = []
        refused = True
        # still persist mood + memory
        await _persist(redis, driver, user_id, session_id, message, answer, mood, settings)
        return ChatResponse(
            answer=answer,
            mood=MoodPayload(**mood.to_dict()),
            citations=citations,
            refused=refused,
            session_id=session_id,
        )

    ticker = resolve.ticker if intent == "holding_lookup" else None
    if intent == "holding_lookup" and resolve.status in ("exact", "fuzzy"):
        ticker = resolve.ticker

    try:
        context = await asyncio.to_thread(
            retrieve_subgraph,
            driver,
            user_id,
            ticker=ticker,
            intent=intent,
            include_sectors=intent in ("portfolio_overview", "count_holdings"),
            holdings_limit=15 if intent != "holding_lookup" else 5,
        )
    except Exception as exc:
        raise RuntimeError(f"dependency_failure:{exc}") from exc

    # Holding lookup that resolved but graph miss (shouldn't happen) → clarify
    if intent == "holding_lookup" and ticker and not context.get("holdings"):
        answer = (
            f"I matched “{ticker}” but couldn't load that holding. "
            "Want to ask another question?"
        )
        await _persist(redis, driver, user_id, session_id, message, answer, mood, settings)
        return ChatResponse(
            answer=answer,
            mood=MoodPayload(**mood.to_dict()),
            citations=[],
            refused=True,
            session_id=session_id,
        )

    templated = _template_answer(intent, context)
    if templated:
        gen = {
            "answer": templated,
            "refused": False,
            "issues": [],
            "used_llm": False,
        }
    else:
        needs_holding = intent == "holding_lookup"
        try:
            gen = await asyncio.to_thread(
                generate_grounded_answer,
                question=message,
                context=context,
                mood=mood.to_dict(),
                history=history,
                needs_holding=needs_holding,
                max_tokens=settings.llm_max_tokens,
            )
        except Exception as exc:
            if context.get("found") and context.get("holdings"):
                raise RuntimeError(f"llm_failure:{exc}") from exc
            gen = {
                "answer": REFUSE_NO_DATA
                + " Want to ask another question (e.g. holdings count or a ticker)?",
                "refused": True,
                "issues": [f"llm_failure:{exc}"],
                "used_llm": False,
            }

    answer = gen["answer"]
    if mood.insufficient_signal and MOOD_INSUFFICIENT.lower() not in answer.lower():
        pass

    citations = [] if gen["refused"] else list(context.get("citations") or [])
    await _persist(redis, driver, user_id, session_id, message, answer, mood, settings)

    return ChatResponse(
        answer=answer,
        mood=MoodPayload(**mood.to_dict()),
        citations=citations,
        refused=bool(gen["refused"]),
        session_id=session_id,
    )


async def _persist(redis, driver, user_id, session_id, message, answer, mood, settings) -> None:
    await asyncio.to_thread(
        append_turn,
        redis,
        user_id,
        session_id,
        "user",
        message,
        max_turns=settings.chat_memory_max_turns,
        ttl_seconds=settings.chat_memory_ttl_seconds,
    )
    await asyncio.to_thread(
        append_turn,
        redis,
        user_id,
        session_id,
        "assistant",
        answer,
        max_turns=settings.chat_memory_max_turns,
        ttl_seconds=settings.chat_memory_ttl_seconds,
    )
    await asyncio.to_thread(persist_mood_event, driver, user_id, mood)
