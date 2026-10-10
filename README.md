# Эмулятор оболочки — вариант 9

Этап 1: GUI на Tkinter, парсер по пробелам, заглушки ls и cd, exit.
Запуск: `python -m src.main`. Требуется Python 3.10+ с Tkinter.
Тесты: `python -m unittest discover -s tests -v`.
Демонстрация: введите `ls /`, `cd /docs`, `unknown`, `exit extra`, `exit`.

Этап 2: `--vfs` и `--startup`; ошибки скрипта не останавливают последующие строки. Проверка параметров: `scripts/check_config.sh` или `.bat`.

Этап 3: CSV с колонками `path,type,content`; абсолютные пути, типы `dir`/`file`, содержимое файлов в base64. VFS не распаковывается. Примеры: minimal/files/deep.csv.

Этап 4: `ls [путь]`, `cd [путь]`, `date [+формат]`, `tail [-n N] файл`. Демонстрация: `python -m src.main --startup examples/commands.txt`.
