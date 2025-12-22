from pathlib import Path

gui_p = Path("GUI.py")
gui = gui_p.read_text()

# --- 1. Fix login injection indentation ---
inject_login = '''
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

gui = gui.replace('root = tk.Tk()', inject_login + '\nroot = tk.Tk()')

# --- 2. Replace text fields with Combobox ---
gui = gui.replace('vehicle_entry = tk.Entry(win, width=30)', 'vehicle_entry = ttk.Combobox(win, width=27, state="readonly")')
gui = gui.replace('tariff_entry = tk.Entry(win, width=30)', 'tariff_entry = ttk.Combobox(win, width=27, state="readonly")')

# --- 3. Inject dropdown population ---
inject_dropdowns = '''
# Populate dropdowns dynamically
try:
    from BLL import BLL
    bll = BLL()
    vehicles = [v.get("VehicleName") for v in bll._db.cursor().execute("SELECT VehicleName FROM vehicles") or []]
    tariffs = [t.get("TariffName") for t in bll._db.cursor().execute("SELECT TariffName FROM tariffs") or []]
    vehicle_entry["values"] = vehicles if vehicles else ["Chevy Bolt"]
    tariff_entry["values"] = tariffs if tariffs else ["Flat Rate"]
except Exception as e:
    messagebox.showerror("Dropdown Error", f"Failed to load dropdowns:\\n{e}")
'''

gui = gui.replace('vehicle_entry.insert(0, "Chevy Bolt")', inject_dropdowns)
gui = gui.replace('tariff_entry.insert(0, "Flat Rate")', '')

gui_p.write_text(gui)
print("✅ GUI.py patched: login fixed + dropdowns added.")
