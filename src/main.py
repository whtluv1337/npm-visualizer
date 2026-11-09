"""Консольное приложение для анализа зависимостей npm."""

import argparse

from src.config import read_config
from src.graph import TestRepository, build_graph
from src.registry import NpmRegistry


def parse_arguments():
    """Читает путь к TOML-конфигурации."""
    parser = argparse.ArgumentParser(description="Практическая №2, вариант 23")
    parser.add_argument("config", help="путь к файлу настроек TOML")
    return parser.parse_args()


def main():
    """Формирует граф зависимостей рекурсивным BFS (этап 3)."""
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
    print(f"Граф зависимостей {config.package}:")
    for package, children in graph.items():
        print(f"  {package}: {', '.join(children) or '(нет)'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
