"""Generate a grounded answer: one LLM call + guardrails (or refuse)."""

from __future__ import annotations

from typing import Any

from app.services.guardrails import (
    REFUSE_NO_DATA,
    build_user_prompt,
    should_refuse_facts,
    validate_answer,
)
from app.services.llm_client import chat_completion, load_system_prompt


def generate_grounded_answer(
    *,
    question: str,
    context: dict[str, Any],
    mood: dict[str, Any] | None = None,
    history: list[dict[str, Any]] | None = None,
    needs_holding: bool = False,
    max_tokens: int = 300,
) -> dict[str, Any]:
    """Returns {answer, refused, issues, used_llm}."""
    if should_refuse_facts(context, needs_holding=needs_holding):
        return {
            "answer": REFUSE_NO_DATA,
            "refused": True,
            "issues": ["empty_retrieval"],
            "used_llm": False,
        }

    messages = [
        {"role": "system", "content": load_system_prompt()},
        {
            "role": "user",
            "content": build_user_prompt(
                question=question,
                context=context,
                mood=mood,
                history=history,
            ),
        },
    ]
    draft = chat_completion(messages, max_tokens=max_tokens)
    checked = validate_answer(draft, context)
    if not checked["ok"]:
        # one stricter retry
        messages[0] = {
            "role": "system",
            "content": load_system_prompt()
            + "\n\nSTRICT MODE: previous draft failed grounding. Use only CONTEXT numbers/tickers.",
        }
        draft2 = chat_completion(messages, max_tokens=max_tokens, temperature=0.0)
        checked = validate_answer(draft2, context)
        if not checked["ok"]:
            return {
                "answer": REFUSE_NO_DATA,
                "refused": True,
                "issues": checked["issues"],
                "used_llm": True,
            }

    return {
        "answer": checked["answer"],
        "refused": False,
        "issues": checked["issues"],
        "used_llm": True,
    }
