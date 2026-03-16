from __future__ import annotations

import polars as pl

from csg.graph.build_reply_graph import build_reply_graph_tables, normalize_parent_comment_id


def test_normalize_parent_comment_id() -> None:
    assert normalize_parent_comment_id("t1_abc123") == "abc123"
    assert normalize_parent_comment_id("t3_thread1") is None
    assert normalize_parent_comment_id(None) is None


def test_build_reply_graph_tables() -> None:
    comments = pl.DataFrame(
        [
            {"content_id": "c1", "parent_id": "t3_thread1", "thread_id": "thread1", "depth": 1},
            {"content_id": "c2", "parent_id": "t1_c1", "thread_id": "thread1", "depth": 2},
            {"content_id": "c3", "parent_id": "t1_c2", "thread_id": "thread1", "depth": 3},
            {"content_id": "c4", "parent_id": "t1_c1", "thread_id": "thread1", "depth": 2},
        ]
    )

    edges, thread_metrics, comment_metrics = build_reply_graph_tables(comments)

    assert edges.to_dicts() == [
        {"parent_comment_id": "c1", "child_comment_id": "c2", "depth": 2, "thread_id": "thread1"},
        {"parent_comment_id": "c1", "child_comment_id": "c4", "depth": 2, "thread_id": "thread1"},
        {"parent_comment_id": "c2", "child_comment_id": "c3", "depth": 3, "thread_id": "thread1"},
    ]

    assert thread_metrics.to_dicts() == [
        {"thread_id": "thread1", "comment_count": 4, "max_depth": 3, "avg_depth": 2.0}
    ]

    metrics_by_comment = {row["comment_id"]: row for row in comment_metrics.to_dicts()}
    assert metrics_by_comment["c1"]["verified_depth"] == 1
    assert metrics_by_comment["c1"]["thread_root"] == "c1"
    assert metrics_by_comment["c1"]["descendant_count"] == 3
    assert metrics_by_comment["c1"]["branch_size"] == 4
    assert metrics_by_comment["c3"]["verified_depth"] == 3
    assert metrics_by_comment["c3"]["descendant_count"] == 0

