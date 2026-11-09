"""Проверки рекурсивного BFS и учебного режима."""

import tempfile
import unittest
from pathlib import Path

from src.graph import TestRepository, build_graph


class GraphTests(unittest.TestCase):
    """Проверяет обход, фильтрацию и циклы."""

    def test_levels(self):
        """BFS обходит все уровни и общую зависимость лишь раз."""
        graph = build_graph("A", TestRepository("fixtures/demo.json"))
        self.assertEqual(list(graph), ["A", "B", "C", "D", "E"])
        self.assertEqual(graph["C"], ["D", "E"])

    def test_cycle(self):
        """Цикл не приводит к бесконечному обходу."""
        graph = build_graph("A", TestRepository("fixtures/cycle.json"))
        self.assertEqual(graph, {"A": ["B"], "B": ["C"],
                                 "C": ["A"]})

    def test_filter(self):
        """Отбрасывает пакеты с указанной подстрокой."""
        graph = build_graph("A", TestRepository("fixtures/branches.json"),
                            "E")
        self.assertNotIn("E", graph)
        self.assertNotIn("E", graph["B"])

    def test_invalid_fixture(self):
        """Отклоняет посторонние имена и неизвестные вершины."""
        with tempfile.TemporaryDirectory() as directory:
            file = Path(directory) / "wrong.json"
            for data in ('{"a": []}', '{"A": ["B"]}'):
                file.write_text(data, encoding="utf-8")
                with self.assertRaises(ValueError):
                    TestRepository(file)
