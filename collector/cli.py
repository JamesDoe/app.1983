from __future__ import annotations

import argparse
from pathlib import Path

from collect_comments import CommentCollector
from collect_threads import ThreadCollector
from config import load_settings
from export_thread_ids import export_thread_ids
from reddit_client import build_reddit_client


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Reddit collectors MVP")
    subparsers = parser.add_subparsers(dest="command", required=True)

    collect_threads_parser = subparsers.add_parser("collect-threads", help="Collect thread listings")
    collect_threads_parser.add_argument("--mode", choices=("pulse", "backfill", "historical"), required=True)

    collect_comments_parser = subparsers.add_parser("collect-comments", help="Collect full comment trees")
    source_group = collect_comments_parser.add_mutually_exclusive_group(required=True)
    source_group.add_argument("--thread-id")
    source_group.add_argument("--input-file", type=Path)

    export_thread_ids_parser = subparsers.add_parser(
        "export-thread-ids",
        help="Export unique thread IDs from normalized threads JSONL",
    )
    export_thread_ids_parser.add_argument(
        "--output-file",
        type=Path,
        default=Path("thread_ids.txt"),
    )
    export_thread_ids_parser.add_argument(
        "--only-uncrawled-comments",
        action="store_true",
        help="Exclude thread IDs already completed by the comment collector",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "collect-threads":
        settings = load_settings()
        reddit = build_reddit_client()
        collector = ThreadCollector(reddit, settings)
        collector.collect(mode=args.mode)
        return 0

    if args.command == "collect-comments":
        settings = load_settings()
        reddit = build_reddit_client()
        collector = CommentCollector(reddit, settings)
        if args.thread_id:
            collector.collect_thread(args.thread_id)
            return 0
        if args.input_file:
            collector.collect_from_file(args.input_file)
            return 0

    if args.command == "export-thread-ids":
        export_thread_ids(
            output_path=args.output_file,
            only_uncrawled_comments=args.only_uncrawled_comments,
        )
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
