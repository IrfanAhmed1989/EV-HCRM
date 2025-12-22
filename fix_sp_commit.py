from pathlib import Path
import re

p = Path("dal.py")
src = p.read_text(encoding="utf-8")

# Insert a commit after callproc() for add/update/delete if missing.
def add_commit_after_callproc(s):
    def repl(match):
        leading = match.group(1)  # indentation
        line = match.group(0)
        # If a commit already appears in the next few lines, keep as-is
        tail = s[match.end():match.end()+200]
        if re.search(r'\bcommit\s*\(', tail):
            return line
        return line + f"{leading}self.db.commit()\n"
    return re.sub(r'(^\s*)cur\.callproc\(\s*[\'"](?:addChargingSession|updateChargingSession|deleteChargingSession)[\'"]\s*,[^\n]*\)\s*\n',
                  repl, s, flags=re.M)

new_src = add_commit_after_callproc(src)

if new_src != src:
    Path("dal.py.bak_commitfix").write_text(src, encoding="utf-8")
    p.write_text(new_src, encoding="utf-8")
    print("✅ Inserted self.db.commit() after SP calls | backup=dal.py.bak_commitfix")
else:
    print("ℹ️ No changes made (commits already present or patterns not found).")
