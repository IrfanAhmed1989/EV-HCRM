#!/usr/bin/env bash
set -euo pipefail

echo "==> Backup"
cp -p "ev_hcrm.sql" "ev_hcrm.sql.bak.$(date +%Y%m%d-%H%M%S)"

echo "==> Clean artifacts in file"
python3 - << 'PY'
import re
p = "ev_hcrm.sql"
with open(p, "r", encoding="utf-8") as f:
    s = f.read()
s = re.sub(r'VARCH\$', 'VARCHAR(40))', s)
s = (s.replace('&amp;gt;', '>')
       .replace('&amp;lt;', '<')
       .replace('&amp;amp;', '&')
       .replace('&gt;', '>')
       .replace('&lt;', '<')
       .replace('&amp;', '&'))
s = s.replace('```', '')
s = s.replace('\nvehicle by nickname (cascade removes its sessions)\n',
              '\n-- vehicle by nickname (cascade removes its sessions)\n')
with open(p, "w", encoding="utf-8") as f:
    f.write(s)
print("✅ Cleaned VARCH$, HTML entities, and code fences.")
PY

echo "==> Remove consecutive duplicate USE lines"
python3 - << 'PY'
p = "ev_hcrm.sql"
with open(p, "r", encoding="utf-8") as f:
    lines = f.readlines()
out, prev = [], ""
for line in lines:
    if line.strip() == "USE ev_hcrm;" and prev.strip() == "USE ev_hcrm;":
        prev = line
        continue
    out.append(line)
    prev = line
with open(p, "w", encoding="utf-8") as f:
    f.writelines(out)
print("✅ Removed consecutive duplicate USE ev_hcrm; lines.")
PY

echo "==> Reload into MySQL"
mysql -u root -p -D ev_hcrm < "ev_hcrm.sql"

echo "==> Verify procedures"
mysql -u root -p -D ev_hcrm -e "SHOW PROCEDURE STATUS WHERE Db='ev_hcrm'\G"
