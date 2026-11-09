"""Тесты порядка обработки зависимостей."""

import unittest

from src.graph import TestRepository, build_graph
from src.order import dependency_order


class OrderTests(unittest.TestCase):
    """Проверяет порядок и циклические графы."""

    def test_dependencies_before_package(self):
        """Пакет появляется после всех своих зависимостей."""
        graph = build_graph("A", TestRepository("fixtures/demo.json"))
        order, blocked = dependency_order(graph)
        self.assertEqual(blocked, [])
        for parent, children in graph.items():
            for child in children:
                self.assertLess(order.index(child), order.index(parent))

    def test_cycle_reported(self):
        """Цикл не выдаётся за корректный порядок."""
        graph = build_graph("A", TestRepository("fixtures/cycle.json"))
        order, blocked = dependency_order(graph)
        self.assertEqual(order, [])
        self.assertEqual(blocked, ["A", "B", "C"])

    def test_filter(self):
        """После фильтрации строится правильный порядок."""
        graph = build_graph("A", TestRepository("fixtures/branches.json"),
                            "E")
        order, blocked = dependency_order(graph)
        self.assertFalse(blocked)
        self.assertLess(order.index("F"), order.index("C"))
