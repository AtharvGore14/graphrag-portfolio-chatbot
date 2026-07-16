"""Mood gate unit tests (no model download)."""

import sys
from pathlib import Path

_root = Path("/app") if Path("/app/app").is_dir() else Path(__file__).resolve().parents[1] / "backend"
sys.path.insert(0, str(_root))

from app.services.mood import gate_mood


def test_gate_below_threshold():
    r = gate_mood("fear", 0.4, 0.5)
    assert r.insufficient_signal and r.label is None


def test_gate_above_threshold():
    r = gate_mood("joy", 0.8, 0.5)
    assert not r.insufficient_signal and r.label == "joy"


if __name__ == "__main__":
    test_gate_below_threshold()
    test_gate_above_threshold()
    print("ok")
