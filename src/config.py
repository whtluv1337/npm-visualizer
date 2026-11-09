"""Чтение и проверка конфигурации TOML."""

import re
import tomllib
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlparse


PACKAGE_NAME = re.compile(r"^(?:@[a-z0-9._~-]+/)?[a-z0-9._~-]+$")
TEST_NAME = re.compile(r"^[A-Z]+$")


@dataclass(frozen=True)
class Config:
    """Пользовательские настройки приложения."""

    package: str
    repository: str
    test_mode: bool
    output: str
    ascii_tree: bool
    filter_substring: str


def check_repository(repository, test_mode):
    """Проверяет расположение реального или тестового репозитория."""
    if not isinstance(repository, str) or not repository.strip():
        raise ValueError("repository: нужен непустой путь или URL")
    if test_mode:
        if not Path(repository).is_file():
            raise ValueError("repository: тестовый файл не найден")
        return
    parsed = urlparse(repository)
    if parsed.scheme not in ("https", "http") or not parsed.netloc:
        raise ValueError("repository: нужен URL с http/https")


def validate(data):
    """Проверяет типы и значения всех шести параметров."""
    required = ("package", "repository", "test_mode", "output",
                "ascii_tree", "filter_substring")
    for key in required:
        if key not in data:
            raise ValueError(f"не указан параметр {key}")
    for key in ("package", "output", "filter_substring"):
        if not isinstance(data[key], str):
            raise ValueError(f"{key}: ожидается строка")
    for key in ("test_mode", "ascii_tree"):
        if type(data[key]) is not bool:
            raise ValueError(f"{key}: ожидается true или false")
    name_pattern = TEST_NAME if data["test_mode"] else PACKAGE_NAME
    if not name_pattern.fullmatch(data["package"]):
        raise ValueError("package: недопустимое имя пакета")
    if not data["output"].lower().endswith(".svg"):
        raise ValueError("output: имя должно оканчиваться на .svg")
    if not Path(data["output"]).name:
        raise ValueError("output: нужно указать имя файла")
    check_repository(data["repository"], data["test_mode"])
    return Config(**{key: data[key] for key in required})


def read_config(filename):
    """Открывает TOML-файл и возвращает проверенную конфигурацию."""
    try:
        with open(filename, "rb") as source:
            data = tomllib.load(source)
    except (OSError, tomllib.TOMLDecodeError) as error:
        raise ValueError(f"не удалось прочитать TOML: {error}") from error
    if not isinstance(data, dict):
        raise ValueError("конфигурация должна быть таблицей TOML")
    return validate(data)
