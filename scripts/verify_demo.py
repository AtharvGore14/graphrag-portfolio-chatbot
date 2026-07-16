"""One-shot Cypher verify for Phase 1."""
import os
from neo4j import GraphDatabase

driver = GraphDatabase.driver(
    os.environ["NEO4J_URI"],
    auth=(os.environ["NEO4J_USER"], os.environ["NEO4J_PASSWORD"]),
)
with driver.session() as s:
    n = s.run(
        "MATCH (:User {id:'demo'})-[:OWNS]->(:Portfolio)-[:HOLDS]->(h:Holding) RETURN count(h) AS c"
    ).single()["c"]
    a = s.run(
        "MATCH (:User {id:'demo'})-[:OWNS]->(:Portfolio)-[:HOLDS]->(h:Holding {ticker:'ADANIPOWER'}) "
        "RETURN h.quantity AS q"
    ).single()["q"]
    print(f"holdings={n} ADANIPOWER_qty={a}")
driver.close()
