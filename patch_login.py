from pathlib import Path

gui_p = Path("GUI.py")
gui = gui_p.read_text()

# 1. Remove old login block if appended at bottom
gui = gui.replace('root.withdraw()', '')
gui = gui.replace('root.deiconify()', '')

# 2. Inject login code BEFORE root = Tk()
inject_code = '''
import json
from pathlib import Path
import tkinter as tk
from tkinter import simpledialog

# Login prompts BEFORE main window
temp_root = tk.Tk()
temp_root.withdraw()
host = simpledialog.askstring("Login", "MySQL Host:", initialvalue="127.0.0.1")
user = simpledialog.askstring("Login", "MySQL User:", initialvalue="root")
password = simpledialog.askstring("Login", "MySQL Password:", show="*")
database = simpledialog.askstring("Login", "Database:", initialvalue="ev_hcrm")
cfg = {"host": host, "port": 3306, "user": user, "password": password, "database": database}
Path("config.json").write_text(json.dumps(cfg))
temp_root.destroy()
'''

gui = gui.replace('root = tk.Tk()', inject_code + '\nroot = tk.Tk()')

gui_p.write_text(gui)
print("✅ Login code repositioned BEFORE main window.")
