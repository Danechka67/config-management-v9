@echo off
cd /d "%~dp0.."
python -m src.main --vfs examples/deep.csv
python -m src.main --vfs examples/deep.csv --startup examples/repl.txt
python -m src.main --vfs examples/deep.csv --startup examples/missing.txt
