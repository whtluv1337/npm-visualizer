"""Проверка D2, ASCII и корректности SVG."""

import tempfile
import unittest
import xml.etree.ElementTree as et
from pathlib import Path
from unittest.mock import patch

from src.graph import TestRepository, build_graph
from src.visual import ascii_tree, save_graph, to_d2, to_svg


def sample_graph():
    """Готовит учебный граф для независимых тестов."""
    return build_graph("A", TestRepository("fixtures/demo.json"))


class VisualTests(unittest.TestCase):
    """Проверяет три способа показа графа."""

    def test_d2(self):
        """D2 содержит все рёбра ориентированного графа."""
        source = to_d2(sample_graph())
        self.assertIn('"A" -> "B"', source)
        self.assertIn('"C" -> "E"', source)

    def test_ascii_shared_node(self):
        """В ASCII общий потомок выводится с отметкой повтора."""
        tree = ascii_tree("A", sample_graph())
        self.assertIn("D (повтор/цикл)", tree)

    def test_svg_xml(self):
        """Сгенерированный SVG является корректным XML."""
        root = et.fromstring(to_svg(sample_graph()))
        self.assertTrue(root.tag.endswith("svg"))
        self.assertIn("A", to_svg(sample_graph()))

    @patch("src.visual.shutil.which", return_value=None)
    def test_save(self, unused):
        """Записывает D2 и SVG даже без установленного D2 CLI."""
        with tempfile.TemporaryDirectory() as directory:
            filename = str(Path(directory) / "graph.svg")
            d2, svg, renderer = save_graph(sample_graph(), filename)
            self.assertTrue(d2.is_file())
            self.assertTrue(svg.is_file())
            self.assertIn("встроенный", renderer)
