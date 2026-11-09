"""Построение графа зависимостей рекурсивным обходом BFS."""

import json
import re
from pathlib import Path


TEST_PACKAGE = re.compile(r"^[A-Z]+$")


def validate_names(graph):
    """Проверяет формат имён пакетов и их прямых зависимостей."""
    for name, children in graph.items():
        if not isinstance(name, str) or not TEST_PACKAGE.fullmatch(name):
            raise ValueError("имена пакетов должны быть заглавными A-Z")
        if not isinstance(children, list):
            raise ValueError(f"{name}: ожидается список зависимостей")
        for child in children:
            if not isinstance(child, str):
                raise ValueError(f"{name}: недопустимое имя зависимости")
            if not TEST_PACKAGE.fullmatch(child):
                raise ValueError(f"{name}: недопустимое имя зависимости")


def validate_links(graph):
    """Проверяет, что каждая зависимость существует в учебном графе."""
    for children in graph.values():
        if any(child not in graph for child in children):
            raise ValueError("в графе есть ссылка на неизвестный пакет")


class TestRepository:
    """Читает учебный граф из JSON, не обращаясь к сети."""

    def __init__(self, filename):
        """Читает и проверяет содержимое учебного файла."""
        try:
            self.graph = json.loads(Path(filename).read_text("utf-8"))
        except (OSError, json.JSONDecodeError) as error:
            raise ValueError(f"тестовый граф: {error}") from error
        if not isinstance(self.graph, dict):
            raise ValueError("тестовый граф должен быть объектом JSON")
        validate_names(self.graph)
        validate_links(self.graph)

    def dependencies(self, package):
        """Возвращает список прямых зависимостей пакета."""
        if package not in self.graph:
            raise ValueError(f"пакет {package} не найден в тестовом графе")
        return sorted(set(self.graph[package]))


def allowed_children(children, filter_substring):
    """Исключает зависимости, содержащие запрещённую подстроку."""
    return sorted({
        child for child in children
        if not filter_substring or filter_substring not in child
    })


def build_graph(root, repository, filter_substring=""):
    """Обходит все доступные зависимости рекурсивным BFS по уровням."""
    if filter_substring and filter_substring in root:
        return {}
    result = {}
    visited = set()

    def visit_level(frontier):
        """Рекурсивно обрабатывает один уровень обхода."""
        if not frontier:
            return
        following = []
        for package in frontier:
            if package in visited:
                continue
            visited.add(package)
            children = repository.dependencies(package)
            allowed = allowed_children(children, filter_substring)
            result[package] = allowed
            following.extend(child for child in allowed
                             if child not in visited)
        visit_level(list(dict.fromkeys(following)))

    visit_level([root])
    return result
