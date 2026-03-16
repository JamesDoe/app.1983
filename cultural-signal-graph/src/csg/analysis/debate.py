from __future__ import annotations

import polars as pl


def contested_phrases(
    phrases: pl.DataFrame,
    comment_phrase_edges: pl.DataFrame,
    comment_depths: pl.DataFrame,
    min_depth: int = 6,
) -> pl.DataFrame:
    deep_comments = comment_depths.filter(pl.col("verified_depth") > min_depth - 1).select(
        ["comment_id", "verified_depth"]
    )
    if deep_comments.is_empty():
        return pl.DataFrame(
            schema={
                "phrase_id": pl.Utf8,
                "phrase": pl.Utf8,
                "deep_comment_count": pl.Int64,
                "max_verified_depth": pl.Int64,
            }
        )

    return (
        comment_phrase_edges.join(deep_comments, on="comment_id", how="inner")
        .join(phrases.select(["phrase_id", "phrase"]), on="phrase_id", how="left")
        .group_by(["phrase_id", "phrase"])
        .agg(
            pl.len().alias("deep_comment_count"),
            pl.max("verified_depth").alias("max_verified_depth"),
        )
        .sort(["deep_comment_count", "max_verified_depth", "phrase"], descending=[True, True, False])
    )
