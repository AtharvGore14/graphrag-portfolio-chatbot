#!/usr/bin/env python3
"""Load portfolio JSON into Neo4j. Idempotent.

user_id comes from the JSON `user_id` field, or --user-id override.

Examples:
  docker compose exec api python /scripts/ingest_portfolio.py --file /app/portfolios/demo_portfolio.json
  docker compose exec api python /scripts/ingest_portfolio.py --all
"""

from __future__ import annotations

import argparse
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

from app.services.ingest import (  # noqa: E402
    ingest_portfolio,
    load_portfolio_json,
    resolve_user_id,
    verify_holding,
)

PORTFOLIOS_DIR = Path("/app/portfolios") if Path("/app/portfolios").is_dir() else _BACKEND / "portfolios"


def _driver():
    uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    user = os.getenv("NEO4J_USER", "neo4j")
    password = os.getenv("NEO4J_PASSWORD", "changeme-neo4j-password")
    return GraphDatabase.driver(uri, auth=(user, password))


def ingest_one(driver, path: Path, user_override: str | None, verify_ticker: str) -> int:
    data = load_portfolio_json(path)
    user_id = resolve_user_id(data, user_override)
    counts = ingest_portfolio(driver, user_id, data)
    check = verify_holding(driver, user_id, verify_ticker)
    print(
        f"ingested user_id={user_id} file={path.name} "
        f"sectors={counts['sectors']} holdings={counts['holdings']}"
    )
    if check:
        print(
            f"  verify {verify_ticker}: quantity={check['quantity']} "
            f"avg={check['average_price']} sector={check['sector']}"
        )
        return 0
    print(f"  verify {verify_ticker}: NOT FOUND", file=sys.stderr)
    return 2


def main() -> int:
    parser = argparse.ArgumentParser(description="Ingest portfolio JSON into Neo4j")
    parser.add_argument("--user-id", default=None, help="Override JSON user_id")
    parser.add_argument("--file", type=Path, default=None, help="Single portfolio JSON")
    parser.add_argument(
        "--all",
        action="store_true",
        help=f"Ingest every *_portfolio.json in {PORTFOLIOS_DIR}",
    )
    parser.add_argument("--verify-ticker", default="ADANIPOWER")
    args = parser.parse_args()

    if args.all:
        files = sorted(PORTFOLIOS_DIR.glob("*_portfolio.json"))
        if not files:
            print(f"error: no *_portfolio.json in {PORTFOLIOS_DIR}", file=sys.stderr)
            return 1
    elif args.file:
        files = [args.file]
    else:
        default = PORTFOLIOS_DIR / "demo_portfolio.json"
        if not default.is_file():
            print("error: pass --file, --all, or add demo_portfolio.json", file=sys.stderr)
            return 1
        files = [default]

    driver = _driver()
    code = 0
    try:
        for path in files:
            if not path.is_file():
                print(f"error: file not found: {path}", file=sys.stderr)
                return 1
            rc = ingest_one(driver, path, args.user_id, args.verify_ticker)
            code = code or rc
    finally:
        driver.close()
    return code


if __name__ == "__main__":
    raise SystemExit(main())
