#!/usr/bin/env python3
"""POST 10 chat questions and log Q/A/response_time to Excel."""

from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request
from pathlib import Path
from uuid import uuid4

from openpyxl import Workbook

QUESTIONS = [
    "How many holdings do I have?",
    "How many Adani Power shares do I hold?",
    "What are my top performing stocks?",
    "What is the price of current Adani Power shares that I hold?",
    "How many stock holdings do I have?",
    "What is my total portfolio value?",
    "Which stock has the highest PnL?",
    "Do I hold any Reliance shares?",
    "What is my unrealized profit and loss?",
    "How many ADANIPOWER shares do I hold?",
]


def post_chat(base: str, payload: dict) -> tuple[str, float]:
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
            elapsed = time.perf_counter() - t0
            return data.get("answer") or "", elapsed
    except urllib.error.HTTPError as e:
        elapsed = time.perf_counter() - t0
        body = e.read().decode()
        try:
            data = json.loads(body)
            return data.get("detail") or body, elapsed
        except json.JSONDecodeError:
            return body, elapsed
    except Exception as e:
        elapsed = time.perf_counter() - t0
        return f"ERROR: {e}", elapsed


def main() -> int:
    base = os.environ.get("API_BASE", "http://localhost:8000")
    out = Path(__file__).resolve().parents[1] / "chat_qa_results.xlsx"
    session_id = str(uuid4())

    wb = Workbook()
    ws = wb.active
    ws.title = "Chat QA"
    ws.append(["Questions", "Answers", "Response time"])

    for i, question in enumerate(QUESTIONS, 1):
        answer, elapsed = post_chat(
            base,
            {"user_id": "demo", "session_id": session_id, "message": question},
        )
        # seconds, 2 decimals — easy to scan in Excel
        ws.append([question, answer, round(elapsed, 2)])
        print(f"[{i}/10] {elapsed:.2f}s | {question}")
        print(f"       -> {answer[:120]}")

    wb.save(out)
    print(f"\nWrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
