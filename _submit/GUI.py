
import tkinter as tk
from tkinter import messagebox, simpledialog
from pathlib import Path
import json

def make_config():
    temp = tk.Tk()
    temp.withdraw()
    host = simpledialog.askstring("Login", "MySQL Host:", initialvalue="127.0.0.1", parent=temp)
    user = simpledialog.askstring("Login", "MySQL User:", initialvalue="root", parent=temp)
    password = simpledialog.askstring("MySQL Password", "Enter password:", show="*", parent=temp)
    database = simpledialog.askstring("Login", "Database:", initialvalue="ev_hcrm", parent=temp)
    cfg = {
        "host": host or "127.0.0.1",
        "port": 3306,
        "user": user or "root",
        "password": password or "",
        "database": database or "ev_hcrm"
    }
    Path("config.json").write_text(json.dumps(cfg))
    temp.destroy()

def main():
    # Create/refresh config.json via prompts
    make_config()
    # Import BLL after config exists
    try:
        from BLL import BLL
        bll = BLL()
    except Exception as e:
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Startup Error",
            f"Failed to start BLL (packages or DB):\\n{e}\\n\\n"
            "Try in terminal:\\n"
            "  pip install mysql-connector-python reportlab fpdf\\n"
            "Also ensure MySQL database 'ev_hcrm' and stored procedures exist."
        )
        raise
    # Tiny window proving GUI works
    win = tk.Tk()
    win.title("EV-HCRM — Starter")
    tk.Label(win, text="GUI is alive! We will add tabs next.", font=("Arial", 12)).pack(padx=16, pady=12)
    tk.Button(win, text="Close", command=win.destroy).pack(pady=8)
    win.mainloop()

if __name__ == "__main__":
    main()
