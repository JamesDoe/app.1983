from __future__ import annotations

import polars as pl


def temporal_phrase_counts(
    phrases: pl.DataFrame,
    comment_phrase_edges: pl.DataFrame,
    comments: pl.DataFrame,
) -> pl.DataFrame:
    return (
        comment_phrase_edges.join(comments.select(["content_id", "created_at"]), left_on="comment_id", right_on="content_id")
        .join(phrases.select(["phrase_id", "phrase"]), on="phrase_id", how="left")
        .with_columns(pl.col("created_at").dt.truncate("1w").alias("week_start"))
        .group_by(["week_start", "phrase_id", "phrase"])
        .agg(pl.len().alias("usage_count"))
        .sort(["week_start", "usage_count", "phrase"], descending=[False, True, False])
    )
