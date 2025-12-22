import re, textwrap
from pathlib import Path

src_path = Path("dal.py")
src = src_path.read_text(encoding="utf-8")

# Find the existing connect() block robustly (multiline mode)
m = re.search(r'^def\s+connect\s*\([^)]*\):[\s\S]*?(?=^\s*def\s+\w+\s*\(|\Z)', src, re.M)
if not m:
    print("❌ connect() not found in dal.py — aborting")
    raise SystemExit(1)

# Clean, properly indented replacement function
new_func = textwrap.dedent("""
def connect():
    import json, os
    import mysql.connector as mc

    # Load config.json
    try:
        cfg = json.load(open("config.json", "r"))
    except Exception as e:
        raise RuntimeError(f"Failed to read config.json: {e}")

    # Prefer unix socket if provided or if /tmp/mysql.sock exists
    unix_socket = cfg.get("unix_socket")
    if not unix_socket and os.path.exists("/tmp/mysql.sock"):
        unix_socket = "/tmp/mysql.sock"

    # Build connector kwargs
    kwargs = dict(
        user=cfg.get("user"),
        password=cfg.get("password"),
        database=cfg.get("database"),
    )

    if unix_socket:
        kwargs["unix_socket"] = unix_socket
    else:
        kwargs["host"] = cfg.get("host", "127.0.0.1")
        kwargs["port"] = int(cfg.get("port", 3306))

    return mc.connect(**kwargs)
""").lstrip() + "\n"

patched = src[:m.start()] + new_func + src[m.end():]
Path("dal.py.bak_indent").write_text(src, encoding="utf-8")
src_path.write_text(patched, encoding="utf-8")

print("✅ Rewrote connect() with proper indentation | backup=dal.py.bak_indent")
