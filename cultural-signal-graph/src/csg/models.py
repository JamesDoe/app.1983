from __future__ import annotations

from datetime import datetime, timezone
from typing import Literal

from pydantic import BaseModel, field_validator


class ThreadRecord(BaseModel):
    record_type: Literal["thread"]
    community: str
    thread_id: str
    title: str
    created_at: datetime
    score: int

    @field_validator("created_at", mode="before")
    @classmethod
    def normalize_created_at(cls, value: object) -> datetime:
        return normalize_utc_datetime(value)


class CommentRecord(BaseModel):
    record_type: Literal["comment"]
    community: str
    thread_id: str
    content_id: str
    author_id: str
    parent_id: str
    depth: int
    reply_count: int
    created_at: datetime
    text: str
    score: int

    @field_validator("created_at", mode="before")
    @classmethod
    def normalize_created_at(cls, value: object) -> datetime:
        return normalize_utc_datetime(value)


def normalize_utc_datetime(value: object) -> datetime:
    if isinstance(value, datetime):
        dt_value = value
    elif isinstance(value, str):
        dt_value = datetime.fromisoformat(value.replace("Z", "+00:00"))
    else:
        raise TypeError("created_at must be a datetime or ISO 8601 string")

    if dt_value.tzinfo is None:
        dt_value = dt_value.replace(tzinfo=timezone.utc)
    else:
        dt_value = dt_value.astimezone(timezone.utc)
    return dt_value
