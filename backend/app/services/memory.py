"""Redis short-term conversation memory.

Key: chat:{user_id}:{session_id}
Value: JSON list of {role, content, ts}
"""

from __future__ import annotations

import json
import time
from typing import Any

DEFAULT_MAX_TURNS = 10
DEFAULT_TTL_SECONDS = 60 * 60 * 24  # 24h sliding


def memory_key(user_id: str, session_id: str) -> str:
    return f"chat:{user_id}:{session_id}"


def get_turns(redis, user_id: str, session_id: str) -> list[dict[str, Any]]:
    raw = redis.get(memory_key(user_id, session_id))
    if not raw:
        return []
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return []
    return data if isinstance(data, list) else []


def append_turn(
    redis,
    user_id: str,
    session_id: str,
    role: str,
    content: str,
    *,
    max_turns: int = DEFAULT_MAX_TURNS,
    ttl_seconds: int = DEFAULT_TTL_SECONDS,
) -> list[dict[str, Any]]:
    """Append one message, truncate to last max_turns, refresh TTL."""
    turns = get_turns(redis, user_id, session_id)
    turns.append({"role": role, "content": content, "ts": time.time()})
    if max_turns > 0 and len(turns) > max_turns:
        turns = turns[-max_turns:]
    key = memory_key(user_id, session_id)
    redis.set(key, json.dumps(turns), ex=ttl_seconds)
    return turns


def clear_session(redis, user_id: str, session_id: str) -> None:
    redis.delete(memory_key(user_id, session_id))
