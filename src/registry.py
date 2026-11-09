"""Получение прямых npm-зависимостей по HTTP API реестра."""

import json
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen


class NpmRegistry:
    """Читает метаданные пакетов без npm и сторонних библиотек."""

    def __init__(self, base_url):
        """Сохраняет адрес реестра и пустой кеш ответов."""
        self.base_url = base_url.rstrip("/")
        self.cache = {}

    def dependencies(self, package):
        """Возвращает runtime dependencies последней версии пакета."""
        if package in self.cache:
            return self.cache[package]
        encoded = quote(package, safe="")
        url = f"{self.base_url}/{encoded}/latest"
        request = Request(url, headers={"Accept": "application/json"})
        try:
            with urlopen(request, timeout=15) as response:
                metadata = json.load(response)
        except (HTTPError, URLError, TimeoutError,
                json.JSONDecodeError) as error:
            raise ValueError(f"npm: не удалось получить {package}: {error}") \
                from error
        if not isinstance(metadata, dict):
            raise ValueError(f"npm: неправильный ответ для {package}")
        names = metadata.get("dependencies", {})
        if not isinstance(names, dict):
            raise ValueError(f"npm: неправильные зависимости {package}")
        result = sorted(names)
        self.cache[package] = result
        return result
