"""Виртуальная файловая система: CSV загружается только в память."""
import base64
import csv
import posixpath
from dataclasses import dataclass


@dataclass
class Node:
    """Тип узла и двоичное содержимое файла."""

    kind: str
    data: bytes = b""


class VFS:
    """Хранит абсолютные POSIX-пути независимо от файловой системы ОС."""

    def __init__(self):
        """Создать корень пустой файловой системы."""
        self.nodes = {"/": Node("dir")}

    @staticmethod
    def resolve(path, cwd="/"):
        """Нормализовать абсолютный или относительный путь."""
        joined = path if path.startswith("/") else posixpath.join(cwd, path)
        return "/" + posixpath.normpath(joined).lstrip("/")

    @classmethod
    def load(cls, path):
        """Прочитать CSV и проверить узлы и их родительские каталоги."""
        vfs = cls()
        with path.open(encoding="utf-8-sig", newline="") as source:
            reader = csv.DictReader(source)
            if reader.fieldnames != ["path", "type", "content"]:
                raise ValueError("ожидаются колонки path,type,content")
            seen = set()
            for row in reader:
                if row.get("path") in seen:
                    raise ValueError(f"повтор пути: {row['path']}")
                seen.add(row.get("path"))
                vfs._add_row(row)
        vfs._check_parents()
        return vfs

    def _add_row(self, row):
        """Проверить и добавить запись, декодируя base64 у файлов."""
        if None in row or any(value is None for value in row.values()):
            raise ValueError("неверное число колонок CSV")
        path, kind, content = row["path"], row["type"], row["content"]
        if not path.startswith("/") or self.resolve(path) != path:
            raise ValueError(f"неканонический абсолютный путь: {path}")
        if kind not in {"file", "dir"}:
            raise ValueError(f"неизвестный тип узла: {kind}")
        if path in self.nodes and path != "/":
            raise ValueError(f"повтор пути: {path}")
        if path == "/" and kind != "dir":
            raise ValueError("корень должен быть каталогом")
        if kind == "dir" and content:
            raise ValueError("каталог не должен содержать данные")
        data = base64.b64decode(content, validate=True)
        self.nodes[path] = Node(kind, data)

    def _check_parents(self):
        """Запретить узлы без родительского каталога."""
        for path in self.nodes:
            if path != "/":
                self.require(posixpath.dirname(path), "dir")

    def require(self, path, kind=None):
        """Получить узел или сообщить об отсутствии/неверном типе."""
        if path not in self.nodes:
            raise ValueError(f"путь не найден: {path}")
        node = self.nodes[path]
        if kind and node.kind != kind:
            raise ValueError(f"ожидается {kind}: {path}")
        return node

    def children(self, path):
        """Вернуть отсортированные непосредственные имена каталога."""
        self.require(path, "dir")
        return sorted(posixpath.basename(item) for item in self.nodes
                      if item != "/" and posixpath.dirname(item) == path)
