"""Проверки парсера и управления сеансом."""
import unittest
from src.shell import Shell


class ShellTest(unittest.TestCase):
    """Проверяет пустой ввод, неизвестные команды и exit."""

    def test_blank(self):
        """Пробельная строка не выполняет команду."""
        self.assertEqual(Shell().execute("  "), "")

    def test_unknown(self):
        """Неизвестная команда возвращает ошибку."""
        self.assertIn("Ошибка", Shell().execute("unknown"))

    def test_exit(self):
        """Ошибочные аргументы не завершают сеанс."""
        shell = Shell()
        self.assertIn("Ошибка", shell.execute("exit extra"))
        self.assertTrue(shell.running)
        shell.execute("exit")
        self.assertFalse(shell.running)
