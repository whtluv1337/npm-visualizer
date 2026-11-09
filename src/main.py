"""Консольное приложение для анализа зависимостей npm."""

import argparse

from src.config import read_config
from src.registry import NpmRegistry


def parse_arguments():
    """Читает путь к TOML-конфигурации."""
    parser = argparse.ArgumentParser(description="Практическая №2, вариант 23")
    parser.add_argument("config", help="путь к файлу настроек TOML")
    return parser.parse_args()


def main():
    """Выводит прямые npm-зависимости (этап 2)."""
    arguments = parse_arguments()
    try:
        config = read_config(arguments.config)
        if config.test_mode:
            raise ValueError("тестовый режим появится на этапе 3")
        registry = NpmRegistry(config.repository)
        dependencies = registry.dependencies(config.package)
    except ValueError as error:
        print(f"Ошибка: {error}")
        return 1
    print(f"Прямые зависимости {config.package}:")
    for dependency in dependencies:
        print(f"  {dependency}")
    if not dependencies:
        print("  (нет зависимостей)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
