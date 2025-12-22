from bll import BLL
from datetime import datetime
b=BLL()
sd=datetime.strptime("2025-12-20 21:00:00","%Y-%m-%d %H:%M:%S")
ed=datetime.strptime("2025-12-20 22:15:00","%Y-%m-%d %H:%M:%S")
ok,msg=b.update_session("Tesla Model 3,2025-12-20,21:00:00", sd, ed, 34.2)
print("OK=", ok, "|", msg)
