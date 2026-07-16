"""Confirm persist_mood_event does not create unknown users."""

import os
import sys
from pathlib import Path

if Path("/app/app").is_dir():
    sys.path.insert(0, "/app")

from neo4j import GraphDatabase
from app.services.mood import MoodResult, persist_mood_event

d = GraphDatabase.driver(
    os.environ["NEO4J_URI"],
    auth=(os.environ["NEO4J_USER"], os.environ["NEO4J_PASSWORD"]),
)
mood = MoodResult(label="fear", confidence=0.9, insufficient_signal=False)
assert persist_mood_event(d, "wrong_user_zzz", mood) is None
assert persist_mood_event(d, "demo", mood) is not None
with d.session() as s:
    c = s.run(
        "MATCH (u:User {id: $id}) RETURN count(u) AS c",
        id="wrong_user_zzz",
    ).single()["c"]
assert c == 0, c
print("ok no orphan user created")
d.close()
