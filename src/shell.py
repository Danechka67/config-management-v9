"""Парсер и команды оболочки, независимые от графического интерфейса."""
from datetime import datetime
import posixpath
from src.vfs import VFS
from src.removal import remove

DEFAULT_TAIL_LINES = 10
MIN_TAIL_LINES = 0


class Shell:
    """Хранит VFS, текущий каталог и состояние сеанса."""

    def __init__(self, vfs=None):
        """Создать активный сеанс с корневым текущим каталогом."""
        self.vfs = vfs if vfs is not None else VFS()
        self.running = True
        self.cwd = "/"
        self.commands = {"ls": self.ls, "cd": self.cd,
                         "date": self.date, "tail": self.tail,
                         "exit": self.exit, "rm": self.rm}

    def execute(self, line):
        """Разделить ввод по пробелам, выполнить команду, вернуть вывод."""
        parts = line.split()
        if not parts:
            return ""
        command, *args = parts
        handler = self.commands.get(command)
        if handler is None:
            return f"Ошибка: неизвестная команда: {command}"
        try:
            return handler(args)
        except (ValueError, UnicodeError) as error:
            return f"Ошибка: {error}"

    def ls(self, args):
        """Показать содержимое каталога или имя указанного файла."""
        if len(args) > 1:
            raise ValueError("использование: ls [путь]")
        path = self.vfs.resolve(args[0] if args else self.cwd, self.cwd)
        node = self.vfs.require(path)
        if node.kind == "file":
            return posixpath.basename(path)
        names = self.vfs.children(path)
        return "  ".join(name + ("/" if self.vfs.require(
            self.vfs.resolve(name, path)).kind == "dir" else "")
                         for name in names)

    def cd(self, args):
        """Перейти по пути; без аргументов перейти в корень VFS."""
        if len(args) > 1:
            raise ValueError("использование: cd [путь]")
        path = self.vfs.resolve(args[0] if args else "/", self.cwd)
        self.vfs.require(path, "dir")
        self.cwd = path
        return ""

    def date(self, args):
        """Показать локальное время ОС, используя необязательный формат."""
        if len(args) > 1 or (args and not args[0].startswith("+")):
            raise ValueError("использование: date [+формат]")
        pattern = args[0][1:] if args else "%Y-%m-%d %H:%M:%S %z"
        return datetime.now().astimezone().strftime(pattern)

    def tail(self, args):
        """Показать последние N строк UTF-8 файла из VFS."""
        count, name = self._tail_args(args)
        path = self.vfs.resolve(name, self.cwd)
        data = self.vfs.require(path, "file").data
        lines = data.decode("utf-8").splitlines()
        return "\n".join(lines[-count:]) if count else ""

    @staticmethod
    def _tail_args(args):
        """Разобрать tail ФАЙЛ или tail -n N ФАЙЛ."""
        if len(args) == 1 and not args[0].startswith("-"):
            return DEFAULT_TAIL_LINES, args[0]
        if len(args) != 3 or args[0] != "-n":
            raise ValueError("использование: tail [-n N] файл")
        try:
            count = int(args[1])
        except ValueError as error:
            raise ValueError("N должно быть целым числом") from error
        if count < MIN_TAIL_LINES:
            raise ValueError("N должно быть неотрицательным")
        return count, args[2]

    def exit(self, args):
        """Завершить сеанс, если аргументы отсутствуют."""
        if args:
            raise ValueError("exit не принимает аргументы")
        self.running = False
        return "Сеанс завершён"

    def rm(self, args):
        """Удалить файлы/деревья каталогов только в памяти."""
        return remove(self.vfs, self.cwd, args)
