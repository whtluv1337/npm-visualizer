"""Порядок обработки зависимостей перед зависящими пакетами."""

import heapq


def build_dependents(graph):
    """Определяет, какие пакеты зависят от каждой вершины."""
    dependents = {name: [] for name in graph}
    for parent, children in graph.items():
        for child in children:
            if child in dependents:
                dependents[child].append(parent)
    return dependents


def consume_ready(ready, prerequisites, dependents):
    """Выводит зависимости прежде пакетов, которые их используют."""
    ordered = []
    while ready:
        package = heapq.heappop(ready)
        ordered.append(package)
        for parent in sorted(dependents[package]):
            prerequisites[parent] -= 1
            if not prerequisites[parent]:
                heapq.heappush(ready, parent)
    return ordered


def dependency_order(graph):
    """Строит топологический порядок и возвращает оставшиеся узлы."""
    prerequisites = {name: len(children) for name, children in graph.items()}
    dependents = build_dependents(graph)
    ready = [name for name, count in prerequisites.items() if not count]
    heapq.heapify(ready)
    ordered = consume_ready(ready, prerequisites, dependents)
    blocked = sorted(set(graph) - set(ordered))
    return ordered, blocked
