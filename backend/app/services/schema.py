"""Neo4j constraints and indexes (idempotent)."""

CONSTRAINTS = [
    "CREATE CONSTRAINT user_id IF NOT EXISTS FOR (u:User) REQUIRE u.id IS UNIQUE",
    "CREATE CONSTRAINT stock_ticker IF NOT EXISTS FOR (s:Stock) REQUIRE s.ticker IS UNIQUE",
    "CREATE INDEX stock_isin IF NOT EXISTS FOR (s:Stock) ON (s.isin)",
    "CREATE INDEX mood_ts IF NOT EXISTS FOR (m:MoodEvent) ON (m.timestamp)",
    "CREATE INDEX holding_ticker IF NOT EXISTS FOR (h:Holding) ON (h.ticker)",
]


def ensure_schema(driver) -> None:
    with driver.session() as session:
        for stmt in CONSTRAINTS:
            session.run(stmt)
