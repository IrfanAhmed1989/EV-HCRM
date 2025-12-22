
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# Make sure Matplotlib uses Tk for windows
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Business Logic Layer
from BLL import BLL


class EVHCRMApp:
    def __init__(self, root):
self.root = root
self.root.title("EV Home Charging Reimbursement Manager")
self.bll = BLL()

        # Tabs
tab_control = ttk.Notebook(root)
self.sessions_tab = ttk.Frame(tab_control)
self.statements_tab = ttk.Frame(tab_control)
self.chart_tab = ttk.Frame(tab_control)
tab_control.add(self.sessions_tab, text="Sessions")
tab_control.add(self.statements_tab, text="Monthly Statements")
tab_control.add(self.chart_tab, text="Charts")
tab_control.pack(expand=1, fill="both")

        # Sessions Tab UI
self.tree = ttk.Treeview(
self.sessions_tab,
columns=("ID", "Vehicle", "Start", "End", "kWh", "Cost"),
show="headings",
height=12
)
for col in ("ID", "Vehicle", "Start", "End", "kWh", "Cost"):
self.tree.heading(col, text=col)
self.tree.column(col, anchor="center", width=120)
self.tree.pack(fill="both", expand=True)

btn_frame = ttk.Frame(self.sessions_tab)
btn_frame.pack(pady=6)
ttk.Button(btn_frame, text="Refresh", command=self.load_sessions).pack(side="left", padx=4)
ttk.Button(btn_frame, text="Add Session", command=self.add_session_dialog).pack(side="left", padx=4)
ttk.Button(btn_frame, text="Edit", command=self.edit_session_dialog).pack(side="left", padx=4)
ttk.Button(btn_frame, text="Delete", command=self.delete_session).pack(side="left", padx=4)

        # Statements Tab UI
tk.Label(self.statements_tab, text="Enter Month (YYYY-MM):").pack(pady=4)
self.month_entry = tk.Entry(self.statements_tab, width=20)
self.month_entry.pack(pady=4)
ttk.Button(self.statements_tab, text="Export CSV", command=self.export_csv).pack(pady=4)
ttk.Button(self.statements_tab, text="Export PDF", command=self.export_pdf).pack(pady=4)

        # Chart Tab UI
ttk.Button(self.chart_tab, text="Refresh Chart", command=self.show_chart).pack(pady=10)

        # Initial load
self.load_sessions()

    # -------- Sessions Tab Methods --------
    def load_sessions(self):
        # Clear current rows
for item in self.tree.get_children():
self.tree.delete(item)
try:
sessions = self.bll.get_sessions()
for s in sessions:
self.tree.insert(
"", "end",
values=(
s.get("SessionID", ""),
s.get("Vehicle", ""),
s.get("Start", ""),
s.get("End", ""),
s.get("kWh", ""),
s.get("Cost", "")
)
)
except Exception as e:
messagebox.showerror("Load Error", f"Failed to load sessions:\n{e}")

    def add_session_dialog(self):
self._session_dialog("Add Session")

    def edit_session_dialog(self):
selected = self.tree.selection()
if not selected:
messagebox.showwarning("Select Row", "Please select a session to edit.")
return
session_id = self.tree.item(selected[0])["values"][0]
self._session_dialog("Edit Session", session_id)

    def _session_dialog(self, title, session_id=None):
        # Simple dialog with defaults that match your sample data
win = tk.Toplevel(self.root)
win.title(title)
win.resizable(False, False)

        # Vehicle & Tariff (text inputs with defaults that exist in DB)
tk.Label(win, text="Vehicle Nickname").grid(row=0, column=0, padx=6, pady=4, sticky="e")
vehicle_entry = tk.Entry(win, width=30)
vehicle_entry.grid(row=0, column=1, padx=6, pady=4)
vehicle_entry.insert(0, "Chevy Bolt")  # exists from ev_hcrm.sql

tk.Label(win, text="Tariff Name").grid(row=1, column=0, padx=6, pady=4, sticky="e")
tariff_entry = tk.Entry(win, width=30)
tariff_entry.grid(row=1, column=1, padx=6, pady=4)
tariff_entry.insert(0, "Flat Rate")    # exists from ev_hcrm.sql

