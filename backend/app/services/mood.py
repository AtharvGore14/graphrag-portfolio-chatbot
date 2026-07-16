"""Text-only mood via DistilRoBERTa emotion classifier.

LLM never invents mood — this module is the only source of labels.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass
from functools import lru_cache
from typing import Any

# j-hartmann/emotion-english-distilroberta-base
DEFAULT_MODEL = "j-hartmann/emotion-english-distilroberta-base"


@dataclass(frozen=True)
class MoodResult:
    label: str | None
    confidence: float
    insufficient_signal: bool

    def to_dict(self) -> dict[str, Any]:
        return {
            "label": self.label,
            "confidence": self.confidence,
            "insufficient_signal": self.insufficient_signal,
        }


def gate_mood(label: str, confidence: float, threshold: float) -> MoodResult:
    if confidence < threshold:
        return MoodResult(label=None, confidence=confidence, insufficient_signal=True)
    return MoodResult(label=label, confidence=confidence, insufficient_signal=False)


class MoodClassifier:
    def __init__(self, model_name: str = DEFAULT_MODEL):
        from transformers import pipeline

        self._pipe = pipeline(
            "text-classification",
            model=model_name,
            top_k=None,
            truncation=True,
        )

    def classify(self, text: str, threshold: float) -> MoodResult:
        text = (text or "").strip()
        if not text:
            return MoodResult(label=None, confidence=0.0, insufficient_signal=True)

        scores = self._pipe(text)[0]  # list of {label, score}
        best = max(scores, key=lambda x: x["score"])
        return gate_mood(best["label"], float(best["score"]), threshold)


@lru_cache
def get_mood_classifier(model_name: str = DEFAULT_MODEL) -> MoodClassifier:
    return MoodClassifier(model_name=model_name)


def classify_mood(
    text: str,
    threshold: float,
    *,
    classifier: MoodClassifier | None = None,
    model_name: str = DEFAULT_MODEL,
) -> MoodResult:
    clf = classifier or get_mood_classifier(model_name)
    return clf.classify(text, threshold)


def persist_mood_event(driver, user_id: str, mood: MoodResult) -> str | None:
    """Write MoodEvent only for users who already have an ingested portfolio.

    Never MERGE/CREATE a bare User — unknown user_ids must not pollute the graph.
    """
    if mood.insufficient_signal or not mood.label:
        return None
    event_id = str(uuid.uuid4())
    with driver.session() as session:
        rec = session.run(
            """
            MATCH (u:User {id: $user_id})-[:OWNS]->(:Portfolio)
            CREATE (u)-[:HAD_MOOD]->(m:MoodEvent {
                id: $event_id,
                label: $label,
                confidence: $confidence,
                timestamp: datetime()
            })
            RETURN m.id AS id
            """,
            user_id=user_id,
            event_id=event_id,
            label=mood.label,
            confidence=mood.confidence,
        ).single()
    return rec["id"] if rec else None
