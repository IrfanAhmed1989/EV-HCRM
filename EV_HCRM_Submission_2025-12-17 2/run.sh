#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"
PY=".venv/bin/python"
[ -x "$PY" ] || PY="python3"
echo "Using: $PY"
$PY -m py_compile dal.py bll.py gui.py 2>/dev/null || $PY -m py_compile dal.py bll.py GUI.py
$PY gui.py 2>/dev/null || $PY GUI.py
