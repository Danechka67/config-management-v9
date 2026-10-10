@echo off
cd /d "%~dp0.."
python -m src.main --vfs examples/minimal.csv --startup examples/vfs.txt
python -m src.main --vfs examples/files.csv --startup examples/vfs.txt
python -m src.main --vfs examples/deep.csv --startup examples/vfs.txt
