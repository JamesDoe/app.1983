from __future__ import annotations

from datetime import datetime, timezone

import polars as pl

from csg.cli.analyze import analyze, compute_signal_salience


def make_test_tables() -> tuple[pl.DataFrame, pl.DataFrame, pl.DataFrame, pl.DataFrame]:
    phrases = pl.DataFrame(
        [
            {"phrase_id": "phrase_00001", "phrase": "hrbt", "occurrence_count": 2, "first_seen": datetime(2026, 3, 10, tzinfo=timezone.utc)},
            {"phrase_id": "phrase_00002", "phrase": "vb", "occurrence_count": 1, "first_seen": datetime(2026, 3, 10, tzinfo=timezone.utc)},
            {"phrase_id": "phrase_00003", "phrase": "ghent", "occurrence_count": 1, "first_seen": datetime(2026, 3, 18, tzinfo=timezone.utc)},
        ]
    )
    comment_phrase_edges = pl.DataFrame(
        [
            {"comment_id": "c1", "phrase_id": "phrase_00001"},
            {"comment_id": "c1", "phrase_id": "phrase_00002"},
            {"comment_id": "c2", "phrase_id": "phrase_00001"},
            {"comment_id": "c3", "phrase_id": "phrase_00003"},
        ]
    )
    reply_edges = pl.DataFrame(
        [
            {"parent_comment_id": "c1", "child_comment_id": "c2", "depth": 6, "thread_id": "t1"},
            {"parent_comment_id": "c2", "child_comment_id": "c3", "depth": 7, "thread_id": "t1"},
        ]
    )
    comments = pl.DataFrame(
        [
            {"content_id": "c1", "thread_id": "t1", "parent_id": "t3_t1", "created_at": datetime(2026, 3, 10, tzinfo=timezone.utc), "score": 4},
            {"content_id": "c2", "thread_id": "t1", "parent_id": "t1_c1", "created_at": datetime(2026, 3, 10, tzinfo=timezone.utc), "score": 5},
            {"content_id": "c3", "thread_id": "t1", "parent_id": "t1_c2", "created_at": datetime(2026, 3, 18, tzinfo=timezone.utc), "score": 7},
        ]
    )
    return phrases, comment_phrase_edges, reply_edges, comments


def test_compute_signal_salience() -> None:
    phrases, comment_phrase_edges, _reply_edges, comments = make_test_tables()
    comment_depths = pl.DataFrame(
        [
            {"comment_id": "c1", "verified_depth": 5},
            {"comment_id": "c2", "verified_depth": 6},
            {"comment_id": "c3", "verified_depth": 7},
        ]
    )

    result = compute_signal_salience(phrases, comment_phrase_edges, comments, comment_depths)
    assert result.height == 3
    assert result["phrase"][0] == "hrbt"


def test_compute_signal_salience_handles_negative_scores() -> None:
    phrases = pl.DataFrame(
        [
            {"phrase_id": "phrase_00001", "phrase": "hrbt", "occurrence_count": 1},
        ]
    )
    comment_phrase_edges = pl.DataFrame([{"comment_id": "c1", "phrase_id": "phrase_00001"}])
    comments = pl.DataFrame([{"content_id": "c1", "score": -4}])
    comment_depths = pl.DataFrame([{"comment_id": "c1", "verified_depth": 2}])

    result = compute_signal_salience(phrases, comment_phrase_edges, comments, comment_depths)
    assert result.height == 1
    assert result["total_comment_score"][0] == 0.0
    assert result["signal_salience"][0] == 0.0


def test_analyze_writes_expected_outputs(tmp_path) -> None:
    phrases, comment_phrase_edges, reply_edges, comments = make_test_tables()
    phrases_path = tmp_path / "phrases.parquet"
    comment_phrase_edges_path = tmp_path / "comment_phrase_edges.parquet"
    reply_edges_path = tmp_path / "reply_edges.parquet"
    comments_path = tmp_path / "comments.parquet"
    output_dir = tmp_path / "artifacts"

    phrases.write_parquet(phrases_path)
    comment_phrase_edges.write_parquet(comment_phrase_edges_path)
    reply_edges.write_parquet(reply_edges_path)
    comments.write_parquet(comments_path)

    outputs = analyze(phrases_path, comment_phrase_edges_path, reply_edges_path, comments_path, output_dir)

    assert outputs["phrase_cooccurrence"].exists()
    assert outputs["contested_phrases"].exists()
    assert outputs["temporal_phrase_counts"].exists()
    assert outputs["top_signals"].exists()
