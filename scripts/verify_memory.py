#!/usr/bin/env python3
"""Phase 3: Redis short-term memory smoke test."""

from __future__ import annotations

import os
import sys
from pathlib import Path
from uuid import uuid4

_REPO = Path(__file__).resolve().parents[1]
_BACKEND = _REPO / "backend"
if Path("/app/app").is_dir():
    sys.path.insert(0, "/app")
elif _BACKEND.is_dir():
    sys.path.insert(0, str(_BACKEND))

from redis import Redis  # noqa: E402

from app.services.memory import append_turn, clear_session, get_turns, memory_key  # noqa: E402


def main() -> int:
    url = os.environ.get("REDIS_URL", "redis://localhost:6379/0")
    r = Redis.from_url(url, decode_responses=True)
    user_id = "demo"
    session_a = f"sess-{uuid4().hex[:8]}"
    session_b = f"sess-{uuid4().hex[:8]}"

    try:
        assert get_turns(r, user_id, session_a) == []

        append_turn(r, user_id, session_a, "user", "How many ADANIPOWER?")
        append_turn(r, user_id, session_a, "assistant", "You hold 1661 shares.")
        turns = get_turns(r, user_id, session_a)
        assert len(turns) == 2, turns
        assert turns[0]["role"] == "user" and "ADANIPOWER" in turns[0]["content"]
        assert turns[1]["role"] == "assistant"
        print(f"ok two turns persist key={memory_key(user_id, session_a)}")

        assert get_turns(r, user_id, session_b) == []
        print("ok new session_id is empty")

        # truncate: keep last 10 with max_turns=2 → only last 2 after 3 appends
        clear_session(r, user_id, session_a)
        append_turn(r, user_id, session_a, "user", "one", max_turns=2)
        append_turn(r, user_id, session_a, "user", "two", max_turns=2)
        append_turn(r, user_id, session_a, "user", "three", max_turns=2)
        turns = get_turns(r, user_id, session_a)
        assert [t["content"] for t in turns] == ["two", "three"], turns
        print("ok truncate to max_turns")

        # no cross-user leak
        other = get_turns(r, "u_alpha", session_a)
        assert other == []
        print("ok user_id isolation")

        clear_session(r, user_id, session_a)
        assert get_turns(r, user_id, session_a) == []
        print("ok clear_session")
    finally:
        clear_session(r, user_id, session_a)
        clear_session(r, user_id, session_b)
        r.close()

    print("phase3 memory ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
