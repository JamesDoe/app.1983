from __future__ import annotations

from itertools import combinations

import polars as pl


def phrase_cooccurrence(comment_phrase_edges: pl.DataFrame, phrases: pl.DataFrame) -> pl.DataFrame:
    phrase_lookup = {
        row["phrase_id"]: row["phrase"]
        for row in phrases.select(["phrase_id", "phrase"]).iter_rows(named=True)
    }

    phrase_ids_by_comment: dict[str, list[str]] = {}
    for row in comment_phrase_edges.iter_rows(named=True):
        phrase_ids_by_comment.setdefault(str(row["comment_id"]), []).append(str(row["phrase_id"]))

    counts: dict[tuple[str, str], int] = {}
    for phrase_ids in phrase_ids_by_comment.values():
        unique_ids = sorted(set(phrase_ids))
        for left_id, right_id in combinations(unique_ids, 2):
            pair = (left_id, right_id)
            counts[pair] = counts.get(pair, 0) + 1

    rows = [
        {
            "left_phrase_id": left_id,
            "left_phrase": phrase_lookup[left_id],
            "right_phrase_id": right_id,
            "right_phrase": phrase_lookup[right_id],
            "cooccurrence_count": count,
        }
        for (left_id, right_id), count in sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    ]
    return pl.DataFrame(
        rows,
        schema={
            "left_phrase_id": pl.Utf8,
            "left_phrase": pl.Utf8,
            "right_phrase_id": pl.Utf8,
            "right_phrase": pl.Utf8,
            "cooccurrence_count": pl.Int64,
        },
    ) if rows else pl.DataFrame(
        schema={
            "left_phrase_id": pl.Utf8,
            "left_phrase": pl.Utf8,
            "right_phrase_id": pl.Utf8,
            "right_phrase": pl.Utf8,
            "cooccurrence_count": pl.Int64,
        }
    )
