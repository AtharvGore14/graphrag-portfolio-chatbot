from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field, field_validator


class ChatRequest(BaseModel):
    user_id: str = Field(..., min_length=1, max_length=128)
    message: str = Field(..., min_length=1, max_length=2000)
    session_id: str | None = Field(default=None, max_length=128)

    @field_validator("user_id", "message")
    @classmethod
    def strip_nonempty(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("must not be empty")
        return v

    def resolved_session_id(self) -> str:
        if self.session_id and self.session_id.strip():
            return self.session_id.strip()
        return str(uuid4())


class MoodPayload(BaseModel):
    label: str | None
    confidence: float
    insufficient_signal: bool


class ChatResponse(BaseModel):
    answer: str
    mood: MoodPayload
    citations: list[dict[str, Any]]
    refused: bool
    session_id: str
