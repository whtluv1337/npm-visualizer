"""Тесты получения npm-метаданных без сетевых запросов."""

import io
import json
import unittest
from unittest.mock import patch

from src.registry import NpmRegistry


class Response:
    """Простой заменитель сетевого ответа."""

    def __init__(self, data):
        """Запоминает тело ответа."""
        self.data = io.BytesIO(json.dumps(data).encode())

    def __enter__(self):
        """Открывает контекст."""
        return self.data

    def __exit__(self, *arguments):
        """Завершает контекст."""
        self.data.close()


class RegistryTests(unittest.TestCase):
    """Проверяет получение прямых зависимостей."""

    @patch("src.registry.urlopen")
    def test_direct_dependencies(self, get_url):
        """Выводит только прямые runtime dependencies."""
        get_url.return_value = Response({
            "dependencies": {"z": "^1", "b": "^2"},
            "devDependencies": {"dev": "^1"},
        })
        registry = NpmRegistry("https://registry.npmjs.org")
        self.assertEqual(registry.dependencies("pkg"), ["b", "z"])
        self.assertEqual(registry.dependencies("pkg"), ["b", "z"])
        get_url.assert_called_once()

    @patch("src.registry.urlopen")
    def test_scoped_package(self, get_url):
        """Учитывает имена npm-пакетов с областью действия."""
        get_url.return_value = Response({"dependencies": {}})
        NpmRegistry("https://registry.npmjs.org").dependencies("@a/b")
        self.assertIn("%40a%2Fb", get_url.call_args.args[0].full_url)
