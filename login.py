import json, os
print("Login — enter MySQL connection (defaults in brackets):")
host=input("Host [127.0.0.1]: ") or "127.0.0.1"
port=input("Port [3306]: ") or "3306"
user=input("User [root]: ") or "root"
password=input("Password [iiii]: ") or "iiii"
db=input("Database [ev_hcrm]: ") or "ev_hcrm"
cfg={"host":host,"port":int(port),"user":user,"password":password,"database":db}
open("config.json","w",encoding="utf-8").write(json.dumps(cfg))
print("✅ config.json updated:", cfg)
