from __future__ import annotations

import argparse
from pathlib import Path

import polars as pl

from csg.extract.phrases import extract_phrase_tables


def run_phrase_extraction(input_path: Path, phrases_output: Path, edges_output: Path) -> tuple[Path, Path]:
    comments = pl.read_parquet(input_path)
    phrases, edges = extract_phrase_tables(comments)
    phrases_output.parent.mkdir(parents=True, exist_ok=True)
    edges_output.parent.mkdir(parents=True, exist_ok=True)
    phrases.write_parquet(phrases_output)
    edges.write_parquet(edges_output)
    return phrases_output, edges_output


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Extract noun-phrase signals from processed comment parquet.")
    parser.add_argument("--input", type=Path, default=Path("data/processed/comments.parquet"))
    parser.add_argument("--phrases-output", type=Path, default=Path("data/processed/phrases.parquet"))
    parser.add_argument(
        "--edges-output",
        type=Path,
        default=Path("data/processed/comment_phrase_edges.parquet"),
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    phrases_output, edges_output = run_phrase_extraction(
        args.input,
        args.phrases_output,
        args.edges_output,
    )
    print(f"Wrote phrases parquet to {phrases_output}")
    print(f"Wrote comment-phrase edges parquet to {edges_output}")


if __name__ == "__main__":
    main()
