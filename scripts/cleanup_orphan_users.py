#!/usr/bin/env python3
"""Delete User nodes that have no Portfolio (orphans from old chat MERGE)."""

from __future__ import annotations

import os
from neo4j import GraphDatabase


def main() -> int:
    driver = GraphDatabase.driver(
        os.environ.get("NEO4J_URI", "bolt://localhost:7687"),
        auth=(
            os.environ.get("NEO4J_USER", "neo4j"),
            os.environ.get("NEO4J_PASSWORD", "changeme-neo4j-password"),
        ),
    )
    try:
        with driver.session() as s:
            before = s.run(
                """
                MATCH (u:User)
                WHERE NOT (u)-[:OWNS]->(:Portfolio)
                RETURN count(u) AS c
                """
            ).single()["c"]
            s.run(
                """
                MATCH (u:User)
                WHERE NOT (u)-[:OWNS]->(:Portfolio)
                OPTIONAL MATCH (u)-[:HAD_MOOD]->(m:MoodEvent)
                DETACH DELETE m, u
                """
            )
            print(f"removed orphan users (no portfolio): {before}")
    finally:
        driver.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
