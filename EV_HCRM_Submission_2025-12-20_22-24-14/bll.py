
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
    
# === BLL runtime safety: correct DAL wiring and getters ===
try:
    from dal import DAL, ChargingSessionDAL, VehiclesDAL, TariffsDAL
except Exception as e:
    DAL = ChargingSessionDAL = VehiclesDAL = TariffsDAL = None

try:
    BLL
except NameError:
    pass
else:
    def _wire_dals(self):
        db = getattr(self, "db", None)
        if db is None and DAL is not None:
            dal = DAL()
            try:
                db = dal.connect()
                self.db = db
            except Exception:
                pass
        if db is not None:
            self._session_dal = getattr(self, "_session_dal", None) or ChargingSessionDAL(db)
            self._vehicles_dal = getattr(self, "_vehicles_dal", None) or VehiclesDAL(db)
            self._tariffs_dal = getattr(self, "_tariffs_dal", None) or TariffsDAL(db)

    if not hasattr(BLL, "_wire_dals"):
        BLL._wire_dals = _wire_dals

    def _get_vehicles(self):
        self._wire_dals()
        v = getattr(self, "_vehicles_dal", None)
        if v is None: return []
        fn = getattr(v, "get_vehicles", None) or getattr(v, "get_all", None)
        return fn() if fn else []

    if not hasattr(BLL, "get_vehicles"):
        BLL.get_vehicles = _get_vehicles

    def _get_tariffs(self):
        self._wire_dals()
        t = getattr(self, "_tariffs_dal", None)
        if t is None: return []
        fn = getattr(t, "get_tariffs", None) or getattr(t, "get_all", None)
        return fn() if fn else []

    if not hasattr(BLL, "get_tariffs"):
        BLL.get_tariffs = _get_tariffs

    def _get_sessions(self):
        self._wire_dals()
        sdal = getattr(self, "_session_dal", None)
        return sdal.get_all() if sdal and hasattr(sdal, "get_all") else []

    if not hasattr(BLL, "get_sessions"):
        BLL.get_sessions = _get_sessions

# === Force override BLL getters to use correct DALs (unconditional) ===
# Assumes DAL, ChargingSessionDAL, VehiclesDAL, TariffsDAL are imported earlier in bll.py.
def __bll_wire(self):
    db = getattr(self, "db", None)
    try:
        dal = DAL()
        if db is None:
            db = dal.connect()
            self.db = db
    except Exception:
        pass
    if db:
        self._session_dal = getattr(self, "_session_dal", None) or ChargingSessionDAL(db)
        self._vehicles_dal = getattr(self, "_vehicles_dal", None) or VehiclesDAL(db)
        self._tariffs_dal = getattr(self, "_tariffs_dal", None) or TariffsDAL(db)

def __bll_get_vehicles(self):
    __bll_wire(self)
    v = getattr(self, "_vehicles_dal", None)
    if not v: return []
    fn = getattr(v, "get_vehicles", None) or getattr(v, "get_all", None)
    return fn() if fn else []

def __bll_get_tariffs(self):
    __bll_wire(self)
    t = getattr(self, "_tariffs_dal", None)
    if not t: return []
    fn = getattr(t, "get_tariffs", None) or getattr(t, "get_all", None)
    return fn() if fn else []

def __bll_get_sessions(self):
    __bll_wire(self)
    sdal = getattr(self, "_session_dal", None)
    return sdal.get_all() if sdal and hasattr(sdal, "get_all") else []

# Unconditionally override any existing BLL methods
BLL._wire_dals = __bll_wire
BLL.get_vehicles = __bll_get_vehicles
BLL.get_tariffs = __bll_get_tariffs
BLL.get_sessions = __bll_get_sessions
