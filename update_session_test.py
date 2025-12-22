from bll import BLL
from datetime import datetime
b = BLL()
sid = 'Tesla Model 3,2025-12-20,21:00:00'
sd = datetime.strptime('2025-12-20 21:00:00', '%Y-%m-%d %H:%M:%S')
ed = datetime.strptime('2025-12-20 22:30:00', '%Y-%m-%d %H:%M:%S')
ok, msg = b.update_session(sid, sd, ed, 36.5)
print("UPDATE:", ok, msg)
