"""Anti-hallucination and analyser-not-suggester guardrails."""

from __future__ import annotations

import re
from typing import Any

REFUSE_NO_DATA = "I don't have that data in your portfolio graph."
MOOD_INSUFFICIENT = "Not enough signal to read your mood right now."

# Advisory / speculative phrases to block or strip
_ADVICE_PATTERNS = [
    re.compile(p, re.IGNORECASE)
    for p in [
        r"\byou should\b",
        r"\bi recommend\b",
        r"\bi suggest\b",
        r"\bconsider (buying|selling|holding)\b",
        r"\bbuy more\b",
        r"\bsell (now|off|your)\b",
        r"\bwill (likely |probably )?(go up|rise|fall|drop)\b",
        r"\bguaranteed\b",
        r"\bmust buy\b",
        r"\bmust sell\b",
        r"\bfinancial advice\b",
    ]
]

# Ticker-like tokens (NSE-style). Avoid matching common short words via allowlist skip.
_TICKER_RE = re.compile(r"\b([A-Z]{2,15}(?:-[A-Z]{1,5})?)\b")
_SKIP_WORDS = {
    "I",
    "A",
    "THE",
    "AND",
    "OR",
    "OF",
    "IN",
    "ON",
    "TO",
    "FOR",
    "IS",
    "IT",
    "AS",
    "AT",
    "BY",
    "BE",
    "AN",
    "IF",
    "NO",
    "NOT",
    "YOU",
    "YOUR",
    "HOLD",
    "HOLDS",
    "HELD",
    "SHARES",
    "SHARE",
    "STOCK",
    "STOCKS",
    "SECTOR",
    "PORTFOLIO",
    "PNL",
    "AVG",
    "AVERAGE",
    "PRICE",
    "QTY",
    "QUANTITY",
    "VALUE",
    "CURRENT",
    "TOTAL",
    "DATA",
    "GRAPH",
    "CONTEXT",
    "MOOD",
    "NSE",
    "BSE",
    "INR",
    "USD",
    "CNC",
    "OK",
    "YES",
    "LLM",
}

_NUMBER_RE = re.compile(r"(?<![A-Za-z])-?\d+(?:\.\d+)?")


def contains_advice(text: str) -> bool:
    return any(p.search(text) for p in _ADVICE_PATTERNS)


def strip_advice_sentences(text: str) -> str:
    """Drop sentences that look advisory; keep the rest."""
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    kept = [p for p in parts if p and not contains_advice(p)]
    return " ".join(kept).strip()


def allowed_tickers_from_context(context: dict[str, Any]) -> set[str]:
    tickers: set[str] = set()
    for t in context.get("matched_tickers") or []:
        if t:
            tickers.add(str(t).upper())
    for h in context.get("holdings") or []:
        t = h.get("ticker")
        if t:
            tickers.add(str(t).upper())
    return tickers


def _context_blob(context: dict[str, Any]) -> str:
    """Flatten retrieved facts for number membership checks."""
    return repr(context)


def extract_tickers(text: str) -> set[str]:
    found = set()
    for m in _TICKER_RE.finditer(text.upper()):
        tok = m.group(1)
        if tok in _SKIP_WORDS:
            continue
        found.add(tok)
    return found


def find_ungrounded_tickers(answer: str, context: dict[str, Any]) -> set[str]:
    allowed = allowed_tickers_from_context(context)
    if not allowed:
        # No holdings in context → any ticker claim is ungrounded
        return extract_tickers(answer)
    return extract_tickers(answer) - allowed


def find_ungrounded_numbers(answer: str, context: dict[str, Any]) -> list[str]:
    """Flag numbers in the answer that never appear in the retrieved context blob.

    Soft check: ignores tiny integers 0-9 that often appear in prose.
    """
    blob = _context_blob(context)
    bad: list[str] = []
    for m in _NUMBER_RE.finditer(answer):
        raw = m.group(0)
        try:
            val = float(raw)
        except ValueError:
            continue
        if abs(val) < 10 and raw.isdigit():
            continue
        # accept if exact token or common rounding forms appear in context
        if raw in blob:
            continue
        # try without trailing zeros / as int
        if raw.endswith(".0") and raw[:-2] in blob:
            continue
        try:
            if str(int(val)) in blob and val == int(val):
                continue
        except (ValueError, OverflowError):
            pass
        bad.append(raw)
    return bad


def validate_answer(answer: str, context: dict[str, Any]) -> dict[str, Any]:
    """Return {ok, answer, issues} after advice + grounding checks."""
    issues: list[str] = []
    text = answer.strip()

    if contains_advice(text):
        text = strip_advice_sentences(text)
        if contains_advice(text) or not text:
            issues.append("advice_language")
            text = REFUSE_NO_DATA if not text else text

    bad_tickers = find_ungrounded_tickers(text, context)
    if bad_tickers:
        issues.append(f"ungrounded_tickers:{sorted(bad_tickers)}")

    bad_nums = find_ungrounded_numbers(text, context)
    if bad_nums:
        issues.append(f"ungrounded_numbers:{bad_nums}")

    ok = not any(i.startswith("ungrounded_") for i in issues) and "advice_language" not in issues
    if not ok and bad_tickers:
        # Hard fail on invented tickers — do not ship the draft
        return {"ok": False, "answer": REFUSE_NO_DATA, "issues": issues}

    return {"ok": ok or (not bad_tickers and "advice_language" not in issues), "answer": text, "issues": issues}


def should_refuse_facts(context: dict[str, Any], *, needs_holding: bool) -> bool:
    """True when we must not call the LLM for portfolio facts."""
    if not context.get("found"):
        return True
    intent = context.get("intent")
    if intent == "count_holdings":
        return (context.get("portfolio_metrics") or {}).get("total_stocks") is None
    if intent == "top_performers":
        return not context.get("holdings")
    if needs_holding and not context.get("holdings"):
        return True
    return False


def build_user_prompt(
    *,
    question: str,
    context: dict[str, Any],
    mood: dict[str, Any] | None,
    history: list[dict[str, Any]] | None = None,
) -> str:
    parts: list[str] = []
    if history:
        hist_lines = [f"{t.get('role')}: {t.get('content')}" for t in history[-6:]]
        parts.append("RECENT_TURNS:\n" + "\n".join(hist_lines))
    parts.append(f"CONTEXT:\n{context}")
    if mood is not None:
        parts.append(f"MOOD:\n{mood}")
    parts.append(f"QUESTION:\n{question}")
    return "\n\n".join(parts)
