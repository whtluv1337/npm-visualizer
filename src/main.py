"""Консольное приложение для анализа зависимостей npm."""

import argparse

from src.config import read_config
from src.graph import TestRepository, build_graph
from src.order import dependency_order
from src.registry import NpmRegistry
from src.visual import ascii_tree, save_graph


def parse_arguments():
    """Читает путь к TOML-конфигурации."""
    parser = argparse.ArgumentParser(description="Практическая №2, вариант 23")
    parser.add_argument("config", help="путь к файлу настроек TOML")
    return parser.parse_args()


def main():
    """Строит граф, показывает порядок и сохраняет визуализацию."""
    arguments = parse_arguments()
    try:
        config = read_config(arguments.config)
        repository = (TestRepository(config.repository) if config.test_mode
                      else NpmRegistry(config.repository))
        graph = build_graph(config.package, repository,
                            config.filter_substring)
        ordered, blocked = dependency_order(graph)
        d2_file, svg_file, renderer = save_graph(graph, config.output)
    except (ValueError, OSError) as error:
        print(f"Ошибка: {error}")
        return 1
    print(f"Пакет: {config.package}")
    print(f"Граф: {len(graph)} вершин, "
          f"{sum(map(len, graph.values()))} рёбер")
    print("Порядок зависимостей:", ", ".join(ordered) or "(нет)")
    if blocked:
        print("Есть цикл или зависимость от цикла:", ", ".join(blocked))
    if config.ascii_tree:
        print("ASCII-дерево:")
        print(ascii_tree(config.package, graph))
    print(f"D2: {d2_file}")
    print(f"SVG: {svg_file} ({renderer})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
