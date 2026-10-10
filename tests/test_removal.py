"""Удаление в памяти и сохранность физического CSV."""
import unittest
from pathlib import Path
from src.shell import Shell
from src.vfs import Node, VFS


class RemovalTest(unittest.TestCase):
    """Проверяет флаги, защиту каталогов и неизменность источника."""

    def setUp(self):
        """Загрузить отдельную VFS и запомнить байты CSV."""
        self.path = Path("examples/deep.csv")
        self.original = self.path.read_bytes()
        self.shell = Shell(VFS.load(self.path))

    def test_file_and_source(self):
        """Удалённый файл исчезает в сеансе и возвращается при загрузке."""
        self.assertEqual(self.shell.execute("rm /hello.txt"), "")
        self.assertIn("Ошибка", self.shell.execute("tail /hello.txt"))
        self.assertEqual(self.path.read_bytes(), self.original)
        reloaded = VFS.load(self.path)
        self.assertIn("/hello.txt", reloaded.nodes)

    def test_recursive(self):
        """Каталог требует -r, после удаления исчезают все потомки."""
        self.assertIn("Ошибка", self.shell.execute("rm /docs"))
        self.assertEqual(self.shell.execute("rm -r /docs"), "")
        self.assertFalse(any(path.startswith("/docs")
                             for path in self.shell.vfs.nodes))
        self.assertEqual(self.path.read_bytes(), self.original)

    def test_protection(self):
        """Нельзя удалить корень, текущий каталог или его предка."""
        self.shell.execute("cd /docs/course/week1")
        for line in ["rm -rf /", "rm -r .", "rm -r ..", "rm -r /docs"]:
            with self.subTest(line=line):
                self.assertIn("Ошибка", self.shell.execute(line))
        self.assertIn(self.shell.cwd, self.shell.vfs.nodes)

    def test_options(self):
        """-f игнорирует отсутствие, -- разрешает имена с дефисом."""
        self.assertEqual(self.shell.execute("rm -f /missing"), "")
        self.assertEqual(self.shell.execute("rm -f"), "")
        self.assertIn("Ошибка", self.shell.execute("rm -x /log.txt"))
        self.assertIn("Ошибка", self.shell.execute("rm"))
        self.shell.vfs.nodes["/-file"] = Node("file")
        self.assertEqual(self.shell.execute("rm -- -file"), "")
        self.assertNotIn("/-file", self.shell.vfs.nodes)

    def test_multiple_atomic(self):
        """При ошибочном пути список удалений не применяется частично."""
        self.assertIn("Ошибка", self.shell.execute(
            "rm /hello.txt /missing"))
        self.assertIn("/hello.txt", self.shell.vfs.nodes)
        self.assertEqual(self.shell.execute(
            "rm /hello.txt /empty.txt"), "")
        self.assertNotIn("/empty.txt", self.shell.vfs.nodes)
