from bll import BLL
from datetime import datetime
b = BLL()
before = len(b.get_sessions())
ok, msg = b.add_session(
    'Tesla Model 3',
    'Flat',
    datetime.strptime('2025-12-20 21:00:00', '%Y-%m-%d %H:%M:%S'),
    datetime.strptime('2025-12-20 22:15:00', '%Y-%m-%d %H:%M:%S'),
    34.2
)
after = len(b.get_sessions())
print("ADD:", ok, msg, "count:", before, "->", after)
