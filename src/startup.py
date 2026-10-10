"""Выполнение стартового скрипта с продолжением после ошибок."""


def run_startup(path, shell, emit, write):
    """Показать и выполнить строки; после exit прекратить выполнение."""
    try:
        lines = path.read_text(encoding="utf-8-sig").splitlines()
    except (OSError, UnicodeError) as error:
        write(f"Ошибка чтения стартового скрипта: {error}")
        return
    for line in lines:
        if not shell.running:
            break
        emit(line)
