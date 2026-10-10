"""Точка входа графического эмулятора."""
from src.config import parse_args
from src.shell import Shell
from src.startup import run_startup


def main():
    """Прочитать настройки, открыть GUI и выполнить стартовый скрипт."""
    args = parse_args()
    import tkinter as tk
    from src.gui import Terminal

    root = tk.Tk()
    shell = Shell()
    terminal = Terminal(root, shell, args.vfs.stem)
    terminal.write(f"VFS: {args.vfs}")
    terminal.write(f"Startup: {args.startup}")
    if args.startup:
        root.after(0, lambda: run_startup(
            args.startup, shell, terminal.run_line, terminal.write))
    root.mainloop()


if __name__ == "__main__":
    main()