tk.Label(win, text="Start (YYYY-MM-DD HH:MM)").grid(row=2, column=0, padx=6, pady=4, sticky="e")
start_entry = tk.Entry(win, width=30)
start_entry.grid(row=2, column=1, padx=6, pady=4)

tk.Label(win, text="End (YYYY-MM-DD HH:MM)").grid(row=3, column=0, padx=6, pady=4, sticky="e")
end_entry = tk.Entry(win, width=30)
end_entry.grid(row=3, column=1, padx=6, pady=4)

tk.Label(win, text="kWh").grid(row=4, column=0, padx=6, pady=4, sticky="e")
kwh_entry = tk.Entry(win, width=30)
kwh_entry.grid(row=4, column=1, padx=6, pady=4)

        def submit():
try:
start_dt = datetime.strptime(start_entry.get().strip(), "%Y-%m-%d %H:%M")
end_dt = datetime.strptime(end_entry.get().strip(), "%Y-%m-%d %H:%M")
kwh = float(kwh_entry.get().strip())
veh = vehicle_entry.get().strip()
tar = tariff_entry.get().strip()

if session_id:
success, msg = self.bll.update_session(session_id, start_dt, end_dt, kwh)
else:
success, msg = self.bll.add_session(veh, tar, start_dt, end_dt, kwh)

messagebox.showinfo("Result", msg)
if success:
win.destroy()
self.load_sessions()
except Exception as e:
messagebox.showerror("Error", f"Failed:\n{e}")

ttk.Button(win, text="Submit", command=submit).grid(row=5, column=0, columnspan=2, pady=8)

    def delete_session(self):
selected = self.tree.selection()
if not selected:
messagebox.showwarning("Select Row", "Please select a session to delete.")
return
session_id = self.tree.item(selected[0])["values"][0]
success, msg = self.bll.delete_session(session_id)
messagebox.showinfo("Result", msg)
if success:
self.load_sessions()

    # -------- Statements Tab Methods --------
    def export_csv(self):
month = self.month_entry.get().strip()
if not month:
messagebox.showwarning("Input Required", "Enter month in YYYY-MM format.")
return
self.bll.export_monthly_csv(month, f"{month}_statement.csv")
messagebox.showinfo("Export", f"CSV exported as {month}_statement.csv")

    def export_pdf(self):
month = self.month_entry.get().strip()
if not month:
messagebox.showwarning("Input Required", "Enter month in YYYY-MM format.")
return
self.bll.export_monthly_pdf(month, f"{month}_statement.pdf")
messagebox.showinfo("Export", f"PDF exported as {month}_statement.pdf")

    # -------- Chart Tab Methods --------
    def show_chart(self):
try:
sessions = self.bll.get_sessions()
if not sessions:
messagebox.showinfo("No Data", "No sessions to chart yet.")
return

dates = [str(s.get("Start", "")).split()[0] for s in sessions]
            # Cost values come like "$12.34" -> strip and float
costs = []
for c in sessions:
cost_str = str(c.get("Cost", "0")).replace("$", "")
try:
costs.append(float(cost_str))
except ValueError:
costs.append(0.0)

fig, ax = plt.subplots(figsize=(6, 4))
ax.bar(dates, costs, color="#3a86ff")
ax.set_title("Cost per Session")
ax.set_ylabel("Cost ($)")
plt.setp(ax.get_xticklabels(), rotation=45, ha="right")
fig.tight_layout()

chart_win = tk.Toplevel(self.root)
chart_win.title("Cost Chart")
canvas = FigureCanvasTkAgg(fig, master=chart_win)
canvas.draw()
canvas.get_tk_widget().pack(fill="both", expand=True)

except Exception as e:
messagebox.showerror("Chart Error", f"Failed to render chart:\n{e}")

if __name__ == "__main__":
print("Starting EVHCRM GUI...")

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

root = tk.Tk()
app = EVHCRMApp(root)
root.mainloop()
import json
from pathlib import Path


host = tk.simpledialog.askstring("Login", "MySQL Host:", initialvalue="127.0.0.1")
user = tk.simpledialog.askstring("Login", "MySQL User:", initialvalue="root")
password = tk.simpledialog.askstring("Login", "MySQL Password:", show="*")
database = tk.simpledialog.askstring("Login", "Database:", initialvalue="ev_hcrm")
cfg = {"host": host, "port": 3306, "user": user, "password": password, "database": database}
Path("config.json").write_text(json.dumps(cfg))
