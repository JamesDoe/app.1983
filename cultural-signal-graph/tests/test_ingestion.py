import json
from pathlib import Path

from csg.cli.ingest import ingest
from csg.io.load_jsonl import load_jsonl, write_jsonl
from csg.models import CommentRecord


def test_valid_row(tmp_path: Path) -> None:
    source = tmp_path / "comments.jsonl"
    errors = tmp_path / "errors.jsonl"
    write_jsonl(
        source,
        [
            {
                "record_type": "comment",
                "community": "norfolk",
                "thread_id": "t1",
                "content_id": "c1",
                "author_id": "u1",
                "parent_id": "t3_t1",
                "depth": 1,
                "reply_count": 0,
                "created_at": "2026-03-13T23:03:07Z",
                "text": "hello",
                "score": 1,
            }
        ],
    )

    rows = load_jsonl(source, model=CommentRecord, errors_path=errors)
    assert len(rows) == 1
    record = rows[0]
    assert isinstance(record, CommentRecord)
    assert record.created_at.isoformat() == "2026-03-13T23:03:07+00:00"
    assert not errors.exists()


def test_missing_field_is_logged(tmp_path: Path) -> None:
    source = tmp_path / "comments.jsonl"
    errors = tmp_path / "errors.jsonl"
    write_jsonl(
        source,
        [
            {
                "record_type": "comment",
                "community": "norfolk",
                "thread_id": "t1",
                "content_id": "c1",
                "author_id": "u1",
                "parent_id": "t3_t1",
                "depth": 1,
                "reply_count": 0,
                "created_at": "2026-03-13T23:03:07Z",
                "score": 1,
            }
        ],
    )

    rows = load_jsonl(source, model=CommentRecord, errors_path=errors)
    assert rows == []
    logged = [json.loads(line) for line in errors.read_text(encoding="utf-8").splitlines()]
    assert logged[0]["error_type"] == "validation_error"


def test_malformed_json_is_logged(tmp_path: Path) -> None:
    source = tmp_path / "comments.jsonl"
    errors = tmp_path / "errors.jsonl"
    source.write_text('{"record_type": "comment"\n', encoding="utf-8")

    rows = load_jsonl(source, model=CommentRecord, errors_path=errors)
    assert rows == []
    logged = [json.loads(line) for line in errors.read_text(encoding="utf-8").splitlines()]
    assert logged[0]["error_type"] == "malformed_json"


def test_ingest_writes_parquet_outputs(tmp_path: Path) -> None:
    comments = tmp_path / "comments.jsonl"
    threads = tmp_path / "threads.jsonl"
    comments_output = tmp_path / "comments.parquet"
    threads_output = tmp_path / "threads.parquet"
    errors = tmp_path / "errors.jsonl"

    write_jsonl(
        comments,
        [
            {
                "record_type": "comment",
                "community": "norfolk",
                "thread_id": "t1",
                "content_id": "c1",
                "author_id": "u1",
                "parent_id": "t3_t1",
                "depth": 1,
                "reply_count": 0,
                "created_at": "2026-03-13T23:03:07Z",
                "text": "hello",
                "score": 1,
            }
        ],
    )
    write_jsonl(
        threads,
        [
            {
                "record_type": "thread",
                "community": "norfolk",
                "thread_id": "t1",
                "title": "Thread title",
                "created_at": "2026-03-13T20:00:00Z",
                "score": 2,
            }
        ],
    )

    ingest(comments, threads, comments_output, threads_output, errors)
    assert comments_output.exists()
    assert threads_output.exists()
