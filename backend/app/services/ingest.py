"""Idempotent portfolio JSON → Neo4j ingest."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from app.services.schema import ensure_schema

REQUIRED_TOP = ("metrics", "sectors", "holdings")


def resolve_user_id(data: dict[str, Any], override: str | None = None) -> str:
    """Prefer CLI override, else JSON user_id."""
    if override:
        return override.strip()
    uid = data.get("user_id")
    if isinstance(uid, str) and uid.strip():
        return uid.strip()
    raise ValueError("user_id missing: pass --user-id or set user_id in the JSON")


def load_portfolio_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("portfolio JSON must be an object")
    for key in REQUIRED_TOP:
        if key not in data:
            raise ValueError(f"missing top-level key: {key}")
    if not isinstance(data["holdings"], list) or not data["holdings"]:
        raise ValueError("holdings must be a non-empty list")
    for i, h in enumerate(data["holdings"]):
        if not h.get("tradingsymbol"):
            raise ValueError(f"holdings[{i}] missing tradingsymbol")
    return data


def _day_change_percent(h: dict[str, Any]) -> float | None:
    if "day_change_percent" in h:
        return h["day_change_percent"]
    if "day_change_percentage" in h:
        return h["day_change_percentage"]
    return None


def ingest_portfolio(driver, user_id: str, data: dict[str, Any]) -> dict[str, int]:
    """Upsert portfolio for user_id. Safe to re-run. Returns counts."""
    ensure_schema(driver)
    metrics = data["metrics"]
    sectors = data["sectors"]
    holdings = data["holdings"]

    with driver.session() as session:
        session.execute_write(_write_portfolio, user_id, metrics, sectors, holdings)

    return {
        "sectors": len(sectors),
        "holdings": len(holdings),
    }


def _write_portfolio(tx, user_id: str, metrics: dict, sectors: list, holdings: list) -> None:
    tx.run(
        """
        MERGE (u:User {id: $user_id})
        MERGE (u)-[:OWNS]->(p:Portfolio)
        SET p.total_investment = $m.total_investment,
            p.current_value = $m.current_value,
            p.profit_loss = $m.profit_loss,
            p.profit_loss_percent = $m.profit_loss_percent,
            p.total_stocks = $m.total_stocks,
            p.total_quantity = $m.total_quantity,
            p.weighted_avg_price = $m.weighted_avg_price,
            p.current_weighted_avg_ltp = $m.current_weighted_avg_ltp,
            p.sectors_count = $m.sectors_count,
            p.day_change = $m.day_change,
            p.day_change_percent = $m.day_change_percent,
            p.settled_quantity = $m.settled_quantity,
            p.t1_quantity = $m.t1_quantity,
            p.t1_percentage = $m.t1_percentage
        """,
        user_id=user_id,
        m=metrics,
    )

    # Replace sector rollups for this portfolio (idempotent)
    tx.run(
        """
        MATCH (u:User {id: $user_id})-[:OWNS]->(p:Portfolio)-[:HAS_SECTOR]->(sec:Sector)
        DETACH DELETE sec
        """,
        user_id=user_id,
    )
    for sec in sectors:
        tx.run(
            """
            MATCH (u:User {id: $user_id})-[:OWNS]->(p:Portfolio)
            CREATE (p)-[:HAS_SECTOR]->(s:Sector {
                name: $name,
                investment_value: $investment_value,
                current_value: $current_value,
                profit_loss: $profit_loss,
                profit_loss_percent: $profit_loss_percent,
                allocation: $allocation
            })
            """,
            user_id=user_id,
            name=sec["sector"],
            investment_value=sec.get("investment_value"),
            current_value=sec.get("current_value"),
            profit_loss=sec.get("profit_loss"),
            profit_loss_percent=sec.get("profit_loss_percent"),
            allocation=sec.get("allocation"),
        )

    # Replace holdings for this portfolio (idempotent); Stock nodes are MERGEd globally
    tx.run(
        """
        MATCH (u:User {id: $user_id})-[:OWNS]->(p:Portfolio)-[:HOLDS]->(h:Holding)
        DETACH DELETE h
        """,
        user_id=user_id,
    )
    for h in holdings:
        ticker = h["tradingsymbol"]
        tx.run(
            """
            MATCH (u:User {id: $user_id})-[:OWNS]->(p:Portfolio)
            MERGE (s:Stock {ticker: $ticker})
            SET s.exchange = $exchange,
                s.isin = $isin,
                s.instrument_token = $instrument_token,
                s.sector = $sector,
                s.industry = $industry,
                s.market_cap = $market_cap,
                s.market_cap_category = $market_cap_category
            CREATE (p)-[:HOLDS]->(holding:Holding {
                ticker: $ticker,
                quantity: $quantity,
                average_price: $average_price,
                last_price: $last_price,
                close_price: $close_price,
                investment_value: $investment_value,
                current_value: $current_value,
                pnl: $pnl,
                profit_loss_percent: $profit_loss_percent,
                day_change: $day_change,
                day_change_percent: $day_change_percent,
                t1_quantity: $t1_quantity,
                realised_quantity: $realised_quantity,
                product: $product
            })-[:OF]->(s)
            """,
            user_id=user_id,
            ticker=ticker,
            exchange=h.get("exchange"),
            isin=h.get("isin"),
            instrument_token=h.get("instrument_token"),
            sector=h.get("sector"),
            industry=h.get("industry"),
            market_cap=h.get("market_cap"),
            market_cap_category=h.get("market_cap_category"),
            quantity=h.get("quantity"),
            average_price=h.get("average_price"),
            last_price=h.get("last_price"),
            close_price=h.get("close_price"),
            investment_value=h.get("investment_value"),
            current_value=h.get("current_value"),
            pnl=h.get("pnl", h.get("profit_loss")),
            profit_loss_percent=h.get("profit_loss_percent"),
            day_change=h.get("day_change"),
            day_change_percent=_day_change_percent(h),
            t1_quantity=h.get("t1_quantity"),
            realised_quantity=h.get("realised_quantity"),
            product=h.get("product"),
        )


def verify_holding(driver, user_id: str, ticker: str) -> dict[str, Any] | None:
    with driver.session() as session:
        rec = session.run(
            """
            MATCH (u:User {id: $user_id})-[:OWNS]->(:Portfolio)-[:HOLDS]->(h:Holding)-[:OF]->(s:Stock {ticker: $ticker})
            RETURN h.quantity AS quantity, h.average_price AS average_price, s.sector AS sector
            """,
            user_id=user_id,
            ticker=ticker,
        ).single()
        return dict(rec) if rec else None
