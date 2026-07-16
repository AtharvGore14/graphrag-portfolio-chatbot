#!/usr/bin/env python3
"""Phase 4: mood classifier smoke test."""

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

from app.services.mood import (  # noqa: E402
    classify_mood,
    gate_mood,
    get_mood_classifier,
    persist_mood_event,
)


def main() -> int:
    threshold = float(os.environ.get("MOOD_CONFIDENCE_THRESHOLD", "0.5"))
    model = os.environ.get(
        "MOOD_MODEL", "j-hartmann/emotion-english-distilroberta-base"
    )

    # Pure gate unit
    low = gate_mood("fear", 0.2, threshold)
    assert low.insufficient_signal and low.label is None
    high = gate_mood("fear", 0.9, threshold)
    assert not high.insufficient_signal and high.label == "fear"
    print("ok gate_mood")

    print(f"loading model {model} …")
    clf = get_mood_classifier(model)

    stressed = classify_mood(
        "I have no idea what's happening with my portfolio and it's stressing me out",
        threshold,
        classifier=clf,
    )
    print(f"stressed -> {stressed.to_dict()}")
    assert not stressed.insufficient_signal, stressed
    assert stressed.label in {
        "anger",
        "disgust",
        "fear",
        "joy",
        "neutral",
        "sadness",
        "surprise",
    }, stressed.label

    empty = classify_mood("   ", threshold, classifier=clf)
    assert empty.insufficient_signal
    print("ok empty text -> insufficient_signal")

    # Persist when confident
    uri = os.environ.get("NEO4J_URI", "bolt://localhost:7687")
    user = os.environ.get("NEO4J_USER", "neo4j")
    password = os.environ.get("NEO4J_PASSWORD", "changeme-neo4j-password")
    driver = GraphDatabase.driver(uri, auth=(user, password))
    try:
        eid = persist_mood_event(driver, "demo", stressed)
        assert eid
        with driver.session() as s:
            n = s.run(
                """
                MATCH (:User {id:'demo'})-[:HAD_MOOD]->(m:MoodEvent {id: $id})
                RETURN m.label AS label
                """,
                id=eid,
            ).single()
        assert n["label"] == stressed.label
        print(f"ok MoodEvent persisted id={eid} label={stressed.label}")
    finally:
        driver.close()

    print("phase4 mood ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
