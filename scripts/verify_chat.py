#!/usr/bin/env python3
"""Phase 6: POST /chat contract smoke test."""

from __future__ import annotations

import json
import os
import sys
import time
import urllib.error
import urllib.request
from uuid import uuid4


def post_chat(base: str, payload: dict) -> tuple[int, dict]:
    req = urllib.request.Request(
        f"{base}/chat",
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return resp.status, json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            data = {"detail": body}
        return e.code, data


def main() -> int:
    base = os.environ.get("API_BASE", "http://localhost:8000")
    session_id = str(uuid4())

    # grounded
    t0 = time.perf_counter()
    code, data = post_chat(
        base,
        {
            "user_id": "demo",
            "session_id": session_id,
            "message": "How many ADANIPOWER shares do I hold?",
        },
    )
    elapsed = time.perf_counter() - t0
    print(f"grounded status={code} elapsed={elapsed:.2f}s")
    print(json.dumps(data, indent=2)[:800])
    assert code == 200, data
    assert data["session_id"] == session_id
    assert "mood" in data and "answer" in data
    assert data["refused"] is False
    assert "ADANIPOWER" in data["answer"].upper() or "1661" in data["answer"]

    # refuse unknown ticker
    code2, data2 = post_chat(
        base,
        {
            "user_id": "demo",
            "session_id": session_id,
            "message": "How many NOTAREALTICKER shares do I hold?",
        },
    )
    print(f"refuse status={code2} refused={data2.get('refused')}")
    assert code2 == 200
    assert data2["refused"] is True

    # validation
    code3, _ = post_chat(base, {"user_id": "", "message": "hi"})
    assert code3 == 422
    print("ok validation 422")

    print(f"phase6 chat ok (grounded {elapsed:.2f}s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
