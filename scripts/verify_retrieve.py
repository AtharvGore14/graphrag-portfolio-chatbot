#!/usr/bin/env python3
"""Phase 2 check: multi-user retrieval isolation."""

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

from neo4j import GraphDatabase  # noqa: E402

from app.services.retrieve import (  # noqa: E402
    get_holding_by_ticker,
    retrieve_subgraph,
    user_exists,
)


def main() -> int:
    driver = GraphDatabase.driver(
        os.environ.get("NEO4J_URI", "bolt://localhost:7687"),
        auth=(
            os.environ.get("NEO4J_USER", "neo4j"),
            os.environ.get("NEO4J_PASSWORD", "changeme-neo4j-password"),
        ),
    )
    try:
        expected = {"demo": 1661, "u_alpha": 1666, "u_beta": 1656}
        for uid, qty in expected.items():
            assert user_exists(driver, uid), f"missing user {uid}"
            h = get_holding_by_ticker(driver, uid, "ADANIPOWER")
            assert h is not None, f"no holding for {uid}"
            assert h["quantity"] == qty, f"{uid}: got {h['quantity']} want {qty}"
            sub = retrieve_subgraph(driver, uid, ticker="ADANIPOWER")
            assert sub["found"] and sub["matched_tickers"] == ["ADANIPOWER"]
            assert sub["citations"], f"{uid}: empty citations"
            print(f"ok {uid}: ADANIPOWER qty={h['quantity']} citations={len(sub['citations'])}")

        assert not user_exists(driver, "nobody")
        empty = retrieve_subgraph(driver, "nobody", ticker="ADANIPOWER")
        assert empty["found"] is False and empty["holdings"] == []
        print("ok isolation: unknown user returns empty")
    finally:
        driver.close()
    print("phase2 retrieve ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
