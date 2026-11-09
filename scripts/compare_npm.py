"""Сравнение прямых зависимостей программы с настоящим npm CLI."""

import argparse
import json
import subprocess

from src.config import read_config
from src.registry import NpmRegistry


def read_npm(package):
    """Читает зависимости через npm CLI только для сравнения."""
    finished = subprocess.run(
        ["npm.cmd", "view", f"{package}@latest", "dependencies", "--json"],
        capture_output=True, text=True, check=False,
    )
    if finished.returncode:
        raise ValueError(f"npm завершился с ошибкой: {finished.stderr}")
    parsed = json.loads(finished.stdout or "null")
    if parsed is None:
        return set()
    if not isinstance(parsed, dict):
        raise ValueError("npm: неожиданный формат ответа")
    return set(parsed)


def main():
    """Показывает совпадения и расхождения с командой npm view."""
    parser = argparse.ArgumentParser(description="Сравнение с npm")
    parser.add_argument("config", help="конфигурация реального npm-реестра")
    arguments = parser.parse_args()
    try:
        config = read_config(arguments.config)
        if config.test_mode:
            raise ValueError("нужен режим настоящего npm")
        ours = set(NpmRegistry(config.repository).dependencies(config.package))
        npm = read_npm(config.package)
    except (ValueError, OSError, json.JSONDecodeError) as error:
        print(f"Ошибка сравнения: {error}")
        return 1
    print("Совпадают:", ", ".join(sorted(ours & npm)) or "(нет)")
    print("Только у нас:", ", ".join(sorted(ours - npm)) or "(нет)")
    print("Только у npm:", ", ".join(sorted(npm - ours)) or "(нет)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
