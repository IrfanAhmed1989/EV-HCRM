import sys, re
from pathlib import Path

# Read dal.py
src = Path("dal.py").read_text(encoding="utf-8")

# Find the entire connect() function block
m = re.search(r'def\s+connect\s*\([^)]*\):[\s\S]*?(?=\n\s*def\s+\w+\s*\(|\Z)', src)
if not m:
    print("❌ connect() not found in dal.py — aborting")
    sys.exit(1)

# New connect() implementation
new_func = (
'def connect():\n'
'    import json, os\n'
'    import mysql.connector as mc\n'
'    # Load config.json\n'
'    try:\n'
'        cfg = json.load(open("config.json","r"))\n'
'    except Exception as e:\n'
'        raise RuntimeError(f"Failed to read config.json: {e}")\n'
'\n'
'    # Prefer unix socket if provided or if /tmp/mysql.sock exists\n'
'    unix_socket = cfg.get("unix_socket")\n'
'    if not unix_socket and os.path.exists("/tmp/mysql.sock"):\n'
'        unix_socket = "/tmp/mysql.sock"\n'
'\n'
'    # Build connector kwargs\n'
'    kwargs = dict(\n'
'        user=cfg.get("user"),\n'
'        password=cfg.get("password"),\n'
'        database=cfg.get("database"),\n'
'    )\n'
'\n'
'    if unix_socket:\n'
'        kwargs["unix_socket"] = unix_socket\n'
'    else:\n'
'        kwargs["host"] = cfg.get("host", "127.0.0.1")\n'
'        kwargs["port"] = int(cfg.get("port", 3306))\n'
'\n'
'    return mc.connect(**kwargs)\n'
)

# Patch the file
patched = src[:m.start()] + new_func + src[m.end():]
Path("dal.py.bak_conn").write_text(src, encoding="utf-8")
Path("dal.py").write_text(patched, encoding="utf-8")

print("✅ Patched dal.py connect() | backup=dal.py.bak_conn")
