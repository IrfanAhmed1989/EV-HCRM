
# BLL.py
from dal import DAL as Db
from dal import DAL as ChargingSessionDAL
from datetime import datetime
import json
from pathlib import Path
import csv
from fpdf import FPDF

class BLL:
    def get_monthly(self):
        return self._session_dal.get_monthly()

    def __init__(self):
        self._db = Db()
        cfg = json.loads(Path("config.json").read_text())
        self._db.connect(host=cfg["host"], port=cfg.get("port", 3306), user=cfg["user"], password=cfg["password"], database=cfg.get("database", "ev_hcrm"))
        self._session_dal = ChargingSessionDAL(self._db)

    def get_sessions(self):
        return self._session_dal.get_all()

    def add_session(self, vehicle_name, tariff_name, start_dt, end_dt, kwh):
        if end_dt <= start_dt:
            return False, "End time must be after start time."
        if kwh <= 0:
            return False, "kWh must be positive."
        success = self._session_dal.add_session(vehicle_name, tariff_name,
                                                start_dt.date(), start_dt.time(),
                                                end_dt.date(), end_dt.time(), kwh)
        return (True, "Session added successfully.") if success else (False, "Error adding session.")

    def update_session(self, session_id, start_dt, end_dt, kwh):
        if end_dt <= start_dt:
            return False, "End time must be after start time."
        success = self._session_dal.update_session(session_id,
                                                   start_dt.date(), start_dt.time(),
                                                   end_dt.date(), end_dt.time(), kwh)
        return (True, "Session updated.") if success else (False, "Update failed.")

    def delete_session(self, session_id):
        success = self._session_dal.delete_session(session_id)
        return (True, "Session deleted.") if success else (False, "Delete failed.")

    def export_monthly_csv(self, month, filename):
        sessions = [s for s in self.get_sessions() if str(s.get("Start", "")).startswith(month)]
        with open(filename, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["SessionID", "Vehicle", "Start", "End", "kWh", "Cost"])
            for s in sessions:
                writer.writerow([s.get("SessionID"), s.get("Vehicle"), s.get("Start"),
                                 s.get("End"), s.get("kWh"), s.get("Cost")])
        return True

    def export_monthly_pdf(self, month, filename):
        sessions = [s for s in self.get_sessions() if str(s.get("Start", "")).startswith(month)]
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, f"Monthly Statement for {month}", ln=True, align="C")
        pdf.ln(10)
        for s in sessions:
            pdf.cell(0, 10, f"{s.get('SessionID')} | {s.get('Vehicle')} | {s.get('Start')} | {s.get('End')} | {s.get('kWh')} kWh | {s.get('Cost')}", ln=True)
        pdf.output(filename)
        return True




    def get_vehicles(self):
        return self._session_dal.get_vehicles()

    def get_tariffs(self):
        return self._session_dal.get_tariffs()
    