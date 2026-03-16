from __future__ import annotations

import argparse
import math
from pathlib import Path

import polars as pl

from csg.analysis.cooccurrence import phrase_cooccurrence
from csg.analysis.debate import contested_phrases
from csg.analysis.frequency import phrase_frequency
from csg.analysis.trends import temporal_phrase_counts


def analyze(
    phrases_path: Path,
    edges_path: Path,
    reply_edges_path: Path,
    comments_path: Path,
    output_dir: Path,
) -> dict[str, Path]:
    phrases = pl.read_parquet(phrases_path)
    comment_phrase_edges = pl.read_parquet(edges_path)
    reply_edges = pl.read_parquet(reply_edges_path)
    comments = pl.read_parquet(comments_path)
    comment_depths = build_comment_depths(comments, reply_edges)

    output_dir.mkdir(parents=True, exist_ok=True)

    frequency = phrase_frequency(phrases)
    cooccurrence = phrase_cooccurrence(comment_phrase_edges, phrases)
    contested = contested_phrases(phrases, comment_phrase_edges, comment_depths, min_depth=6)
    temporal = temporal_phrase_counts(phrases, comment_phrase_edges, comments)
    top_signals = compute_signal_salience(phrases, comment_phrase_edges, comments, comment_depths)

    outputs = {
        "phrase_frequency": output_dir / "phrase_frequency.csv",
        "phrase_cooccurrence": output_dir / "phrase_cooccurrence.csv",
        "contested_phrases": output_dir / "contested_phrases.csv",
        "temporal_phrase_counts": output_dir / "temporal_phrase_counts.csv",
        "top_signals": output_dir / "top_signals.csv",
    }
    frequency.write_csv(outputs["phrase_frequency"])
    cooccurrence.write_csv(outputs["phrase_cooccurrence"])
    contested.write_csv(outputs["contested_phrases"])
    temporal.write_csv(outputs["temporal_phrase_counts"])
    top_signals.write_csv(outputs["top_signals"])
    return outputs


def compute_signal_salience(
    phrases: pl.DataFrame,
    comment_phrase_edges: pl.DataFrame,
    comments: pl.DataFrame,
    comment_depths: pl.DataFrame,
) -> pl.DataFrame:
    joined = (
        comment_phrase_edges.join(
            comments.select(["content_id", "score"]),
            left_on="comment_id",
            right_on="content_id",
            how="left",
        )
        .join(comment_depths, on="comment_id", how="left")
    )

    max_depth = 0
    if not comment_depths.is_empty():
        max_depth = int(comment_depths["verified_depth"].max())

    aggregated = (
        joined.group_by("phrase_id")
        .agg(
            pl.len().alias("phrase_frequency"),
            pl.sum("score").fill_null(0).alias("total_comment_score"),
            pl.mean("verified_depth").fill_null(0).alias("avg_reply_depth"),
        )
        .join(phrases.select(["phrase_id", "phrase"]), on="phrase_id", how="left")
    )

    rows = []
    for row in aggregated.iter_rows(named=True):
        normalized_reply_depth = (float(row["avg_reply_depth"]) / max_depth) if max_depth else 0.0
        total_comment_score = max(float(row["total_comment_score"]), 0.0)
        salience = (
            math.log1p(int(row["phrase_frequency"]))
            * math.log1p(total_comment_score)
            * (1.0 + normalized_reply_depth)
        )
        rows.append(
            {
                "phrase_id": row["phrase_id"],
                "phrase": row["phrase"],
                "phrase_frequency": int(row["phrase_frequency"]),
                "total_comment_score": total_comment_score,
                "normalized_reply_depth": normalized_reply_depth,
                "signal_salience": salience,
            }
        )

    return pl.DataFrame(
        rows,
        schema={
            "phrase_id": pl.Utf8,
            "phrase": pl.Utf8,
            "phrase_frequency": pl.Int64,
            "total_comment_score": pl.Float64,
            "normalized_reply_depth": pl.Float64,
            "signal_salience": pl.Float64,
        },
    ).sort(["signal_salience", "phrase"], descending=[True, False]) if rows else pl.DataFrame(
        schema={
            "phrase_id": pl.Utf8,
            "phrase": pl.Utf8,
            "phrase_frequency": pl.Int64,
            "total_comment_score": pl.Float64,
            "normalized_reply_depth": pl.Float64,
            "signal_salience": pl.Float64,
        }
    )


def build_comment_depths(comments: pl.DataFrame, reply_edges: pl.DataFrame) -> pl.DataFrame:
    comment_ids = comments.select(pl.col("content_id").cast(pl.Utf8).alias("comment_id")).unique()
    child_depths = reply_edges.select(
        pl.col("child_comment_id").cast(pl.Utf8).alias("comment_id"),
        pl.col("depth").cast(pl.Int64).alias("verified_depth"),
    )
    root_comments = comment_ids.join(child_depths, on="comment_id", how="anti").with_columns(
        pl.lit(1).cast(pl.Int64).alias("verified_depth")
    )
    return pl.concat([child_depths, root_comments]).unique(subset=["comment_id"]).sort("comment_id")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run cultural signal analyses from parquet artifacts.")
    parser.add_argument("--phrases", type=Path, default=Path("data/processed/phrases.parquet"))
    parser.add_argument(
        "--comment-phrase-edges",
        type=Path,
        default=Path("data/processed/comment_phrase_edges.parquet"),
    )
    parser.add_argument("--reply-edges", type=Path, default=Path("data/processed/reply_edges.parquet"))
    parser.add_argument("--comments", type=Path, default=Path("data/processed/comments.parquet"))
    parser.add_argument("--output-dir", type=Path, default=Path("artifacts"))
    return parser


def main() -> None:
    args = build_parser().parse_args()
    outputs = analyze(
        args.phrases,
        args.comment_phrase_edges,
        args.reply_edges,
        args.comments,
        args.output_dir,
    )
    for name, path in outputs.items():
        print(f"Wrote {name} to {path}")


if __name__ == "__main__":
    main()
