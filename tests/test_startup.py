"""Проверки последовательного исполнения скриптов."""
import tempfile
import unittest
from pathlib import Path
from src.config import parse_args
from src.shell import Shell
from src.startup import run_startup


class StartupTest(unittest.TestCase):
    """Ошибка команды не должна останавливать остальные строки."""

    def test_continue_and_exit(self):
        """После ошибки продолжать, после exit остановиться."""
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "startup.txt"
            path.write_text("unknown\nls\nexit\nunknown", encoding="utf-8")
            shell = Shell()
            output = []
            run_startup(path, shell,
                        lambda line: output.append(shell.execute(line)),
                        output.append)
        self.assertEqual(len(output), 3)
        self.assertIn("Ошибка", output[0])
        self.assertFalse(shell.running)

    def test_missing(self):
        """Недоступный скрипт возвращает сообщение об ошибке."""
        output = []
        run_startup(Path("missing-script.txt"), Shell(),
                    output.append, output.append)
        self.assertIn("Ошибка", output[0])

    def test_config(self):
        """Оба параметра передаются без потери значения."""
        args = parse_args(["--vfs", "a.csv", "--startup", "b.txt"])
        self.assertEqual(args.vfs, Path("a.csv"))
        self.assertEqual(args.startup, Path("b.txt"))
