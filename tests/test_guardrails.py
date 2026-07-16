"""Guardrail unit tests (no LLM)."""

import sys
from pathlib import Path

_root = Path("/app") if Path("/app/app").is_dir() else Path(__file__).resolve().parents[1] / "backend"
sys.path.insert(0, str(_root))

from app.services.guardrails import (
    REFUSE_NO_DATA,
    contains_advice,
    find_ungrounded_tickers,
    should_refuse_facts,
    strip_advice_sentences,
    validate_answer,
)


def test_advice_detect_and_strip():
    assert contains_advice("You should buy more ADANIPOWER.")
    cleaned = strip_advice_sentences(
        "You hold 1661 shares. You should buy more. Sector is Utilities."
    )
    assert "should" not in cleaned.lower()
    assert "1661" in cleaned


def test_ungrounded_ticker_blocked():
    ctx = {
        "found": True,
        "matched_tickers": ["ADANIPOWER"],
        "holdings": [{"ticker": "ADANIPOWER", "quantity": 1661}],
    }
    bad = find_ungrounded_tickers("You also hold RELIANCE.", ctx)
    assert "RELIANCE" in bad
    result = validate_answer("You hold RELIANCE.", ctx)
    assert result["ok"] is False
    assert result["answer"] == REFUSE_NO_DATA


def test_grounded_ticker_ok():
    ctx = {
        "found": True,
        "matched_tickers": ["ADANIPOWER"],
        "holdings": [{"ticker": "ADANIPOWER", "quantity": 1661, "average_price": 103.48}],
    }
    result = validate_answer("You hold 1661 shares of ADANIPOWER.", ctx)
    assert result["ok"] is True


def test_empty_retrieval_refuse():
    assert should_refuse_facts({"found": False}, needs_holding=True)
    assert should_refuse_facts({"found": True, "holdings": []}, needs_holding=True)


if __name__ == "__main__":
    test_advice_detect_and_strip()
    test_ungrounded_ticker_blocked()
    test_grounded_ticker_ok()
    test_empty_retrieval_refuse()
    print("ok")
