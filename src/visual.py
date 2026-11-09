"""Формирование D2, SVG и текстового дерева зависимостей."""

from collections import deque
from html import escape
from pathlib import Path
import shutil
import subprocess


def to_d2(graph):
    """Преобразует ориентированный граф в описание D2."""
    lines = ['direction: right', 'classes: {',
             '  pkg: { shape: rectangle }', '}']
    for package in sorted(graph):
        lines.append(f'"{package}": {{ class: pkg }}')
    for package in sorted(graph):
        for dependency in graph[package]:
            lines.append(f'"{package}" -> "{dependency}"')
    return "\n".join(lines) + "\n"


def ascii_tree(root, graph):
    """Строит дерево связей и отмечает уже показанные узлы."""
    if root not in graph:
        return "(пакет отфильтрован)"
    lines = [root]
    seen = {root}

    def visit(package, prefix):
        """Обходит ветви дерева и не зацикливается."""
        children = graph.get(package, [])
        for index, child in enumerate(children):
            last = index == len(children) - 1
            branch = "`-- " if last else "|-- "
            suffix = " (повтор/цикл)" if child in seen else ""
            lines.append(f"{prefix}{branch}{child}{suffix}")
            if child not in seen:
                seen.add(child)
                visit(child, prefix + ("    " if last else "|   "))

    visit(root, "")
    return "\n".join(lines)


def graph_levels(graph):
    """Вычисляет уровни вершин по кратчайшему пути от корня."""
    if not graph:
        return {}
    root = next(iter(graph))
    queue = deque([root])
    levels = {root: 0}
    while queue:
        package = queue.popleft()
        for child in graph.get(package, []):
            if child not in levels:
                levels[child] = levels[package] + 1
                queue.append(child)
    return levels


def node_positions(graph):
    """Располагает пакеты по уровням в простом SVG-макете."""
    levels = graph_levels(graph)
    columns = {}
    for package, level in levels.items():
        columns.setdefault(level, []).append(package)
    width = max(700, (len(columns) + 1) * 230)
    height = max(300, (max(map(len, columns.values()), default=1) + 1)
                 * 110)
    points = {}
    for level, packages in columns.items():
        for index, package in enumerate(sorted(packages)):
            x = 130 + level * 230
            y = (height / (len(packages) + 1)) * (index + 1)
            points[package] = (x, y)
    return width, height, points


def svg_edges(graph, points):
    """Рисует направленные связи между прямоугольниками."""
    lines = []
    for package, children in graph.items():
        for child in children:
            if package not in points or child not in points:
                continue
            x1, y1 = points[package]
            x2, y2 = points[child]
            lines.append(
                f'<path d="M {x1 + 65:.1f} {y1:.1f} '
                f'L {x2 - 65:.1f} {y2:.1f}" '
                'stroke="#637994" stroke-width="2" fill="none" '
                'marker-end="url(#arrow)"/>'
            )
    return lines


def svg_nodes(points):
    """Рисует подписи и карточки пакетов."""
    lines = []
    for name, (x, y) in points.items():
        label = escape(name)
        lines.append(
            f'<rect x="{x - 65:.1f}" y="{y - 23:.1f}" '
            'width="130" height="46" rx="9" fill="#e1edfd" '
            'stroke="#3974b8" stroke-width="1.5"/>'
        )
        lines.append(
            f'<text x="{x:.1f}" y="{y + 5:.1f}" '
            'text-anchor="middle" font-family="Arial,sans-serif" '
            f'font-size="15" fill="#15395f">{label}</text>'
        )
    return lines


def to_svg(graph):
    """Создаёт автономное SVG по тем же рёбрам, что и D2."""
    width, height, points = node_positions(graph)
    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#f7f9fc"/>',
        '<defs><marker id="arrow" markerWidth="8" markerHeight="8" '
        'refX="7" refY="3" orient="auto">',
        '<path d="M0,0 L0,6 L7,3 z" fill="#637994"/>',
        '</marker></defs>',
    ]
    lines.extend(svg_edges(graph, points))
    lines.extend(svg_nodes(points))
    lines.append('</svg>')
    return "\n".join(lines) + "\n"


def save_graph(graph, output):
    """Сохраняет D2 и SVG, используя D2 CLI при его наличии."""
    target = Path(output)
    target.parent.mkdir(parents=True, exist_ok=True)
    d2_file = target.with_suffix(".d2")
    d2_file.write_text(to_d2(graph), encoding="utf-8")
    d2_command = shutil.which("d2")
    if d2_command:
        completed = subprocess.run(
            [d2_command, str(d2_file), str(target)],
            capture_output=True, text=True, check=False,
        )
        if completed.returncode == 0:
            return d2_file, target, "D2 CLI"
    target.write_text(to_svg(graph), encoding="utf-8")
    return d2_file, target, "встроенный SVG-рендерер"
