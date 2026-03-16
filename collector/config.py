from __future__ import annotations

import json
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
NORMALIZED_DIR = DATA_DIR / "normalized"
CHECKPOINT_DIR = DATA_DIR / "checkpoints"
SETTINGS_PATH = BASE_DIR / "collector_settings.json"
ENV_PATH = BASE_DIR / ".env"


@dataclass(frozen=True)
class RedditCredentials:
    client_id: str
    client_secret: str
    user_agent: str


@dataclass(frozen=True)
class CollectorSettings:
    subreddits: list[str]
    thread_limit_per_listing: int
    pulse_listings: list[str]
    backfill_listings: list[str]
    historical_window_days: int
    historical_min_window_days: int
    historical_windows_per_run: int
    historical_stop_at: str
    comment_refresh_window_hours: int
    comment_recrawl_interval_minutes: int
    comment_sort: str
    replace_more_limit: int | None


def ensure_data_dirs() -> None:
    for directory in (RAW_DIR, NORMALIZED_DIR, CHECKPOINT_DIR):
        directory.mkdir(parents=True, exist_ok=True)


def load_dotenv(path: Path = ENV_PATH) -> None:
    if not path.exists():
        return
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()
        if value.startswith(("\"", "'")) and value.endswith(("\"", "'")) and len(value) >= 2:
            value = value[1:-1]
        os.environ.setdefault(key, value)


def load_settings(path: Path = SETTINGS_PATH) -> CollectorSettings:
    payload = json.loads(path.read_text(encoding="utf-8"))
    return CollectorSettings(
        subreddits=list(payload["subreddits"]),
        thread_limit_per_listing=int(payload["thread_limit_per_listing"]),
        pulse_listings=list(payload["pulse_listings"]),
        backfill_listings=list(payload["backfill_listings"]),
        historical_window_days=int(payload.get("historical_window_days", 30)),
        historical_min_window_days=int(payload.get("historical_min_window_days", 3)),
        historical_windows_per_run=int(payload.get("historical_windows_per_run", 1)),
        historical_stop_at=str(payload.get("historical_stop_at", "2008-01-01T00:00:00Z")),
        comment_refresh_window_hours=int(payload.get("comment_refresh_window_hours", 72)),
        comment_recrawl_interval_minutes=int(payload.get("comment_recrawl_interval_minutes", 60)),
        comment_sort=str(payload["comment_sort"]),
        replace_more_limit=payload["replace_more_limit"],
    )


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def parse_utc_iso(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc)


def load_reddit_credentials() -> RedditCredentials:
    load_dotenv()
    client_id = os.getenv("REDDIT_CLIENT_ID", "").strip()
    client_secret = os.getenv("REDDIT_CLIENT_SECRET", "").strip()
    user_agent = os.getenv("REDDIT_USER_AGENT", "reddit-collector-mvp/0.1").strip()
    missing = [
        name
        for name, value in (
            ("REDDIT_CLIENT_ID", client_id),
            ("REDDIT_CLIENT_SECRET", client_secret),
        )
        if not value
    ]
    if missing:
        joined = ", ".join(missing)
        raise RuntimeError(f"Missing Reddit credentials: {joined}")
    return RedditCredentials(
        client_id=client_id,
        client_secret=client_secret,
        user_agent=user_agent,
    )
