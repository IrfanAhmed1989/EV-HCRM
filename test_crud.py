from bll import BLL
from datetime import datetime, timedelta

b = BLL()
v = "Tesla Model 3"
t = "Flat Rate"

# Build set of existing SessionIDs to avoid duplicates
existing = set()
for r in b.get_sessions():
    s = str(r.get("Start", ""))
    parts = s.split()
    sdate = parts[0] if len(parts) > 0 else ""
    stime = parts[1] if len(parts) > 1 else ""
    existing.add(f"{r.get('Vehicle','')},{sdate},{stime}")

# Pick a unique future start time
sdt = datetime(2031, 1, 1, 1, 1, 1)
sid_str = f"{v},{sdt:%Y-%m-%d},{sdt:%H:%M:%S}"
while sid_str in existing:
    sdt += timedelta(minutes=1)
    sid_str = f"{v},{sdt:%Y-%m-%d},{sdt:%H:%M:%S}"
edt = sdt + timedelta(hours=1)

print("ADD:", *b.add_session(v, t, sdt, edt, 9.75))

# Use tuple form to avoid parsing issues: (Vehicle, StartDate, StartTime)
sid_tuple = (v, sdt.date(), sdt.time())
print("UPDATE:", *b.update_session(sid_tuple, sdt, edt + timedelta(minutes=30), 10.50))

print("DELETE:", *b.delete_session(sid_tuple))

print("ROWS AFTER:", lenprint("ROWS AFTER:", len(b.get_sessions()))
