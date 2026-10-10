#!/bin/sh
cd "$(dirname "$0")/.." || exit 1
python3 -m src.main --vfs examples/deep.csv
python3 -m src.main --vfs examples/deep.csv --startup examples/repl.txt
python3 -m src.main --vfs examples/deep.csv --startup examples/missing.txt
