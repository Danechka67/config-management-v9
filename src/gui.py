"""Графический терминал на Tkinter."""
import tkinter as tk
from tkinter.scrolledtext import ScrolledText


class Terminal:
    """Показывает диалог с оболочкой в одном окне."""

    def __init__(self, root, shell, name):
        """Настроить окно, журнал и поле ввода."""
        self.root = root
        self.shell = shell
        root.title(f"Shell Emulator - VFS: {name}")
        root.geometry("850x550")
        self.output = ScrolledText(root, state="disabled", wrap="word")
        self.output.pack(fill="both", expand=True, padx=10, pady=10)
        self.prompt = tk.Label(root, text="/$")
        self.prompt.pack(anchor="w", padx=10)
        self.entry = tk.Entry(root, font=("Courier", 12))
        self.entry.pack(fill="x", padx=10, pady=(0, 10))
        self.entry.bind("<Return>", self.submit)
        self.entry.focus_set()

    def write(self, text):
        """Добавить текст в журнал терминала."""
        if not text:
            return
        self.output.configure(state="normal")
        self.output.insert("end", text + "\n")
        self.output.configure(state="disabled")
        self.output.see("end")

    def submit(self, event=None):
        """Выполнить введённую строку и очистить поле ввода."""
        line = self.entry.get()
        self.entry.delete(0, "end")
        self.run_line(line)

    def run_line(self, line):
        """Показать ввод, вывод и новое приглашение."""
        self.write(f"{self.shell.cwd}$ {line}")
        self.write(self.shell.execute(line))
        self.prompt.configure(text=f"{self.shell.cwd}$")
        if not self.shell.running:
            self.root.after(150, self.root.destroy)
