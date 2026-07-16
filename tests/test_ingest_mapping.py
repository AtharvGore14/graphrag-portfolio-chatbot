"""Minimal check: JSON load + day_change_percent alias."""

import sys
from pathlib import Path

_root = Path("/app") if Path("/app/app").is_dir() else Path(__file__).resolve().parents[1] / "backend"
sys.path.insert(0, str(_root))

from app.services.ingest import _day_change_percent, load_portfolio_json


def test_day_change_percent_aliases():
    assert _day_change_percent({"day_change_percent": 1.5}) == 1.5
    assert _day_change_percent({"day_change_percentage": 2.0}) == 2.0
    assert _day_change_percent({}) is None


def test_resolve_user_id_from_json():
    from app.services.ingest import resolve_user_id

    assert resolve_user_id({"user_id": "demo"}, None) == "demo"
    assert resolve_user_id({"user_id": "demo"}, "other") == "other"
    try:
        resolve_user_id({}, None)
        raise AssertionError("expected ValueError")
    except ValueError:
        pass


def test_load_demo_portfolio_has_user_id():
    path = _root / "portfolios" / "demo_portfolio.json"
    data = load_portfolio_json(path)
    assert data["user_id"] == "demo"
    assert data["metrics"]["total_stocks"] == 76
    adani = next(h for h in data["holdings"] if h["tradingsymbol"] == "ADANIPOWER")
    assert adani["quantity"] == 1661


if __name__ == "__main__":
    test_day_change_percent_aliases()
    test_resolve_user_id_from_json()
    test_load_demo_portfolio_has_user_id()
    print("ok")
