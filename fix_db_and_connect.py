import re
from pathlib import Path

p = Path("dal.py")
src = p.read_text(encoding="utf-8")

# Build a correct Db class body
db_class_fixed = (
"class Db:\n"
"    def __init__(self):\n"
"        self.conn = None\n"
"\n"
"    def connect(self, host=None, port=None, user=None, password=None, database=None, unix_socket=None):\n"
"        import json, os\n"
"        import mysql.connector as mc\n"
"\n"
"        # Load config.json if available\n"
"        cfg = {}\n"
"        try:\n"
"            cfg = json.load(open(\"config.json\", \"r\"))\n"
"        except Exception:\n"
"            pass\n"
"\n"
"        # Prefer unix socket if provided or if /tmp/mysql.sock exists\n"
"        if unix_socket is None and cfg.get(\"unix_socket\") is None and os.path.exists(\"/tmp/mysql.sock\"):\n"
"            unix_socket = \"/tmp/mysql.sock\"\n"
"        if unix_socket is None:\n"
"            unix_socket = cfg.get(\"unix_socket\")\n"
"\n"
"        # Resolve credentials\n"
"        user = user if user is not None else cfg.get(\"user\")\n"
"        password = password if password is not None else cfg.get(\"password\")\n"
"        database = database if database is not None else cfg.get(\"database\")\n"
"\n"
"        if unix_socket:\n"
"            kwargs = dict(user=user, password=password, database=database, unix_socket=unix_socket)\n"
"        else:\n"
"            host = host if host is not None else cfg.get(\"host\", \"127.0.0.1\")\n"
"            port = port if port is not None else int(cfg.get(\"port\", 3306))\n"
"            kwargs = dict(user=user, password=password, database=database, host=host, port=port)\n"
"\n"
"        self.conn = mc.connect(**kwargs)\n"
"        return self.conn\n"
"\n"
"    def cursor(self):\n"
"        if not self.conn or not getattr(self.conn, 'is_connected', lambda: False)():\n"
"            raise RuntimeError('Database not connected. Call Db.connect(...) first.')\n"
"        return self.conn.cursor(dictionary=True)\n"
"\n"
"    def commit(self):\n"
"        if self.conn:\n"
"            self.conn.commit()\n"
"\n"
"    def close(self):\n"
"        try:\n"
"            if self.conn:\n"
"                self.conn.close()\n"
"        except:\n"
"            pass\n"
)

# 1) Replace the entire Db class block (from 'class Db:' up to the next 'class ' or EOF)
m_db_start = re.search(r'^class\s+Db\s*:\s*', src, re.M)
m_next_class = re.search(r'^\s*class\s+\w+\s*:', src[m_db_start.end():], re.M) if m_db_start else None
if m_db_start:
    end_index = m_db_start.end() + (m_next_class.start() if m_next_class else len(src[m_db_start.end():]))
    before = src[:m_db_start.start()]
    after = src[end_index:]
    src = before + db_class_fixed + after
    replaced = True
else:
    replaced = False

# 2) Ensure a top-level function connect() exists; if absent, add it after the imports
has_top_connect = re.search(r'^\s*def\s+connect\s*\(', src, re.M) is not None
if not has_top_connect:
    # Find position after the first two import lines (heuristic)
    m_first_import_block = re.search(r'^(?:import\s+[^\n]+\n|from\s+[^\n]+\n)+', src, re.M)
    insert_pos = m_first_import_block.end() if m_first_import_block else 0
    top_connect = (
        "\n"
        "def connect():\n"
        "    db = Db()\n"
        "    return db.connect()\n"
        "\n"
    )
    src = src[:insert_pos] + top_connect + src[insert_pos:]

# Write backups and the patched file
Path("dal.py.bak_dbfix").write_text(p.read_text(encoding="utf-8"), encoding="utf-8")
p.write_text(src, encoding="utf-8")
print(\"✅ Patched Db class and ensured top-level connect() | backup=dal.py.bak_dbfix\")
