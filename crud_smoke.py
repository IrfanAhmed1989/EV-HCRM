from datetime import datetime
from bll import BLL
b=BLL()
sid=("Chevy Bolt","2025-12-18","08:00:00")
print("ADD:", *b.add_session("Chevy Bolt","Flat Rate","2025-12-18","08:00:00","2025-12-18","09:30:00",2.50))
print("UPDATE:", *b.update_session(sid, datetime(2025,12,18,8), datetime(2025,12,18,10), 3.20))
print("DELETE:", *b.delete_session(sid))
print("CRUD smoke done")
