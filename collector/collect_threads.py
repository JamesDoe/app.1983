from __future__ import annotations

from collections.abc import Iterable
from datetime import datetime, timedelta, timezone
from typing import Any

from checkpoints import CheckpointStore
from config import (
    CHECKPOINT_DIR,
    NORMALIZED_DIR,
    RAW_DIR,
    CollectorSettings,
    ensure_data_dirs,
    parse_utc_iso,
    utc_now,
)
from normalize import normalize_thread
from reddit_client import model_to_dict
from writers import DedupingJsonlWriter, JsonlWriter


def _listing_items(subreddit: Any, listing: str, limit: int) -> Iterable[Any]:
    if listing == "hot":
        return subreddit.hot(limit=limit)
    if listing == "new":
        return subreddit.new(limit=limit)
    if listing == "top_month":
        return subreddit.top(time_filter="month", limit=limit)
    raise ValueError(f"Unsupported listing: {listing}")


class ThreadCollector:
    def __init__(self, reddit: Any, settings: CollectorSettings) -> None:
        self.reddit = reddit
        self.settings = settings

    def collect(self, mode: str) -> dict[str, int]:
        ensure_data_dirs()
        raw_writer = JsonlWriter(RAW_DIR / "threads.jsonl")
        normalized_writer = DedupingJsonlWriter(NORMALIZED_DIR / "threads.jsonl", id_field="native_id")
        checkpoint = CheckpointStore(CHECKPOINT_DIR / f"threads_{mode}.json")
        state = checkpoint.load()
        if mode == "historical":
            return self._collect_historical(raw_writer, normalized_writer, checkpoint, state)
        listings = self.settings.pulse_listings if mode == "pulse" else self.settings.backfill_listings
        counts = {"raw": 0, "normalized": 0}
        use_checkpoints = mode == "backfill"
        batches_processed = 0
        batches_skipped = 0

        for subreddit_name in self.settings.subreddits:
            subreddit = self.reddit.subreddit(subreddit_name)
            for listing in listings:
                checkpoint_key = f"{mode}:{subreddit_name}:{listing}"
                if use_checkpoints and checkpoint_key in state.completed_keys:
                    batches_skipped += 1
                    continue
                raw_records: list[dict[str, Any]] = []
                normalized_records: list[dict[str, Any]] = []
                for submission in _listing_items(subreddit, listing, self.settings.thread_limit_per_listing):
                    raw_records.append(
                        {
                            "record_type": "thread_raw",
                            "community": subreddit_name,
                            "listing": listing,
                            "native_id": submission.id,
                            "payload": model_to_dict(submission),
                        }
                    )
                    normalized_records.append(normalize_thread(subreddit_name, submission))
                counts["raw"] += raw_writer.write_records(raw_records)
                counts["normalized"] += normalized_writer.write_records(normalized_records)
                batches_processed += 1
                if use_checkpoints:
                    state.completed_keys.add(checkpoint_key)
                    checkpoint.save(state)
        print(
            "collect-threads summary:"
            f" mode={mode}"
            f" subreddits={len(self.settings.subreddits)}"
            f" listings={','.join(listings)}"
            f" processed_batches={batches_processed}"
            f" skipped_batches={batches_skipped}"
            f" raw_records={counts['raw']}"
            f" normalized_new_records={counts['normalized']}"
        )
        return counts

    def _collect_historical(
        self,
        raw_writer: JsonlWriter,
        normalized_writer: DedupingJsonlWriter,
        checkpoint: CheckpointStore,
        state: Any,
    ) -> dict[str, int]:
        counts = {"raw": 0, "normalized": 0}
        windows_processed = 0
        windows_completed = 0
        stop_at = parse_utc_iso(self.settings.historical_stop_at)
        now = utc_now()
        metadata = state.metadata

        for subreddit_name in self.settings.subreddits:
            subreddit = self.reddit.subreddit(subreddit_name)
            cursor_key = f"historical:{subreddit_name}:next_end_at"
            next_end_at = parse_utc_iso(str(metadata.get(cursor_key, now.isoformat().replace("+00:00", "Z"))))
            remaining = self.settings.historical_windows_per_run
            while remaining > 0 and next_end_at > stop_at:
                window_days = self.settings.historical_window_days
                window_start_at = max(stop_at, next_end_at - timedelta(days=window_days))
                raw_records, normalized_records, split_count = self._collect_historical_window(
                    subreddit_name=subreddit_name,
                    subreddit=subreddit,
                    start_at=window_start_at,
                    end_at=next_end_at,
                )
                counts["raw"] += raw_writer.write_records(raw_records)
                counts["normalized"] += normalized_writer.write_records(normalized_records)
                windows_processed += split_count
                windows_completed += 1
                next_end_at = window_start_at
                metadata[cursor_key] = next_end_at.replace(microsecond=0).isoformat().replace("+00:00", "Z")
                checkpoint.save(state)
                remaining -= 1

        print(
            "collect-threads summary:"
            " mode=historical"
            f" subreddits={len(self.settings.subreddits)}"
            f" windows_completed={windows_completed}"
            f" search_batches={windows_processed}"
            f" raw_records={counts['raw']}"
            f" normalized_new_records={counts['normalized']}"
            f" stop_at={self.settings.historical_stop_at}"
        )
        return counts

    def _collect_historical_window(
        self,
        subreddit_name: str,
        subreddit: Any,
        start_at: datetime,
        end_at: datetime,
    ) -> tuple[list[dict[str, Any]], list[dict[str, Any]], int]:
        submissions = list(self._historical_search(subreddit, start_at, end_at))
        batch_count = 1
        window_days = max(1, int((end_at - start_at).total_seconds() // 86400))
        if (
            len(submissions) >= self.settings.thread_limit_per_listing
            and window_days > self.settings.historical_min_window_days
        ):
            midpoint = start_at + (end_at - start_at) / 2
            left_raw, left_normalized, left_batches = self._collect_historical_window(
                subreddit_name,
                subreddit,
                start_at,
                midpoint,
            )
            right_raw, right_normalized, right_batches = self._collect_historical_window(
                subreddit_name,
                subreddit,
                midpoint,
                end_at,
            )
            return (
                left_raw + right_raw,
                left_normalized + right_normalized,
                left_batches + right_batches,
            )

        raw_records: list[dict[str, Any]] = []
        normalized_records: list[dict[str, Any]] = []
        for submission in submissions:
            raw_records.append(
                {
                    "record_type": "thread_raw",
                    "community": subreddit_name,
                    "listing": "historical",
                    "window_start_at": start_at.replace(microsecond=0).isoformat().replace("+00:00", "Z"),
                    "window_end_at": end_at.replace(microsecond=0).isoformat().replace("+00:00", "Z"),
                    "native_id": submission.id,
                    "payload": model_to_dict(submission),
                }
            )
            normalized_records.append(normalize_thread(subreddit_name, submission))
        return raw_records, normalized_records, batch_count

    def _historical_search(
        self,
        subreddit: Any,
        start_at: datetime,
        end_at: datetime,
    ) -> Iterable[Any]:
        start_ts = int(start_at.replace(tzinfo=timezone.utc).timestamp())
        end_ts = int(end_at.replace(tzinfo=timezone.utc).timestamp())
        query = f"timestamp:{start_ts}..{end_ts}"
        return subreddit.search(
            query=query,
            sort="new",
            syntax="cloudsearch",
            time_filter="all",
            limit=self.settings.thread_limit_per_listing,
        )
