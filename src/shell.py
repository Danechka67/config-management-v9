"""Парсер и обработчик команд, независимые от графического интерфейса."""


class Shell:
    """Хранит состояние сеанса и выполняет команды-заглушки."""

    def __init__(self):
        """Создать активный сеанс."""
        self.running = True
        self.cwd = "/"

    def execute(self, line):
        """Разделить строку по пробелам и вернуть вывод команды."""
        parts = line.split()
        if not parts:
            return ""
        command, *args = parts
        if command == "exit":
            if args:
                return "Ошибка: exit не принимает аргументы"
            self.running = False
            return "Сеанс завершён"
        if command in {"ls", "cd"}:
            return f"{command}: {args}"
        return f"Ошибка: неизвестная команда: {command}"
