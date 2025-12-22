#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"
if [ ! -d .venv ]; then
  python3 -m venv .venv
fi
. .venv/bin/activate
pip install -r requirements.txt
echo "Using Python: $(which python)"
python -m py_compile dal.py bll.py gui.py
python gui.py
