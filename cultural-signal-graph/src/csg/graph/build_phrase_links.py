from __future__ import annotations

from itertools import combinations

import networkx as nx


def build_phrase_links(records: list[dict]) -> nx.Graph:
    graph = nx.Graph()
    for record in records:
        phrases = sorted(set(record.get("phrases", [])))
        for phrase in phrases:
            graph.add_node(phrase)
        for left, right in combinations(phrases, 2):
            weight = graph.get_edge_data(left, right, {}).get("weight", 0) + 1
            graph.add_edge(left, right, weight=weight)
    return graph

