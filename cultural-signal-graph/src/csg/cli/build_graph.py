from __future__ import annotations

import argparse
from pathlib import Path

from csg.graph.build_reply_graph import build_reply_graph


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build reply graph artifacts from comments parquet.")
    parser.add_argument("--input", type=Path, default=Path("data/processed/comments.parquet"))
    parser.add_argument("--edges-output", type=Path, default=Path("data/processed/reply_edges.parquet"))
    parser.add_argument("--metrics-output", type=Path, default=Path("data/processed/thread_metrics.parquet"))
    return parser


def main() -> None:
    args = build_parser().parse_args()
    edges_output, metrics_output = build_reply_graph(
        args.input,
        args.edges_output,
        args.metrics_output,
    )
    print(f"Wrote reply edges parquet to {edges_output}")
    print(f"Wrote thread metrics parquet to {metrics_output}")


if __name__ == "__main__":
    main()

