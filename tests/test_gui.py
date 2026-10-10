"""Проверки связи GUI и оболочки без графического дисплея."""
import unittest
from unittest.mock import Mock, patch
from src.shell import Shell


class GuiTest(unittest.TestCase):
    """Проверяет заголовок, вывод и завершение с подменой виджетов."""

    @classmethod
    def setUpClass(cls):
        """Подменить только Tkinter, чтобы тесты работали без Tcl/Tk."""
        cls.modules = patch.dict("sys.modules", {
            "tkinter": Mock(), "tkinter.scrolledtext": Mock()})
        cls.modules.start()
        import importlib
        import sys
        sys.modules.pop("src.gui", None)
        cls.gui = importlib.import_module("src.gui")

    @classmethod
    def tearDownClass(cls):
        """Удалить тестовый модуль и восстановить настоящий Tkinter."""
        import sys
        sys.modules.pop("src.gui", None)
        cls.modules.stop()

    def test_title_and_input(self):
        """Заголовок содержит VFS, поле ввода привязано к Enter."""
        root = Mock()
        terminal = self.gui.Terminal(root, Shell(), "course")
        root.title.assert_called_with("Shell Emulator - VFS: course")
        terminal.entry.bind.assert_called_with("<Return>", terminal.submit)

    def test_echo_and_error(self):
        """Журнал показывает введённую строку и ошибку команды."""
        terminal = self.gui.Terminal(Mock(), Shell(), "demo")
        terminal.write = Mock()
        terminal.run_line("unknown")
        self.assertIn("/$ unknown", terminal.write.call_args_list[0].args)
        self.assertIn("Ошибка", terminal.write.call_args_list[1].args[0])

    def test_exit(self):
        """exit планирует закрытие окна."""
        root = Mock()
        terminal = self.gui.Terminal(root, Shell(), "demo")
        terminal.run_line("exit")
        self.assertFalse(terminal.shell.running)
        root.after.assert_called_with(150, root.destroy)
