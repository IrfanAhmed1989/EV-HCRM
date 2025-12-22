import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
from bll import BLL
import os

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("EV-HCRM")
        self.geometry("1000x600")
        self.resizable(True, True)

        # Status line
        self.status = tk.StringVar(value="Connecting to MySQL...")
        top = ttk.Frame(self, padding=8)
        top.pack(fill="x")
        ttk.Label(top, textvariable=self.status).pack(side="left")

        # Try BLL
        try:
            self.bll = BLL()
            self.status.set("✅ Connected")
        except Exception as e:
            self.bll = None
            self.status.set(f"❌ Failed to start BLL: {e}")
            ttk.Button(top, text="Close", command=self.destroy).pack(side="right", padx=8)
            return

        # Notebook with tabs
        nb = ttk.Notebook(self)
        nb.pack(fill="both", expand=True)

        # ---- Sessions tab ----
        self.tab_sessions = ttk.Frame(nb)
        nb.add(self.tab_sessions, text="Sessions")

        s_btns = ttk.Frame(self.tab_sessions, padding=8)
        s_btns.pack(fill="x")

        ttk.Button(s_btns, text="Refresh Sessions", command=self.refresh_sessions).pack(side="left", padx=4)
        ttk.Button(s_btns, text="Add Session", command=self.add_session_dialog).pack(side="left", padx=4)
        ttk.Button(s_btns, text="Delete Selected", command=self.delete_selected).pack(side="left", padx=4)

        s_cols = ("Vehicle","Tariff","Start","End","kWh","Cost")
        self.s_tree = ttk.Treeview(self.tab_sessions, columns=s_cols, show="headings")
        for c, w in zip(s_cols, (160,120,180,180,80,80)):
            self.s_tree.heading(c, text=c)
            self.s_tree.column(c, width=w, anchor="center")
        self.s_tree.pack(fill="both", expand=True, padx=8, pady=4)

        # ---- Monthly tab ----
        self.tab_monthly = ttk.Frame(nb)
        nb.add(self.tab_monthly, text="Monthly Statements")

        m_top = ttk.Frame(self.tab_monthly, padding=8)
        m_top.pack(fill="x")
        ttk.Button(m_top, text="Refresh Monthly", command=self.refresh_monthly).pack(side="left", padx=4)

        ttk.Label(m_top, text="Month (YYYY-MM):").pack(side="left", padx=(16,4))
        self.month_var = tk.StringVar()
        self.cbo_month = ttk.Combobox(m_top, textvariable=self.month_var, values=[], state="readonly", width=10)
        self.cbo_month.pack(side="left")

        ttk.Button(m_top, text="Export CSV", command=self.export_csv).pack(side="left", padx=4)
        ttk.Button(m_top, text="Export PDF", command=self.export_pdf).pack(side="left", padx=4)

        m_cols = ("First_Name","Last_Name","Nickname","BillingMonth","TotalSessions","Total_kWh","TotalCost")
        self.m_tree = ttk.Treeview(self.tab_monthly, columns=m_cols, show="headings")
        for c, w in zip(m_cols, (120,120,140,120,120,120,120)):
            self.m_tree.heading(c, text=c)
            self.m_tree.column(c, width=w, anchor="center")
        self.m_tree.pack(fill="both", expand=True, padx=8, pady=4)

        # Initial loads
        self.refresh_sessions()
        self.refresh_monthly()

    # ---------- Sessions ----------
    def refresh_sessions(self):
        try:
            rows = self.bll.get_sessions()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load sessions:\n{e}")
            return
        self.s_tree.delete(*self.s_tree.get_children())
        for r in rows:
            sid = r.get("SessionID","")
            self.s_tree.insert("", "end", iid=sid, values=(
                r.get("Vehicle",""),
                r.get("Tariff",""),
                str(r.get("Start","")),
                str(r.get("End","")),
                r.get("kWh",""),
                r.get("Cost",""),
            ))

    def add_session_dialog(self):
        d = tk.Toplevel(self)
        d.title("Add Charging Session")
        d.geometry("420x360")
        frm = ttk.Frame(d, padding=10)
        frm.pack(fill="both", expand=True)

        try:
            vehicles = self.bll.get_vehicles()
            tariffs = self.bll.get_tariffs()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load lists:\n{e}")
            d.destroy()
            return

        row = 0
        ttk.Label(frm, text="Vehicle").grid(row=row, column=0, sticky="e"); row+=1
        cbo_vehicle = ttk.Combobox(frm, values=vehicles, state="readonly"); 
        if vehicles: cbo_vehicle.current(0)
        cbo_vehicle.grid(row=row-1, column=1, sticky="w")

        ttk.Label(frm, text="Tariff").grid(row=row, column=0, sticky="e"); row+=1
        cbo_tariff = ttk.Combobox(frm, values=tariffs, state="readonly");
        if tariffs: cbo_tariff.current(0)
        cbo_tariff.grid(row=row-1, column=1, sticky="w")

        ttk.Label(frm, text="Start Date (YYYY-MM-DD)").grid(row=row, column=0, sticky="e"); row+=1
        ent_sdate = ttk.Entry(frm); ent_sdate.grid(row=row-1, column=1, sticky="w")

        ttk.Label(frm, text="Start Time (HH:MM:SS)").grid(row=row, column=0, sticky="e"); row+=1
        ent_stime = ttk.Entry(frm); ent_stime.grid(row=row-1, column=1, sticky="w")

        ttk.Label(frm, text="End Date (YYYY-MM-DD)").grid(row=row, column=0, sticky="e"); row+=1
        ent_edate = ttk.Entry(frm); ent_edate.grid(row=row-1, column=1, sticky="w")

        ttk.Label(frm, text="End Time (HH:MM:SS)").grid(row=row, column=0, sticky="e"); row+=1
        ent_etime = ttk.Entry(frm); ent_etime.grid(row=row-1, column=1, sticky="w")

        ttk.Label(frm, text="kWh").grid(row=row, column=0, sticky="e"); row+=1
        ent_kwh = ttk.Entry(frm); ent_kwh.grid(row=row-1, column=1, sticky="w")

        def save():
            v = cbo_vehicle.get().strip()
            t = cbo_tariff.get().strip()
            sdate = ent_sdate.get().strip()
            stime = ent_stime.get().strip()
            edate = ent_edate.get().strip()
            etime = ent_etime.get().strip()
            kwh_txt = ent_kwh.get().strip()
            try: kwh = float(kwh_txt)
            except: messagebox.showerror("Error", "kWh must be a number."); return
            try:
                sdt = datetime.strptime(f"{sdate} {stime}", "%Y-%m-%d %H:%M:%S")
                edt = datetime.strptime(f"{edate} {etime}", "%Y-%m-%d %H:%M:%S")
            except Exception as e:
                messagebox.showerror("Error", f"Invalid date/time:\n{e}"); return
            ok, msg = self.bll.add_session(v, t, sdt, edt, kwh)
            if ok:
                messagebox.showinfo("Success", msg); d.destroy(); self.refresh_sessions()
            else:
                messagebox.showerror("Error", msg)

        ttk.Button(frm, text="Save", command=save).grid(row=row, column=0, pady=12)
        ttk.Button(frm, text="Cancel", command=d.destroy).grid(row=row, column=1, pady=12)

    def delete_selected(self):
        sel = self.s_tree.selection()
        if not sel:
            messagebox.showwarning("No selection", "Select a session row first.")
            return
        sid = sel[0]
        try:
            ok, msg = self.bll.delete_session(sid)
        except Exception as e:
            messagebox.showerror("Error", f"Delete failed:\n{e}")
            return
        if ok:
            messagebox.showinfo("Success", msg)
            self.refresh_sessions()
        else:
            messagebox.showerror("Error", msg)

    # ---------- Monthly ----------
    def refresh_monthly(self):
        try:
            rows = self.bll.get_monthly()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load monthly statements:\n{e}")
            return
        self.m_tree.delete(*self.m_tree.get_children())
        months = []
        for r in rows:
            bm = r.get("BillingMonth","")
            self.m_tree.insert("", "end", values=(
                r.get("First_Name",""),
                r.get("Last_Name",""),
                r.get("Nickname",""),
                bm,
                r.get("TotalSessions",""),
                r.get("Total_kWh",""),
                r.get("TotalCost",""),
            ))
            if bm and bm not in months:
                months.append(bm)
        months.sort()
        self.cbo_month["values"] = months
        if months and not self.month_var.get():
            self.month_var.set(months[-1])  # latest

    def export_csv(self):
        month = self.month_var.get().strip()
        if not month:
            messagebox.showwarning("Select month", "Choose a month (YYYY-MM) first.")
            return
        filename = os.path.join(os.getcwd(), f"statement_{month}.csv")
        try:
            self.bll.export_monthly_csv(month, filename)
            messagebox.showinfo("CSV exported", f"Saved to:\n{filename}")
        except Exception as e:
            messagebox.showerror("Error", f"CSV export failed:\n{e}")

    def export_pdf(self):
        month = self.month_var.get().strip()
        if not month:
            messagebox.showwarning("Select month", "Choose a month (YYYY-MM) first.")
            return
        filename = os.path.join(os.getcwd(), f"statement_{month}.pdf")
        try:
            self.bll.export_monthly_pdf(month, filename)
            messagebox.showinfo("PDF exported", f"Saved to:\n{filename}")
        except Exception as e:
            messagebox.showerror("Error", f"PDF export failed:\n{e}")

def main():
    app = App()
    app.mainloop()

if __name__ == "__main__":
    main()
