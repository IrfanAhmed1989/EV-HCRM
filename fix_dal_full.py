from pathlib import Path
import re, textwrap

p = Path("dal.py")
src = p.read_text(encoding="utf-8")

# New, correctly indented Db class
db_class = textwrap.dedent("""
class Db:
    def __init__(self):
        self.conn = None

    def connect(self, host=None, port=None, user=None, password=None, database=None, unix_socket=None):
        import json, os
        import mysql.connector as mc

        # Load config.json if available
        cfg = {}
        try:
            cfg = json.load(open("config.json", "r"))
        except Exception:
            pass

        # Prefer unix socket if provided or if /tmp/mysql.sock exists
        if unix_socket is None and cfg.get("unix_socket") is None and os.path.exists("/tmp/mysql.sock"):
            unix_socket = "/tmp/mysql.sock"
        if unix_socket is None:
            unix_socket = cfg.get("unix_socket")

        # Resolve credentials
        user = user if user is not None else cfg.get("user")
        password = password if password is not None else cfg.get("password")
        database = database if database is not None else cfg.get("database")

        if unix_socket:
            kwargs = dict(user=user, password=password, database=database, unix_socket=unix_socket)
        else:
            host = host if host is not None else cfg.get("host", "127.0.0.1")
            port = port if port is not None else int(cfg.get("port", 3306))
            kwargs = dict(user=user, password=password, database=database, host=host, port=port)

        self.conn = mc.connect(**kwargs)
        return self.conn

    def cursor(self):
        if not self.conn or not getattr(self.conn, 'is_connected', lambda: False)():
            raise RuntimeError('Database not connected. Call Db.connect(...) first.')
        return self.conn.cursor(dictionary=True)

    def commit(self):
        if self.conn:
            self.conn.commit()

    def close(self):
        try:
            if self.conn:
                self.conn.close()
        except:
            pass
""").lstrip() + "\n"

# Replace existing Db class block from 'class Db' to next 'class' or EOF
m_db = re.search(r'^\s*class\s+Db\s*:\s*[\s\S]*?(?=^\s*class\s+\w+\s*:|\Z)', src, re.M)
if m_db:
    before = src[:m_db.start()]
    after = src[m_db.end():]
    src = before + db_class + after
else:
    src = db_class + src  # prepend if class not found

# Ensure top-level def connect() exists
if not re.search(r'^\s*def\s+connect\s*\(\s*\)\s*:', src, re.M):
    m_imports = re.search(r'^(?:import[^\n]*\n|from[^\n]*\n)+', src, re.M)
    insert_pos = m_imports.end() if m_imports else 0
    top_connect = textwrap.dedent("""
    def connect():
        db = Db()
        return db.connect()
    """).lstrip() + "\n"
    src = src[:insert_pos] + top_connect + src[insert_pos:]

# Write backup and file
Path("dal.py.bak_fullfix").write_text(p.read_text(encoding="utf-8"), encoding="utf-8")
p.write_text(src, encoding="utf-8")
print("✅ dal.py patched: Db class fixed + top-level connect() added | backup=dal.py.bak_fullfix")
