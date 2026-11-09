"""Консольное приложение для анализа зависимостей npm."""

import argparse

from src.config import read_config


def parse_arguments():
    """Читает путь к TOML-конфигурации."""
    parser = argparse.ArgumentParser(description="Практическая №2, вариант 23")
    parser.add_argument("config", help="путь к файлу настроек TOML")
    return parser.parse_args()


def main():
    """Читает конфигурацию и показывает её значения (этап 1)."""
    arguments = parse_arguments()
    try:
        config = read_config(arguments.config)
    except ValueError as error:
        print(f"Ошибка: {error}")
        return 1
    for name, value in vars(config).items():
        print(f"{name}: {value}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
