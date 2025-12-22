import json
import sys
import mysql.connector as mc
from pathlib import Path

# 1) Inspect dal.py for config usage and hard-coded creds
s = Path("dal.py").read_text(encoding="utf-8")
print("DAL references config.json:", ("config.json" in s))
print("Suspicious hard-coded patterns:", [p for p in ["user=", "password=", "host=", "port="] if p in s])

# 2) Load config.json
try:
    cfg = json.loads(Path("config.json").read_text(encoding="utf-8"))
    print("Loaded config.json:", cfg)
except Exception as e:
    print("ERROR reading config.json:", e)
    sys.exit(1)

# 3) Attempt live DB connection
try:
    con = mc.connect(host=cfg["host"], port=cfg["port"], user=cfg["user"], password=cfg["password"], database=cfg["database"])
    print("✅ DB connect OK")
    con.close()
except Exception as e:
    print("❌ DB connect FAILED:", e)
    sys.exit(1)
