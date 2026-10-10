"""Настройки запуска, получаемые из командной строки."""
import argparse
from pathlib import Path


def parse_args(argv=None):
    """Прочитать путь CSV и необязательный стартовый скрипт."""
    parser = argparse.ArgumentParser(description="Shell GUI, variant 9")
    parser.add_argument("--vfs", type=Path,
                        default=Path("examples/deep.csv"),
                        help="путь к CSV виртуальной файловой системы")
    parser.add_argument("--startup", type=Path,
                        help="путь к текстовому стартовому скрипту")
    return parser.parse_args(argv)
