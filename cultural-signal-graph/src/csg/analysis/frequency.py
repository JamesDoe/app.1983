from __future__ import annotations

import polars as pl


def phrase_frequency(phrases: pl.DataFrame) -> pl.DataFrame:
    return phrases.select(["phrase_id", "phrase", "occurrence_count"]).sort(
        ["occurrence_count", "phrase"],
        descending=[True, False],
    )
