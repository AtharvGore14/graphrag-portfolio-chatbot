"""User-scoped Neo4j retrieval. Every query starts at (:User {id})."""

from __future__ import annotations

from typing import Any


def user_exists(driver, user_id: str) -> bool:
    with driver.session() as session:
        rec = session.run(
            "MATCH (u:User {id: $user_id}) RETURN u.id AS id LIMIT 1",
            user_id=user_id,
        ).single()
        return rec is not None


def get_portfolio_metrics(driver, user_id: str) -> dict[str, Any] | None:
    with driver.session() as session:
        rec = session.run(
            """
            MATCH (u:User {id: $user_id})-[:OWNS]->(p:Portfolio)
            RETURN p {.*} AS metrics
            """,
            user_id=user_id,
        ).single()
        return rec["metrics"] if rec else None


def get_sectors(driver, user_id: str) -> list[dict[str, Any]]:
    with driver.session() as session:
        result = session.run(
            """
            MATCH (u:User {id: $user_id})-[:OWNS]->(:Portfolio)-[:HAS_SECTOR]->(s:Sector)
            RETURN s {.*} AS sector
            ORDER BY s.allocation DESC
            """,
            user_id=user_id,
        )
        return [r["sector"] for r in result]


def get_holding_by_ticker(driver, user_id: str, ticker: str) -> dict[str, Any] | None:
    ticker = ticker.upper()
    with driver.session() as session:
        rec = session.run(
            """
            MATCH (u:User {id: $user_id})-[:OWNS]->(:Portfolio)-[:HOLDS]->(h:Holding)-[:OF]->(s:Stock)
            WHERE h.ticker = $ticker OR s.ticker = $ticker
            RETURN h {.*, stock_sector: s.sector, stock_industry: s.industry,
                      exchange: s.exchange, isin: s.isin} AS holding
            """,
            user_id=user_id,
            ticker=ticker,
        ).single()
        return rec["holding"] if rec else None


def list_holdings(driver, user_id: str, limit: int = 20) -> list[dict[str, Any]]:
    with driver.session() as session:
        result = session.run(
            """
            MATCH (u:User {id: $user_id})-[:OWNS]->(:Portfolio)-[:HOLDS]->(h:Holding)-[:OF]->(s:Stock)
            RETURN h {
              .ticker, .quantity, .average_price, .current_value, .pnl,
              .profit_loss_percent, sector: s.sector
            } AS holding
            ORDER BY h.current_value DESC
            LIMIT $limit
            """,
            user_id=user_id,
            limit=limit,
        )
        return [r["holding"] for r in result]


def user_has_portfolio(driver, user_id: str) -> bool:
    with driver.session() as session:
        rec = session.run(
            """
            MATCH (u:User {id: $user_id})-[:OWNS]->(:Portfolio)
            RETURN u.id AS id LIMIT 1
            """,
            user_id=user_id,
        ).single()
        return rec is not None


def list_tickers(driver, user_id: str) -> list[str]:
    with driver.session() as session:
        result = session.run(
            """
            MATCH (u:User {id: $user_id})-[:OWNS]->(:Portfolio)-[:HOLDS]->(h:Holding)
            RETURN h.ticker AS ticker
            ORDER BY h.ticker
            """,
            user_id=user_id,
        )
        return [r["ticker"] for r in result if r["ticker"]]


def top_holdings_by_pnl(driver, user_id: str, limit: int = 5) -> list[dict[str, Any]]:
    with driver.session() as session:
        result = session.run(
            """
            MATCH (u:User {id: $user_id})-[:OWNS]->(:Portfolio)-[:HOLDS]->(h:Holding)-[:OF]->(s:Stock)
            RETURN h {
              .ticker, .quantity, .average_price, .last_price, .current_value, .pnl,
              .profit_loss_percent, sector: s.sector
            } AS holding
            ORDER BY coalesce(h.pnl, 0) DESC
            LIMIT $limit
            """,
            user_id=user_id,
            limit=limit,
        )
        return [r["holding"] for r in result]


def retrieve_subgraph(
    driver,
    user_id: str,
    *,
    ticker: str | None = None,
    intent: str = "holding_lookup",
    include_sectors: bool = True,
    holdings_limit: int = 20,
) -> dict[str, Any]:
    """Minimal subgraph + citation candidates for a chat turn."""
    if not user_has_portfolio(driver, user_id):
        return {
            "user_id": user_id,
            "found": False,
            "intent": intent,
            "portfolio_metrics": None,
            "sectors": [],
            "holdings": [],
            "matched_tickers": [],
            "citations": [],
        }

    metrics = get_portfolio_metrics(driver, user_id)
    sectors = get_sectors(driver, user_id) if include_sectors else []
    citations: list[dict[str, Any]] = []

    if metrics:
        citations.append({"type": "Portfolio", "fields": list(metrics.keys())})

    for sec in sectors:
        citations.append(
            {
                "type": "Sector",
                "name": sec.get("name"),
                "fields": ["allocation", "current_value"],
            }
        )

    holdings: list[dict[str, Any]] = []
    matched: list[str] = []

    if intent == "count_holdings":
        # metrics.total_stocks is enough; optional sample holdings
        holdings = list_holdings(driver, user_id, limit=min(5, holdings_limit))
        matched = [h["ticker"] for h in holdings if h.get("ticker")]
    elif intent == "top_performers":
        holdings = top_holdings_by_pnl(driver, user_id, limit=min(5, holdings_limit))
        matched = [h["ticker"] for h in holdings if h.get("ticker")]
        for t in matched:
            citations.append(
                {"type": "Holding", "ticker": t, "fields": ["pnl", "profit_loss_percent", "quantity"]}
            )
    elif ticker:
        h = get_holding_by_ticker(driver, user_id, ticker)
        if h:
            holdings = [h]
            matched = [h.get("ticker") or ticker.upper()]
            citations.append(
                {
                    "type": "Holding",
                    "ticker": matched[0],
                    "fields": [
                        "quantity",
                        "average_price",
                        "last_price",
                        "pnl",
                    ],
                }
            )
            citations.append(
                {"type": "Stock", "ticker": matched[0], "fields": ["sector", "industry"]}
            )
    elif intent in ("portfolio_overview", "holding_lookup"):
        holdings = list_holdings(driver, user_id, limit=holdings_limit)
        matched = [h["ticker"] for h in holdings if h.get("ticker")]
        for t in matched[:5]:
            citations.append(
                {"type": "Holding", "ticker": t, "fields": ["quantity", "current_value"]}
            )

    return {
        "user_id": user_id,
        "found": True,
        "intent": intent,
        "portfolio_metrics": metrics,
        "sectors": sectors,
        "holdings": holdings,
        "matched_tickers": matched,
        "citations": citations,
    }
