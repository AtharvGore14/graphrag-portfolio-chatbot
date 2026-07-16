"""Intent detection + fuzzy ticker resolution against the user's holdings."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal

Intent = Literal[
    "count_holdings",
    "top_performers",
    "holding_lookup",
    "portfolio_overview",
    "unclear",
]

_WORD = re.compile(r"[A-Za-z]{2,}")

_STOP = {
    "how",
    "many",
    "much",
    "what",
    "whats",
    "which",
    "where",
    "when",
    "why",
    "do",
    "does",
    "did",
    "i",
    "my",
    "me",
    "the",
    "a",
    "an",
    "of",
    "in",
    "on",
    "to",
    "for",
    "is",
    "are",
    "was",
    "were",
    "be",
    "been",
    "have",
    "has",
    "had",
    "hold",
    "holds",
    "holding",
    "holdings",
    "share",
    "shares",
    "stock",
    "stocks",
    "sector",
    "sectors",
    "portfolio",
    "about",
    "please",
    "show",
    "list",
    "tell",
    "give",
    "avg",
    "average",
    "price",
    "prices",
    "value",
    "pnl",
    "profit",
    "loss",
    "allocation",
    "exposure",
    "overexposed",
    "amount",
    "current",
    "currently",
    "performing",
    "performance",
    "top",
    "best",
    "worst",
    "that",
    "this",
    "those",
    "these",
    "with",
    "from",
    "into",
    "only",
    "just",
    "also",
    "total",
    "number",
    "count",
    "qty",
    "quantity",
    "ltp",
    "last",
    "close",
    "cost",
    "bought",
    "owned",
    "own",
    "ones",
    "one",
    "all",
    "any",
    "some",
    "few",
    "more",
    "most",
    "can",
    "you",
    "your",
    "ask",
    "another",
    "question",
    "want",
}


@dataclass(frozen=True)
class TickerResolve:
    ticker: str | None
    candidates: list[str]
    status: Literal["exact", "fuzzy", "ambiguous", "none"]


def detect_intent(message: str) -> Intent:
    m = message.lower().strip()
    if re.search(
        r"(how many|number of|count of|total).*(holding|stock|position)|"
        r"(holding|stock|position).*(do i have|count|number)|"
        r"^how many (stock )?holdings",
        m,
    ):
        return "count_holdings"
    if re.search(
        r"top (perform|gainer|stock)|best (perform|stock)|"
        r"highest (pnl|profit|return)|worst (perform|stock)|"
        r"performing stock",
        m,
    ):
        return "top_performers"
    if re.search(
        r"\b(allocation|sector|portfolio value|total investment|"
        r"current value|overall|diversif)",
        m,
    ):
        return "portfolio_overview"
    # default toward holding lookup if any non-stop token looks company-like
    tokens = [t for t in _WORD.findall(m) if t not in _STOP]
    if tokens:
        return "holding_lookup"
    return "unclear"


def _collapse(s: str) -> str:
    return re.sub(r"[^A-Za-z0-9]", "", s).upper()


def resolve_ticker(message: str, universe: list[str]) -> TickerResolve:
    """Match user phrasing (e.g. 'Adani Power') to tickers the user actually holds."""
    if not universe:
        return TickerResolve(None, [], "none")

    uni = sorted({t.upper() for t in universe if t})
    uni_set = set(uni)
    collapsed_msg = _collapse(message)

    # 1) Exact token match (ADANIPOWER, AdaniPower)
    tokens = [_collapse(t) for t in _WORD.findall(message)]
    tokens = [t for t in tokens if t and t.lower() not in _STOP and len(t) >= 2]
    for t in tokens:
        if t in uni_set:
            return TickerResolve(t, [t], "exact")

    # 2) Collapsed multi-word: "Adani Power" → ADANIPOWER
    if collapsed_msg:
        for t in uni:
            if t in collapsed_msg or collapsed_msg in t:
                # avoid tiny accidental matches
                if len(t) >= 4 or t == collapsed_msg:
                    return TickerResolve(t, [t], "fuzzy")

    # 3) Token / bigram fuzzy against tickers
    scores: dict[str, int] = {}
    # also try joining adjacent non-stop tokens
    raw_tokens = [t for t in _WORD.findall(message.lower()) if t not in _STOP]
    phrases = list(raw_tokens)
    for i in range(len(raw_tokens) - 1):
        phrases.append(raw_tokens[i] + raw_tokens[i + 1])
    for i in range(len(raw_tokens) - 2):
        phrases.append(raw_tokens[i] + raw_tokens[i + 1] + raw_tokens[i + 2])

    for phrase in phrases:
        p = _collapse(phrase)
        if len(p) < 3:
            continue
        for t in uni:
            if p == t:
                scores[t] = max(scores.get(t, 0), 100)
            elif len(p) >= 4 and (t.startswith(p) or p.startswith(t)):
                scores[t] = max(scores.get(t, 0), 80)
            elif len(p) >= 4 and len(t) >= 4 and (p in t or t in p):
                scores[t] = max(scores.get(t, 0), 60)

    if not scores:
        return TickerResolve(None, [], "none")

    ranked = sorted(scores.items(), key=lambda kv: (-kv[1], kv[0]))
    best_score = ranked[0][1]
    top = [t for t, s in ranked if s == best_score]
    if len(top) == 1:
        return TickerResolve(top[0], top, "fuzzy")
    return TickerResolve(None, top[:8], "ambiguous")


def clarify_message(
    *,
    intent: Intent,
    resolve: TickerResolve,
    has_portfolio: bool,
) -> str | None:
    """Deterministic clarify / soft-refuse. None means proceed to retrieval+LLM."""
    if not has_portfolio:
        return (
            "I don't have a portfolio loaded for this user_id. "
            "Ingest a portfolio first, or try user_id `demo`. "
            "Want to ask another question with a different user_id?"
        )

    if intent == "unclear":
        return (
            "I wasn't sure what you meant. You can ask things like:\n"
            "- How many holdings do I have?\n"
            "- How many ADANIPOWER shares do I hold?\n"
            "- What are my top performing stocks?\n"
            "Want to try another question?"
        )

    if intent == "holding_lookup":
        if resolve.status == "ambiguous":
            opts = ", ".join(resolve.candidates)
            return (
                f"I found several matching holdings: {opts}. "
                "Which ticker did you mean? Or ask another question."
            )
        if resolve.status == "none":
            return (
                "I couldn't match that name to a holding in your portfolio. "
                "Try the exchange ticker (e.g. ADANIPOWER), or ask "
                "\"How many holdings do I have?\" / \"What are my top performing stocks?\". "
                "Want to ask another question?"
            )
    return None
