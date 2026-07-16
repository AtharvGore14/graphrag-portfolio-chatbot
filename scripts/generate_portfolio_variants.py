"""One-shot: build backend/portfolios/{user_id}_portfolio.json variants."""

from __future__ import annotations

import copy
import json
from pathlib import Path

SRC = Path(__file__).resolve().parents[1] / "backend" / "portfolio_data (27).json"
OUT = Path(__file__).resolve().parents[1] / "backend" / "portfolios"

SKIP_KEYS = {
    "tradingsymbol",
    "exchange",
    "isin",
    "instrument_token",
    "product",
    "sector",
    "industry",
    "market_cap_category",
    "authorised_date",
    "collateral_type",
    "user_id",
}


def nudge(obj, delta):
    if isinstance(obj, dict):
        return {k: (v if k in SKIP_KEYS else nudge(v, delta)) for k, v in obj.items()}
    if isinstance(obj, list):
        return [nudge(x, delta) for x in obj]
    if isinstance(obj, bool):
        return obj
    if isinstance(obj, int):
        return obj + int(delta)
    if isinstance(obj, float):
        return obj + float(delta)
    return obj


def main() -> None:
    base = json.loads(SRC.read_text(encoding="utf-8"))
    OUT.mkdir(exist_ok=True)
    variants = [("demo", 0), ("u_alpha", 5), ("u_beta", -5)]
    for user_id, delta in variants:
        data = copy.deepcopy(base)
        if delta:
            data = nudge(data, delta)
        ordered = {"user_id": user_id}
        for k, v in data.items():
            if k != "user_id":
                ordered[k] = v
        path = OUT / f"{user_id}_portfolio.json"
        path.write_text(json.dumps(ordered, indent=2), encoding="utf-8")
        h = next(x for x in ordered["holdings"] if x["tradingsymbol"] == "ADANIPOWER")
        print(f"{path.name}: ADANIPOWER qty={h['quantity']}")


if __name__ == "__main__":
    main()
