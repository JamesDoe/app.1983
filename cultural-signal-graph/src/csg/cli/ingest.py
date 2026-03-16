from __future__ import annotations

import argparse
from pathlib import Path

import polars as pl

from csg.config import DEFAULT_CONFIG
from csg.io.load_jsonl import stream_jsonl
from csg.models import CommentRecord, ThreadRecord


def ingest(
    comments_path: Path,
    threads_path: Path,
    comments_output: Path,
    threads_output: Path,
    errors_path: Path,
) -> tuple[Path, Path]:
    comments = stream_jsonl(comments_path, model=CommentRecord, errors_path=errors_path)
    threads = stream_jsonl(threads_path, model=ThreadRecord, errors_path=errors_path)

    write_parquet(comments_output, comments, CommentRecord)
    write_parquet(threads_output, threads, ThreadRecord)
    return comments_output, threads_output


def write_parquet(output_path: Path, records, model_type: type[CommentRecord] | type[ThreadRecord]) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    rows = [record.model_dump(mode="python") for record in records]
    if rows:
        frame = pl.DataFrame(rows)
    else:
        schema = {name: pl.Utf8 for name in model_type.model_fields}
        schema["created_at"] = pl.Datetime(time_zone="UTC")
        if "score" in schema:
            schema["score"] = pl.Int64
        if "depth" in schema:
            schema["depth"] = pl.Int64
        if "reply_count" in schema:
            schema["reply_count"] = pl.Int64
        frame = pl.DataFrame(schema=schema)
    frame.write_parquet(output_path)
    return output_path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate raw JSONL inputs and write parquet outputs.")
    parser.add_argument("--comments", type=Path, default=Path("data/raw/comments.jsonl"))
    parser.add_argument("--threads", type=Path, default=Path("data/raw/threads.jsonl"))
    parser.add_argument("--comments-output", type=Path, default=Path("data/processed/comments.parquet"))
    parser.add_argument("--threads-output", type=Path, default=Path("data/processed/threads.parquet"))
    parser.add_argument("--errors", type=Path, default=Path("artifacts/errors.jsonl"))
    return parser


def main() -> None:
    DEFAULT_CONFIG.ensure_directories()
    args = build_parser().parse_args()
    comments_output, threads_output = ingest(
        args.comments,
        args.threads,
        args.comments_output,
        args.threads_output,
        args.errors,
    )
    print(f"Wrote comments parquet to {comments_output}")
    print(f"Wrote threads parquet to {threads_output}")


if __name__ == "__main__":
    main()
