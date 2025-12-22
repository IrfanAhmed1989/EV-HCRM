import inspect, datetime
from bll import BLL
b=BLL()
print("== Adaptive CRUD smoke ==")
names=["add_session","addsession","create_session","update_session","updatesession","delete_session","deletesession"]
C={"vehicle":"Chevy Bolt","vehicle_nickname":"Chevy Bolt","tariff":"Flat Rate","tariff_name":"Flat Rate","start_date":"2025-12-18","start_time":"08:00:00","end_date":"2025-12-18","end_time":"09:30:00","rate":2.50,"unit_rate":2.50,"price_per_kwh":2.50,"kwh_rate":2.50,"cost":3.20,"unit_cost":3.20,"kwh":11.0,"energy_kwh":11.0,"session_id":("Chevy Bolt","2025-12-18","08:00:00"),"sid":("Chevy Bolt","2025-12-18","08:00:00"),"start_dt":datetime.datetime(2025,12,18,8,0,0),"end_dt":datetime.datetime(2025,12,18,10,0,0)}
for n in names:
    m=getattr(b,n,None)
    print("--",n)
    if not m:
        print("not found"); continue
    sig=inspect.signature(m)
    print("signature:",sig)
    P=[p.name for p in sig.parameters.values() if p.name!="self"]
    KW={k:C[k] for k in P if k in C}
    try:
        r=m(**KW); print("OK:",r)
    except Exception as e:
        print("ERROR:",e)
print("== Done ==")
