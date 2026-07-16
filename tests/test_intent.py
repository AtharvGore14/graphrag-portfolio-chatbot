"""Intent + fuzzy ticker unit checks."""

import sys
from pathlib import Path

_root = Path("/app") if Path("/app/app").is_dir() else Path(__file__).resolve().parents[1] / "backend"
sys.path.insert(0, str(_root))

from app.services.intent import detect_intent, resolve_ticker


UNI = ["ADANIPOWER", "AJANTPHARM", "RELIANCE"]


def test_intents():
    assert detect_intent("How many holdings do I have?") == "count_holdings"
    assert detect_intent("How many stock holdings do I have?") == "count_holdings"
    assert detect_intent("What are my top performing stocks?") == "top_performers"
    assert detect_intent("How many Adani power shares do I hold?") == "holding_lookup"


def test_fuzzy_adani_power():
    r = resolve_ticker("What is the price of current Adani Power shares that I hold?", UNI)
    assert r.status in ("fuzzy", "exact") and r.ticker == "ADANIPOWER"
    r2 = resolve_ticker("How many Adani power shares do I hold?", UNI)
    assert r2.ticker == "ADANIPOWER"
    r3 = resolve_ticker("How many AdaniPower shares do I hold?", UNI)
    assert r3.ticker == "ADANIPOWER"


def test_no_false_have_ticker():
    r = resolve_ticker("How many holdings do I have?", UNI)
    assert r.ticker is None or r.ticker in UNI


if __name__ == "__main__":
    test_intents()
    test_fuzzy_adani_power()
    test_no_false_have_ticker()
    print("ok")
