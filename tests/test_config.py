"""Проверки конфигурации (этап 1)."""

import unittest
from dataclasses import replace

from src.config import read_config, validate


class ConfigTests(unittest.TestCase):
    """Проверяет параметры и сообщения об ошибках."""

    def test_valid(self):
        """Принимает правильный TOML."""
        self.assertEqual(read_config("configs/test.toml").package, "A")

    def test_each_invalid_parameter(self):
        """Отклоняет каждое неправильное значение."""
        base = vars(read_config("configs/test.toml"))
        wrong = {"package": "abc", "repository": "missing.json",
                 "test_mode": "yes", "output": "image.png",
                 "ascii_tree": "yes", "filter_substring": 12}
        for key, value in wrong.items():
            with self.subTest(key=key), self.assertRaises(ValueError):
                validate({**base, key: value})

    def test_missing_parameter(self):
        """Отклоняет отсутствующий параметр."""
        data = vars(read_config("configs/test.toml"))
        data.pop("package")
        with self.assertRaisesRegex(ValueError, "package"):
            validate(data)

    def test_bad_url(self):
        """Отклоняет некорректный URL реального реестра."""
        data = vars(replace(read_config("configs/test.toml"),
                            test_mode=False, package="express"))
        with self.assertRaises(ValueError):
            validate(data)
