import tkinter as tk
try:
    from tkcalendar import DateEntry
except Exception:
    DateEntry=None
from tkinter import ttk, messagebox
import json
from datetime import datetime
import os

# BLL import (DAL reads config.json)
from bll import BLL

APP_TITLE = "EV-HCRM — Home Charging Reimbursement Manager"

def ensure_config_written(cfg):
    """Write config.json with provided DB settings."""
    try:
        with open("config.json", "w", encoding="utf-8") as f:
            json.dump(cfg, f, indent=2)
        return True, "config.json updated"
    except Exception as e:
        return False, f"Failed to write config.json: {e}"

def parse_time_from_spin(h_spin, m_spin, s_spin):
    try:
        h = int(h_spin.get()); m = int(m_spin.get()); s = int(s_spin.get())
        if not (0 <= h <= 23 and 0 <= m <= 59 and 0 <= s <= 59):
            raise ValueError("Out of range")
        return f"{h:02d}:{m:02d}:{s:02d}"
    except Exception:
        return None

def parse_date_from_entry(entry):
    try:
        raw = entry.get().strip()
        datetime.strptime(raw, "%Y-%m-%d")  # validate
        return raw
    except Exception:
        return None

class LoginFrame(ttk.Frame):
    """Collect DB settings, write config.json, build BLL."""
    def __init__(self, master, on_connected_cb):
        super().__init__(master)
        self.on_connected_cb = on_connected_cb

        self.columnconfigure(1, weight=1)
        ttk.Label(self, text="Database Login", font=("Segoe UI", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=(10, 10))

        # Defaults; prefill from existing config.json if present
        self.host = tk.StringVar(value="localhost")
        self.port = tk.StringVar(value="3306")
        self.user = tk.StringVar(value="root")
        self.password = tk.StringVar(value="")
        self.database = tk.StringVar(value="ev_hcrm")
        self.socket = tk.StringVar(value="/tmp/mysql.sock")  # macOS default; leave blank to force TCP

        if os.path.exists("config.json"):
            try:
                cfg = json.load(open("config.json"))
                self.host.set(cfg.get("host", "localhost"))
                self.port.set(str(cfg.get("port", "3306")))
                self.user.set(cfg.get("user", "root"))
                self.password.set(cfg.get("password", ""))
                self.database.set(cfg.get("database", "ev_hcrm"))
                self.socket.set(cfg.get("unix_socket", "/tmp/mysql.sock") or "")
            except Exception:
                pass

        row = 1
        ttk.Label(self, text="Host").grid(row=row, column=0, sticky="e", padx=6, pady=4); ttk.Entry(self, textvariable=self.host).grid(row=row, column=1, sticky="ew", padx=6, pady=4); row+=1
        ttk.Label(self, text="Port").grid(row=row, column=0, sticky="e", padx=6, pady=4); ttk.Entry(self, textvariable=self.port).grid(row=row, column=1, sticky="ew", padx=6, pady=4); row+=1
        ttk.Label(self, text="User").grid(row=row, column=0, sticky="e", padx=6, pady=4); ttk.Entry(self, textvariable=self.user).grid(row=row, column=1, sticky="ew", padx=6, pady=4); row+=1
        ttk.Label(self, text="Password").grid(row=row, column=0, sticky="e", padx=6, pady=4); ttk.Entry(self, show="*", textvariable=self.password).grid(row=row, column=1, sticky="ew", padx=6, pady=4); row+=1
        ttk.Label(self, text="Database").grid(row=row, column=0, sticky="e", padx=6, pady=4); ttk.Entry(self, textvariable=self.database).grid(row=row, column=1, sticky="ew", padx=6, pady=4); row+=1
        ttk.Label(self, text="Unix Socket (macOS)").grid(row=row, column=0, sticky="e", padx=6, pady=4); ttk.Entry(self, textvariable=self.socket).grid(row=row, column=1, sticky="ew", padx=6, pady=4); row+=1

        self.status = ttk.Label(self, text="Not connected", foreground="red")
        self.status.grid(row=row, column=0, columnspan=2, pady=(8, 8)); row+=1

        ttk.Button(self, text="Connect", command=self.do_connect).grid(row=row, column=0, columnspan=2, pady=(8, 12))

    def do_connect(self):
        # Build config from inputs and write to config.json
        sock_val = self.socket.get().strip()
        cfg = {
            "host": self.host.get().strip(),
            "port": int(self.port.get().strip() or "3306"),
            "user": self.user.get().strip(),
            "password": self.password.get(),
            "database": self.database.get().strip(),
            "unix_socket": sock_val if sock_val else None
        }
        ok, msg = ensure_config_written(cfg)
        if not ok:
            self.status.config(text=msg, foreground="red")
            messagebox.showerror("Config Error", msg)
            return

        # Try to create BLL (DAL will read config.json)
        try:
            bll = BLL()
            _ = bll.get_vehicles()  # sanity call
            self.status.config(text="Connected", foreground="green")
            self.on_connected_cb(bll)
        except Exception as e:
            self.status.config(text="Connection failed", foreground="red")
            messagebox.showerror("Connection Failed", f"Could not connect:\n{e}")

class SessionsTab(ttk.Frame):
    """Sessions grid with Add / Update / Delete and date/time pickers."""
    def __init__(self, master, bll):
        super().__init__(master)
        self.bll = bll

        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        form = ttk.LabelFrame(self, text="Session Details")
        form.grid(row=0, column=0, sticky="ew", padx=8, pady=8)
        for i in range(8):
            form.columnconfigure(i, weight=1)

        # Vehicle & Tariff
        ttk.Label(form, text="Vehicle").grid(row=0, column=0, sticky="e", padx=4, pady=4)
        self.vehicle_cb = ttk.Combobox(form, values=self.bll.get_vehicles())
        self.vehicle_cb.grid(row=0, column=1, sticky="ew", padx=4, pady=4)

        ttk.Label(form, text="Tariff").grid(row=0, column=2, sticky="e", padx=4, pady=4)
        self.tariff_cb = ttk.Combobox(form, values=self.bll.get_tariffs())
        self.tariff_cb.grid(row=0, column=3, sticky="ew", padx=4, pady=4)

        # Start Date/Time pickers (Entry + Spinboxes)
        ttk.Label(form, text="Start Date (YYYY-MM-DD)").grid(row=1, column=0, sticky="e", padx=4, pady=4)
        self.start_date = ttk.Entry(form); self.start_date.grid(row=1, column=1, sticky="ew", padx=4, pady=4)
        self.start_date.insert(0, datetime.now().strftime("%Y-%m-%d"))

        ttk.Label(form, text="Start Time (H:M:S)").grid(row=1, column=2, sticky="e", padx=4, pady=4)
        self.start_h = tk.Spinbox(form, from_=0, to=23, width=4)
        self.start_m = tk.Spinbox(form, from_=0, to=59, width=4)
        self.start_s = tk.Spinbox(form, from_=0, to=59, width=4)
        self.start_h.grid(row=1, column=3, sticky="w", padx=2); self.start_m.grid(row=1, column=4, sticky="w", padx=2); self.start_s.grid(row=1, column=5, sticky="w", padx=2)
        self.start_h.delete(0, tk.END); self.start_h.insert(0, "21")
        self.start_m.delete(0, tk.END); self.start_m.insert(0, "00")
        self.start_s.delete(0, tk.END); self.start_s.insert(0, "00")

        # End Date/Time pickers
        ttk.Label(form, text="End Date (YYYY-MM-DD)").grid(row=2, column=0, sticky="e", padx=4, pady=4)
        self.end_date = ttk.Entry(form); self.end_date.grid(row=2, column=1, sticky="ew", padx=4, pady=4)
        self.end_date.insert(0, datetime.now().strftime("%Y-%m-%d"))

        ttk.Label(form, text="End Time (H:M:S)").grid(row=2, column=2, sticky="e", padx=4, pady=4)
        self.end_h = tk.Spinbox(form, from_=0, to=23, width=4)
        self.end_m = tk.Spinbox(form, from_=0, to=59, width=4)
        self.end_s = tk.Spinbox(form, from_=0, to=59, width=4)
        self.end_h.grid(row=2, column=3, sticky="w", padx=2); self.end_m.grid(row=2, column=4, sticky="w", padx=2); self.end_s.grid(row=2, column=5, sticky="w", padx=2)
        self.end_h.delete(0, tk.END); self.end_h.insert(0, "22")
        self.end_m.delete(0, tk.END); self.end_m.insert(0, "15")
        self.end_s.delete(0, tk.END); self.end_s.insert(0, "00")

        ttk.Label(form, text="kWh").grid(row=3, column=0, sticky="e", padx=4, pady=4)
        self.kwh_entry = ttk.Entry(form); self.kwh_entry.grid(row=3, column=1, sticky="ew", padx=4, pady=4)
        self.kwh_entry.insert(0, "34.2")

        ttk.Button(form, text="Add", command=self.do_add).grid(row=3, column=3, padx=4, pady=4)
        ttk.Button(form, text="Update", command=self.do_update).grid(row=3, column=4, padx=4, pady=4)
        ttk.Button(form, text="Delete", command=self.do_delete).grid(row=3, column=5, padx=4, pady=4)

        # Sessions grid
        self.tree = ttk.Treeview(self, columns=("Vehicle", "Tariff", "Start", "End", "kWh", "Cost"), show="headings", height=12)
        for col in ("Vehicle", "Tariff", "Start", "End", "kWh", "Cost"):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=140 if col in ("Vehicle","Tariff") else 160, anchor="center")
        self.tree.grid(row=1, column=0, sticky="nsew", padx=8, pady=8)

        self.refresh()

    def refresh(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        try:
            rows = self.bll.get_sessions()
            for r in rows:
                self.tree.insert("", "end", values=(r.get("Vehicle"), r.get("Tariff"), r.get("Start"), r.get("End"), r.get("kWh"), r.get("Cost")))
        except Exception as e:
            messagebox.showerror("Load Error", f"Failed to load sessions:\n{e}")

    def _current_selection_sid(self):
        item = self.tree.selection()
        if not item:
            return None
        vals = self.tree.item(item[0], "values")
        vehicle = vals[0]
        start = vals[2]  # 'YYYY-MM-DD HH:MM:SS'
        date_part, time_part = start.split(" ")
        return f"{vehicle},{date_part},{time_part}"

    def do_add(self):
        vehicle = (self.vehicle_cb.get() or "").strip()
        tariff = (self.tariff_cb.get() or "").strip()
        sd = parse_date_from_entry(self.start_date)
        st = parse_time_from_spin(self.start_h, self.start_m, self.start_s)
        ed = parse_date_from_entry(self.end_date)
        et = parse_time_from_spin(self.end_h, self.end_m, self.end_s)
        try:
            kwh = float(self.kwh_entry.get())
        except Exception:
            messagebox.showerror("Input Error", "kWh must be a number")
            return

        if not vehicle or not tariff or not sd or not st or not ed or not et:
            messagebox.showerror("Input Error", "Please fill Vehicle, Tariff, Start/End date & time correctly.")
            return

        try:
            from_dt = datetime.strptime(f"{sd} {st}", "%Y-%m-%d %H:%M:%S")
            to_dt = datetime.strptime(f"{ed} {et}", "%Y-%m-%d %H:%M:%S")
            ok, msg = self.bll.add_session(vehicle, tariff, from_dt, to_dt, kwh)
            if ok:
                messagebox.showinfo("Add", f"✅ {msg}")
                self.refresh()
            else:
                messagebox.showerror("Add Failed", f"❌ {msg}")
        except Exception as e:
            messagebox.showerror("Add Failed", f"{e}")

    def do_update(self):
        sid = self._current_selection_sid()
        if not sid:
            messagebox.showwarning("Update", "Select a session row first.")
            return

        # Read end date/time and kWh from pickers
        ed = parse_date_from_entry(self.end_date)
        et = parse_time_from_spin(self.end_h, self.end_m, self.end_s)
        try:
            kwh = float(self.kwh_entry.get())
        except Exception:
            messagebox.showerror("Input Error", "kWh must be a number")
            return
        if not ed or not et:
            messagebox.showerror("Input Error", "End date/time invalid.")
            return

        # Original start datetime from selected row
        try:
            start_str = self.tree.item(self.tree.selection()[0], "values")[2]
            sd_dt = datetime.strptime(start_str, "%Y-%m-%d %H:%M:%S")
            ed_dt = datetime.strptime(f"{ed} {et}", "%Y-%m-%d %H:%M:%S")
        except Exception as e:
            messagebox.showerror("Update Failed", f"Bad date/time: {e}")
            return

        try:
            ok, msg = self.bll.update_session(sid, sd_dt, ed_dt, kwh)
            if ok:
                messagebox.showinfo("Update", f"✅ {msg}")
                self.refresh()
            else:
                messagebox.showerror("Update Failed", f"❌ {msg}")
        except Exception as e:
            messagebox.showerror("Update Failed", f"{e}")

    def do_delete(self):
        sid = self._current_selection_sid()
        if not sid:
            messagebox.showwarning("Delete", "Select a session row first.")
            return
        if not messagebox.askyesno("Confirm Delete", f"Delete session:\n{sid}?"):
            return
        try:
            ok, msg = self.bll.delete_session(sid)
            if ok:
                messagebox.showinfo("Delete", f"✅ {msg}")
                self.refresh()
            else:
                messagebox.showerror("Delete Failed", f"❌ {msg}")
        except Exception as e:
            messagebox.showerror("Delete Failed", f"{e}")

class StatementsTab(ttk.Frame):
    def __init__(self, master, bll):
        super().__init__(master)
        self.bll = bll

        box = ttk.LabelFrame(self, text="Monthly Statement")
        box.pack(fill="x", padx=8, pady=8)

        ttk.Label(box, text="Month (YYYY-MM)").grid(row=0, column=0, sticky="e", padx=6, pady=6)
        self.month = ttk.Entry(box); self.month.grid(row=0, column=1, sticky="w", padx=6, pady=6)
        self.month.insert(0, datetime.now().strftime("%Y-%m"))

        ttk.Button(box, text="Export CSV", command=self.export_csv).grid(row=0, column=2, padx=6, pady=6)
        ttk.Button(box, text="Export PDF", command=self.export_pdf).grid(row=0, column=3, padx=6, pady=6)

    def export_csv(self):
        m = self.month.get().strip()
        try:
            ok, msg = self.bll.export_monthly_csv(m, f"statement_{m}.csv")
            if ok:
                messagebox.showinfo("CSV", f"✅ {msg}")
            else:
                messagebox.showerror("CSV Failed", f"❌ {msg}")
        except Exception as e:
            messagebox.showerror("CSV Failed", f"{e}")

    def export_pdf(self):
        m = self.month.get().strip()
        try:
            ok, msg = self.bll.export_monthly_pdf(m, f"statement_{m}.pdf")
            if ok:
                messagebox.showinfo("PDF", f"✅ {msg}")
            else:
                messagebox.showerror("PDF Failed", f"❌ {msg}")
        except Exception as e:
            messagebox.showerror("PDF Failed", f"{e}")

class MainFrame(ttk.Frame):
    def __init__(self, master, bll):
        super().__init__(master)
        self.bll = bll
        self.pack(fill="both", expand=True)

        topbar = ttk.Frame(self); topbar.pack(fill="x")
        self.status_dot = ttk.Label(topbar, text="● Connected", foreground="green"); self.status_dot.pack(side="left", padx=8, pady=4)

        nb = ttk.Notebook(self); nb.pack(fill="both", expand=True, padx=6, pady=6)
        self.sessions_tab = SessionsTab(nb, self.bll)
        self.statements_tab = StatementsTab(nb, self.bll)
        nb.add(self.sessions_tab, text="Sessions")
        nb.add(self.statements_tab, text="Monthly Statements")

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry("980x640")
        self._container = ttk.Frame(self); self._container.pack(fill="both", expand=True)
        self.show_login()

    def show_login(self):
        for w in self._container.winfo_children():
            w.destroy()
        self.login = LoginFrame(self._container, on_connected_cb=self.show_main)
        self.login.pack(fill="both", expand=True)

    def show_main(self, bll):
        for w in self._container.winfo_children():
            w.destroy()
        self.main = MainFrame(self._container, bll)

def main():
    app = App()
    app.mainloop()

if __name__ == "__main__":
    main()
