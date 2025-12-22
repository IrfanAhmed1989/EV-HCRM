from pathlib import Path
t = Path("README.md").read_text(encoding="utf-8")
t = t.replace("GUI.py", "gui.py").replace("DAL.py", "dal.py").replace("BLL.py", "bll.py")
lines = t.splitlines()
# Remove duplicated socket notes (heuristic)
dedup = []
seen = set()
for ln in lines:
    key = ln.strip()
    if key in seen and ("Unix socket" in key or "127.0.0.1" in key or "mysql -u root -piiii" in key):
        continue
    seen.add(key)
    dedup.append(ln)
Path("README.md.bak").write_text(t, encoding="utf-8")
Path("README.md").write_text("\n".join(dedup), encoding="utf-8")
print("✅ README normalized (backup=README.md.bak)")
