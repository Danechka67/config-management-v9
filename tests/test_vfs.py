"""Проверка CSV, вложенности и двоичных данных."""
import base64
import tempfile
import unittest
from pathlib import Path
from src.vfs import VFS


class VFSTest(unittest.TestCase):
    """Проверяет формат и инварианты виртуальной файловой системы."""

    def load_text(self, text):
        """Загрузить временный CSV без изменения примеров проекта."""
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "test.csv"
            path.write_text(text, encoding="utf-8")
            return VFS.load(path)

    def test_deep(self):
        """Загрузить три уровня каталогов и Unicode-файл."""
        vfs = VFS.load(Path("examples/deep.csv"))
        node = vfs.require("/docs/course/week1/notes.txt", "file")
        self.assertIn("Третья", node.data.decode())
        self.assertEqual(vfs.children("/docs"), ["course"])

    def test_binary(self):
        """Двоичное содержимое восстанавливается точно."""
        data = bytes(range(256))
        encoded = base64.b64encode(data).decode()
        vfs = self.load_text(f"path,type,content\n/x,file,{encoded}\n")
        self.assertEqual(vfs.require("/x").data, data)

    def test_invalid(self):
        """Некорректные записи и структура отклоняются."""
        cases = ["wrong,header\n", "path,type,content\n/x,file,!\n",
                 "path,type,content\n/a/x,file,\n",
                 "path,type,content\n/x,file,\n/x,file,\n",
                 "path,type,content\n/x,dir,YQ==\n",
                 "path,type,content\n/x,unknown,\n",
                 "path,type,content\n/../x,file,\n",
                 "path,type,content\n/x,file\n"]
        for text in cases:
            with self.subTest(text=text), self.assertRaises(ValueError):
                self.load_text(text)

    def test_paths(self):
        """Относительные пути, .. и повторные / нормализуются."""
        self.assertEqual(VFS.resolve("../x", "/docs"), "/x")
        self.assertEqual(VFS.resolve("../../.."), "/")
        self.assertEqual(VFS.resolve("//docs//course"), "/docs/course")
