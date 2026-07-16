"""OpenAI-compatible LLM client (Groq now, OpenAI later via env).

All SDK calls go through this module — nowhere else.
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from openai import OpenAI

from app.config import get_settings

_SYSTEM_PROMPT_PATH = Path(__file__).resolve().parents[1] / "prompts" / "system.txt"


def load_system_prompt() -> str:
    return _SYSTEM_PROMPT_PATH.read_text(encoding="utf-8").strip()


@lru_cache
def get_llm_client() -> OpenAI:
    settings = get_settings()
    return OpenAI(
        api_key=settings.llm_api_key or "missing-key",
        base_url=settings.llm_base_url,
    )


def chat_completion(
    messages: list[dict[str, str]],
    *,
    max_tokens: int = 300,
    temperature: float = 0.2,
    model: str | None = None,
) -> str:
    settings = get_settings()
    client = get_llm_client()
    resp = client.chat.completions.create(
        model=model or settings.llm_model,
        messages=messages,
        max_tokens=max_tokens,
        temperature=temperature,
    )
    return (resp.choices[0].message.content or "").strip()
