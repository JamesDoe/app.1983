from __future__ import annotations

from collections.abc import Iterable
from datetime import timedelta
from pathlib import Path
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
from normalize import normalize_comment, to_utc_iso
from reddit_client import model_to_dict
from writers import DedupingJsonlWriter, JsonlWriter


def traverse_comment_tree(comments: Iterable[Any], depth: int = 1) -> list[tuple[Any, int]]:
    nodes: list[tuple[Any, int]] = []
    for comment in comments:
        nodes.append((comment, depth))
        replies = getattr(comment, "replies", [])
        if replies:
            nodes.extend(traverse_comment_tree(replies, depth + 1))
    return nodes


class CommentCollector:
    def __init__(self, reddit: Any, settings: CollectorSettings) -> None:
        self.reddit = reddit
        self.settings = settings

    def _metadata_key(self, thread_id: str, field: str) -> str:
        return f"thread:{thread_id}:{field}"

    def _thread_is_recent(self, thread_created_at: str, now: Any) -> bool:
        created_at = parse_utc_iso(thread_created_at)
        refresh_window = timedelta(hours=self.settings.comment_refresh_window_hours)
        return now - created_at <= refresh_window

    def _print_summary(self, **fields: str | int) -> None:
        print(
            "collect-comments summary:"
            + "".join(f" {key}={value}" for key, value in fields.items())
        )

    def _should_skip_thread(self, thread_id: str, state: Any, now: Any) -> bool:
        checkpoint_key = f"thread:{thread_id}"
        metadata = state.metadata
        thread_created_at = metadata.get(self._metadata_key(thread_id, "thread_created_at"))
        last_crawled_at = metadata.get(self._metadata_key(thread_id, "last_crawled_at"))

        if not thread_created_at and checkpoint_key in state.completed_keys:
            return False
        if not thread_created_at:
            return False
        if not self._thread_is_recent(str(thread_created_at), now):
            return checkpoint_key in state.completed_keys
        if not last_crawled_at:
            return False
        recrawl_interval = timedelta(minutes=self.settings.comment_recrawl_interval_minutes)
        return now - parse_utc_iso(str(last_crawled_at)) < recrawl_interval

    def collect_thread(self, thread_id: str, emit_summary: bool = True) -> dict[str, int]:
        ensure_data_dirs()
        raw_writer = JsonlWriter(RAW_DIR / "comments.jsonl")
        normalized_writer = DedupingJsonlWriter(NORMALIZED_DIR / "comments.jsonl", id_field="native_id")
        checkpoint = CheckpointStore(CHECKPOINT_DIR / "comments.json")
        state = checkpoint.load()
        checkpoint_key = f"thread:{thread_id}"
        now = utc_now()
        if self._should_skip_thread(thread_id, state, now):
            counts = {"raw": 0, "normalized": 0}
            if emit_summary:
                self._print_summary(
                    source="thread-id",
                    thread_id=thread_id,
                    skipped=1,
                    raw_records=0,
                    normalized_new_records=0,
                )
            return counts

        submission = self.reddit.submission(id=thread_id)
        submission.comment_sort = self.settings.comment_sort
        submission.comments.replace_more(limit=self.settings.replace_more_limit)
        subreddit_name = submission.subreddit.display_name
        thread_created_at = to_utc_iso(getattr(submission, "created_utc", None))
        raw_records: list[dict[str, Any]] = []
        normalized_records: list[dict[str, Any]] = []

        top_level_comments = list(submission.comments)
        for comment, depth in traverse_comment_tree(top_level_comments):
            raw_records.append(
                {
                    "record_type": "comment_raw",
                    "community": subreddit_name,
                    "thread_id": thread_id,
                    "native_id": comment.id,
                    "payload": model_to_dict(comment),
                }
            )
            normalized_records.append(normalize_comment(subreddit_name, thread_id, comment, depth))

        counts = {
            "raw": raw_writer.write_records(raw_records),
            "normalized": normalized_writer.write_records(normalized_records),
        }
        if thread_created_at is not None:
            state.metadata[self._metadata_key(thread_id, "thread_created_at")] = thread_created_at
        state.metadata[self._metadata_key(thread_id, "last_crawled_at")] = now.replace(microsecond=0).isoformat().replace(
            "+00:00", "Z"
        )
        if thread_created_at is not None and self._thread_is_recent(thread_created_at, now):
            state.completed_keys.discard(checkpoint_key)
        else:
            state.completed_keys.add(checkpoint_key)
        checkpoint.save(state)
        if emit_summary:
            self._print_summary(
                source="thread-id",
                thread_id=thread_id,
                skipped=0,
                raw_records=counts["raw"],
                normalized_new_records=counts["normalized"],
            )
        return counts

    def collect_from_file(self, path: Path) -> dict[str, int]:
        totals = {"raw": 0, "normalized": 0}
        threads_seen = 0
        threads_skipped = 0
        for line in path.read_text(encoding="utf-8").splitlines():
            thread_id = line.strip()
            if not thread_id:
                continue
            threads_seen += 1
            counts = self.collect_thread(thread_id, emit_summary=False)
            totals["raw"] += counts["raw"]
            totals["normalized"] += counts["normalized"]
            if counts["raw"] == 0 and counts["normalized"] == 0:
                threads_skipped += 1
        self._print_summary(
            source="input-file",
            input_file=path,
            thread_ids=threads_seen,
            skipped_threads=threads_skipped,
            raw_records=totals["raw"],
            normalized_new_records=totals["normalized"],
        )
        return totals
