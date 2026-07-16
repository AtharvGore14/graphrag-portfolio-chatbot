#!/usr/bin/env python3
"""Phase 8: user-reported question forms + latency smoke."""

from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request
from uuid import uuid4


def post_chat(base: str, payload: dict) -> tuple[int, dict, float]:
    req = urllib.request.Request(
        f"{base}/chat",
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    t0 = time.perf_counter()
    try:
        with urllib.request.urlopen(req, timeout=90) as resp:
            data = json.loads(resp.read().decode())
            return resp.status, data, time.perf_counter() - t0
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            data = {"detail": body}
        return e.code, data, time.perf_counter() - t0


CASES = [
    ("How many holdings do I have?", False, "76"),
    ("How many stock holdings do I have?", False, "76"),
    ("What are my top performing stocks?", False, None),
    ("What is the price of current Adani Power shares that I hold?", False, "ADANIPOWER"),
    ("How many Adani power shares do I hold?", False, "1661"),
    ("How many AdaniPower shares do I hold?", False, "1661"),
    ("How many NOTAREALTICKER shares do I hold?", True, None),
]


def main() -> int:
    base = os.environ.get("API_BASE", "http://localhost:8000")
    session_id = str(uuid4())
    failed = 0

    for msg, expect_refuse, needle in CASES:
        code, data, elapsed = post_chat(
            base,
            {"user_id": "demo", "session_id": session_id, "message": msg},
        )
        ok = code == 200 and bool(data.get("refused")) == expect_refuse
        if ok and needle and not expect_refuse:
            blob = (data.get("answer") or "").upper()
            ok = needle.upper() in blob
        status = "ok" if ok else "FAIL"
        if not ok:
            failed += 1
        print(f"{status} [{elapsed:.2f}s] refuse={data.get('refused')} | {msg}")
        print(f"   -> {(data.get('answer') or '')[:160]}")

    # unknown user soft refuse
    code, data, _ = post_chat(
        base,
        {"user_id": "no_such_user_xyz", "session_id": str(uuid4()), "message": "How many holdings?"},
    )
    if code == 200 and data.get("refused"):
        print("ok unknown user refuses with guidance")
    else:
        print("FAIL unknown user", data)
        failed += 1

    if failed:
        print(f"phase8 FAILED ({failed})")
        return 1
    print("phase8 question-forms ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
