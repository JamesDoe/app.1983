from __future__ import annotations

from collections import defaultdict, deque
from dataclasses import dataclass
from pathlib import Path

import polars as pl


@dataclass(slots=True)
class CommentGraphMetrics:
    verified_depth: int
    thread_root: str
    descendant_count: int
    branch_size: int


def normalize_parent_comment_id(parent_id: str | None) -> str | None:
    if not parent_id or not isinstance(parent_id, str):
        return None
    if not parent_id.startswith("t1_"):
        return None
    return parent_id.split("_", maxsplit=1)[1]


def build_reply_graph_tables(comments: pl.DataFrame) -> tuple[pl.DataFrame, pl.DataFrame, pl.DataFrame]:
    records = comments.to_dicts()
    comments_by_thread: dict[str, list[dict]] = defaultdict(list)
    for record in records:
        comments_by_thread[str(record["thread_id"])].append(record)

    edge_rows: list[dict] = []
    thread_metric_rows: list[dict] = []
    comment_metric_rows: list[dict] = []

    for thread_id, thread_comments in comments_by_thread.items():
        edges, metrics = build_thread_reply_graph(thread_id, thread_comments)
        edge_rows.extend(edges)
        for comment_id, metric in metrics.items():
            comment_metric_rows.append(
                {
                    "comment_id": comment_id,
                    "thread_id": thread_id,
                    "verified_depth": metric.verified_depth,
                    "thread_root": metric.thread_root,
                    "descendant_count": metric.descendant_count,
                    "branch_size": metric.branch_size,
                }
            )

        depths = [metric.verified_depth for metric in metrics.values()]
        thread_metric_rows.append(
            {
                "thread_id": thread_id,
                "comment_count": len(thread_comments),
                "max_depth": max(depths, default=0),
                "avg_depth": float(sum(depths) / len(depths)) if depths else 0.0,
            }
        )

    edges_frame = pl.DataFrame(
        edge_rows,
        schema={
            "parent_comment_id": pl.Utf8,
            "child_comment_id": pl.Utf8,
            "depth": pl.Int64,
            "thread_id": pl.Utf8,
        },
    ) if edge_rows else pl.DataFrame(
        schema={
            "parent_comment_id": pl.Utf8,
            "child_comment_id": pl.Utf8,
            "depth": pl.Int64,
            "thread_id": pl.Utf8,
        }
    )

    thread_metrics_frame = pl.DataFrame(
        thread_metric_rows,
        schema={
            "thread_id": pl.Utf8,
            "comment_count": pl.Int64,
            "max_depth": pl.Int64,
            "avg_depth": pl.Float64,
        },
    ) if thread_metric_rows else pl.DataFrame(
        schema={
            "thread_id": pl.Utf8,
            "comment_count": pl.Int64,
            "max_depth": pl.Int64,
            "avg_depth": pl.Float64,
        }
    )

    comment_metrics_frame = pl.DataFrame(
        comment_metric_rows,
        schema={
            "comment_id": pl.Utf8,
            "thread_id": pl.Utf8,
            "verified_depth": pl.Int64,
            "thread_root": pl.Utf8,
            "descendant_count": pl.Int64,
            "branch_size": pl.Int64,
        },
    ) if comment_metric_rows else pl.DataFrame(
        schema={
            "comment_id": pl.Utf8,
            "thread_id": pl.Utf8,
            "verified_depth": pl.Int64,
            "thread_root": pl.Utf8,
            "descendant_count": pl.Int64,
            "branch_size": pl.Int64,
        }
    )

    return edges_frame, thread_metrics_frame, comment_metrics_frame


def build_thread_reply_graph(thread_id: str, thread_comments: list[dict]) -> tuple[list[dict], dict[str, CommentGraphMetrics]]:
    comment_ids = {str(record["content_id"]) for record in thread_comments}
    children: dict[str, list[str]] = defaultdict(list)
    parents: dict[str, str | None] = {}

    for record in thread_comments:
        comment_id = str(record["content_id"])
        parent_comment_id = normalize_parent_comment_id(record.get("parent_id"))
        if parent_comment_id not in comment_ids:
            parent_comment_id = None
        parents[comment_id] = parent_comment_id
        if parent_comment_id:
            children[parent_comment_id].append(comment_id)

    roots = sorted(comment_id for comment_id, parent_id in parents.items() if parent_id is None)
    metrics: dict[str, CommentGraphMetrics] = {}
    queue: deque[tuple[str, int, str]] = deque((root_id, 1, root_id) for root_id in roots)

    while queue:
        comment_id, depth, root_id = queue.popleft()
        if comment_id in metrics:
            continue
        metrics[comment_id] = CommentGraphMetrics(
            verified_depth=depth,
            thread_root=root_id,
            descendant_count=0,
            branch_size=1,
        )
        for child_id in sorted(children.get(comment_id, [])):
            queue.append((child_id, depth + 1, root_id))

    for comment_id in reversed(topological_order(children, roots)):
        descendant_count = sum(metrics[child_id].branch_size for child_id in children.get(comment_id, []))
        metric = metrics[comment_id]
        metric.descendant_count = descendant_count
        metric.branch_size = descendant_count + 1

    edge_rows = []
    for child_id, parent_id in sorted(parents.items()):
        if not parent_id:
            continue
        edge_rows.append(
            {
                "parent_comment_id": parent_id,
                "child_comment_id": child_id,
                "depth": metrics[child_id].verified_depth,
                "thread_id": thread_id,
            }
        )

    return edge_rows, metrics


def topological_order(children: dict[str, list[str]], roots: list[str]) -> list[str]:
    order: list[str] = []
    stack = list(reversed(roots))
    while stack:
        current = stack.pop()
        order.append(current)
        for child in reversed(sorted(children.get(current, []))):
            stack.append(child)
    return order


def build_reply_graph(input_path: Path, edges_output: Path, metrics_output: Path) -> tuple[Path, Path]:
    comments = pl.read_parquet(input_path)
    edges, thread_metrics, _comment_metrics = build_reply_graph_tables(comments)
    edges_output.parent.mkdir(parents=True, exist_ok=True)
    metrics_output.parent.mkdir(parents=True, exist_ok=True)
    edges.write_parquet(edges_output)
    thread_metrics.write_parquet(metrics_output)
    return edges_output, metrics_output
