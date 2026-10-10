"""Проверки основных команд варианта 9."""
import unittest
from pathlib import Path
from unittest.mock import patch
from datetime import datetime, timezone
from src.shell import Shell
from src.vfs import Node, VFS


class CommandsTest(unittest.TestCase):
    """Проверяет команды на настоящей VFS с вложенными каталогами."""

    def setUp(self):
        """Создать независимый сеанс для каждой проверки."""
        self.shell = Shell(VFS.load(Path("examples/deep.csv")))

    def test_navigation(self):
        """ls и cd работают с абсолютными и относительными путями."""
        self.assertIn("docs/", self.shell.execute("ls"))
        self.shell.execute("cd /docs/course/week1")
        self.assertEqual(self.shell.execute("ls ."), "notes.txt")
        self.assertIn("Третья", self.shell.execute("tail notes.txt"))
        self.shell.execute("cd ..")
        self.assertEqual(self.shell.cwd, "/docs/course")
        self.shell.execute("cd")
        self.assertEqual(self.shell.cwd, "/")
        self.assertEqual(self.shell.execute("ls /hello.txt"), "hello.txt")

    def test_tail(self):
        """Проверить стандартное N, 0, большое N и пустой файл."""
        self.assertEqual(len(self.shell.execute("tail /log.txt")
                             .splitlines()), 10)
        self.assertEqual(self.shell.execute("tail -n 2 /log.txt"),
                         "line 14\nline 15")
        self.assertEqual(self.shell.execute("tail -n 0 /log.txt"), "")
        self.assertEqual(len(self.shell.execute("tail -n 99 /log.txt")
                             .splitlines()), 15)
        self.assertEqual(self.shell.execute("tail /empty.txt"), "")

    def test_errors(self):
        """Ошибки аргументов и путей не прерывают сеанс."""
        cases = ["ls /missing", "ls a b", "cd /hello.txt", "cd a b",
                 "tail /docs", "tail /missing", "tail -n -1 /log.txt",
                 "tail -n abc /log.txt", "tail", "date invalid"]
        for line in cases:
            with self.subTest(line=line):
                self.assertIn("Ошибка", self.shell.execute(line))
                self.assertTrue(self.shell.running)
        self.assertEqual(self.shell.cwd, "/")

    def test_binary_tail(self):
        """Нетекстовый файл возвращает ошибку UTF-8."""
        self.shell.vfs.nodes["/bad.bin"] = Node("file", b"\xff")
        self.assertIn("Ошибка", self.shell.execute("tail /bad.bin"))

    @patch("src.shell.datetime")
    def test_date(self, clock):
        """Формат времени проверяется с фиксированными часами."""
        clock.now.return_value = datetime(2026, 10, 10,
                                          tzinfo=timezone.utc)
        self.assertEqual(self.shell.execute("date +%Y-%m-%d"),
                         "2026-10-10")
        self.assertTrue(self.shell.execute("date"))
