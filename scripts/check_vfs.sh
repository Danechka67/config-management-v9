#!/bin/sh
cd "$(dirname "$0")/.." || exit 1
python3 -m src.main --vfs examples/minimal.csv --startup examples/vfs.txt
python3 -m src.main --vfs examples/files.csv --startup examples/vfs.txt
python3 -m src.main --vfs examples/deep.csv --startup examples/vfs.txt
