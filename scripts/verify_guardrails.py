#!/usr/bin/env python3
"""Phase 5: guardrails + optional live Groq smoke test."""

from __future__ import annotations

import os
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
_BACKEND = _REPO / "backend"
if Path("/app/app").is_dir():
    sys.path.insert(0, "/app")
elif _BACKEND.is_dir():
    sys.path.insert(0, str(_BACKEND))

from app.services.generate import generate_grounded_answer  # noqa: E402
from app.services.guardrails import REFUSE_NO_DATA, validate_answer  # noqa: E402


def main() -> int:
    ctx = {
        "found": True,
        "user_id": "demo",
        "matched_tickers": ["ADANIPOWER"],
        "holdings": [
            {
                "ticker": "ADANIPOWER",
                "quantity": 1661,
                "average_price": 103.482179,
                "stock_sector": "Utilities",
            }
        ],
        "citations": [{"type": "Holding", "ticker": "ADANIPOWER"}],
    }

    # Local guardrail checks
    bad = validate_answer("You hold TSLA and should buy more.", ctx)
    assert bad["answer"] == REFUSE_NO_DATA or "should" not in bad["answer"].lower()
    print("ok local guardrails")

    empty = generate_grounded_answer(
        question="How many RELIANCE?",
        context={"found": True, "holdings": [], "matched_tickers": []},
        needs_holding=True,
    )
    assert empty["refused"] and empty["answer"] == REFUSE_NO_DATA and not empty["used_llm"]
    print("ok empty retrieval skips LLM")

    key = os.environ.get("LLM_API_KEY", "")
    if not key or key.startswith("gsk-your"):
        print("skip live LLM (no LLM_API_KEY)")
        print("phase5 guardrails ok")
        return 0

    result = generate_grounded_answer(
        question="How many ADANIPOWER shares do I hold?",
        context=ctx,
        mood={"label": "fear", "confidence": 0.8, "insufficient_signal": False},
        needs_holding=True,
    )
    print(f"live LLM -> refused={result['refused']} used_llm={result['used_llm']}")
    print(f"answer: {result['answer']}")
    assert result["used_llm"]
    assert "ADANIPOWER" in result["answer"].upper() or result["refused"]
    print("phase5 llm+guardrails ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
