
# BLL.py
from dal import DAL, ChargingSessionDAL, VehiclesDAL, TariffsDAL
from dal import DAL, ChargingSessionDAL, VehiclesDAL, TariffsDAL
from datetime import datetime
import json
from pathlib import Path
import csv
from fpdf import FPDF

class BLL:
    def __init__(self):
        from dal import DAL, ChargingSessionDAL, VehiclesDAL, TariffsDAL
        self._db = DAL()
        self._db.connect()
        self._session_dal = ChargingSessionDAL(self._db)
        self._vehicles_dal = VehiclesDAL(self._db)
        self._tariffs_dal = TariffsDAL(self._db)
    def get_monthly(self):
        return self._session_dal.get_monthly()

    def get_sessions(self):
        return self._session_dal.get_all()
    def add_session(self, vehicle_name, tariff_name, start_dt, end_dt, kwh):
        """Add a charging session with validation, via DAL (SP-first, SQL fallback)."""
        try:
            if kwh is None or float(kwh) <= 0:
                return False, "kWh must be > 0"
            if end_dt <= start_dt:
                return False, "End time must be after Start time"
            ok, msg = self._session_dal.add_session(vehicle_name, tariff_name, start_dt, end_dt, kwh)
            return ok, msg
        except Exception as e:
            return False, f"ADD failed: {e}" 
    def update_session(self, session_id, start_dt, end_dt, kwh):
        """Update a charging session with validation, via DAL (SP-first, SQL fallback)."""
        try:
            if kwh is None or float(kwh) <= 0:
                return False, "kWh must be > 0"
            if end_dt <= start_dt:
                return False, "End time must be after Start time"
            ok, msg = self._session_dal.update_session(session_id, start_dt, end_dt, kwh)
            return ok, msg
        except Exception as e:
            return False, f"UPDATE failed: {e}" 
    def delete_session(self, session_id):
        """Delete a charging session via DAL (SP-first, SQL fallback)."""
        try:
            ok, msg = self._session_dal.delete_session(session_id)
            return ok, msg
        except Exception as e:
            return False, f"DELETE failed: {e}"

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
    