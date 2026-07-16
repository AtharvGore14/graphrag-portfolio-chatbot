"""Unit checks for Redis memory keying / truncate (no Redis required for key)."""

import sys
from pathlib import Path

_root = Path("/app") if Path("/app/app").is_dir() else Path(__file__).resolve().parents[1] / "backend"
sys.path.insert(0, str(_root))

from app.services.memory import memory_key


def test_memory_key():
    assert memory_key("demo", "abc") == "chat:demo:abc"


if __name__ == "__main__":
    test_memory_key()
    print("ok")
