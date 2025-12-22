import json
from pathlib import Path
import tkinter as tk
from tkinter import simpledialog
import subprocess, sys

def main():
    temp_root = tk.Tk()
    temp_root.withdraw()

    host = simpledialog.askstring("Login", "MySQL Host:", initialvalue="127.0.0.1")
    user = simpledialog.askstring("Login", "MySQL User:", initialvalue="root")
    password = simpledialog.askstring("Login", "MySQL Password:", show="*", initialvalue="iiii")
    database = simpledialog.askstring("Login", "Database:", initialvalue="ev_hcrm")

    cfg = {"host": host, "port": 3306, "user": user, "password": password, "database": database}
    Path("config.json").write_text(json.dumps(cfg))

    temp_root.destroy()
    subprocess.run([sys.executable, "GUI.py"], check=False)

if __name__ == "__main__":
    main()
