"""Консольное приложение для анализа зависимостей npm."""

import argparse

from src.config import read_config
from src.graph import TestRepository, build_graph
from src.order import dependency_order
from src.registry import NpmRegistry


def parse_arguments():
    """Читает путь к TOML-конфигурации."""
    parser = argparse.ArgumentParser(description="Практическая №2, вариант 23")
    parser.add_argument("config", help="путь к файлу настроек TOML")
    return parser.parse_args()


def main():
    """Показывает порядок зависимостей (этап 4)."""
    arguments = parse_arguments()
    try:
        config = read_config(arguments.config)
        repository = (TestRepository(config.repository) if config.test_mode
                      else NpmRegistry(config.repository))
        graph = build_graph(config.package, repository,
                            config.filter_substring)
    except ValueError as error:
        print(f"Ошибка: {error}")
        return 1
    ordered, blocked = dependency_order(graph)
    print(f"Порядок зависимостей для {config.package}:")
    for index, package in enumerate(ordered, 1):
        print(f"  {index}. {package}")
    if blocked:
        print("Внимание: цикл или зависимость от цикла:",
              ", ".join(blocked))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
