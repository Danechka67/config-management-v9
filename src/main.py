"""Точка входа графического эмулятора."""
import tkinter as tk
from src.gui import Terminal
from src.shell import Shell


def main():
    """Открыть графическое окно REPL."""
    root = tk.Tk()
    Terminal(root, Shell(), "demo")
    root.mainloop()


if __name__ == "__main__":
    main()
