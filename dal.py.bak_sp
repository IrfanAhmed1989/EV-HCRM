import mysql.connector
from datetime import datetime
def connect():
    """Create a MySQL connection using config.json.
    Prefers Unix socket (/tmp/mysql.sock) if present; otherwise TCP (host, port)."""
    import os, json, mysql.connector
    cfg_path = "config.json"
    if not os.path.exists(cfg_path):
        raise FileNotFoundError("config.json not found. Please run GUI login to create it.")
    cfg = json.load(open(cfg_path, "r", encoding="utf-8"))
    user = cfg.get("user") or cfg.get("username") or "root"
    password = cfg.get("password") or ""
    database = cfg.get("database") or "ev_hcrm"
    host = cfg.get("host") or "localhost"
    port = int(cfg.get("port") or 3306)
    unix_socket = cfg.get("unix_socket") or "/tmp/mysql.sock"

    try:
        if unix_socket and os.path.exists(unix_socket):
            conn = mysql.connector.connect(user=user, password=password, database=database, unix_socket=unix_socket)
        else:
            conn = mysql.connector.connect(user=user, password=password, database=database, host=host, port=port)
        return conn
    except mysql.connector.Error:
        # Final fallback: try TCP once more
        conn = mysql.connector.connect(user=user, password=password, database=database, host=host, port=port)
        return conn

class DAL:
    def __init__(self, config_path=None):
        self.config_path = config_path or 'config.json'
        self.db = None

    def connect(self):
        """Instance connection using same logic as global connect()."""
        import os, json, mysql.connector
        cfg_path = getattr(self, "config_path", None) or "config.json"
        if not os.path.exists(cfg_path):
            raise FileNotFoundError("config.json not found. Please run GUI login to create it.")
        cfg = json.load(open(cfg_path, "r", encoding="utf-8"))
        user = cfg.get("user") or cfg.get("username") or "root"
        password = cfg.get("password") or ""
        database = cfg.get("database") or "ev_hcrm"
        host = cfg.get("host") or "localhost"
        port = int(cfg.get("port") or 3306)
        unix_socket = cfg.get("unix_socket") or "/tmp/mysql.sock"

        try:
            if unix_socket and os.path.exists(unix_socket):
                self.db = mysql.connector.connect(user=user, password=password, database=database, unix_socket=unix_socket)
            else:
                self.db = mysql.connector.connect(user=user, password=password, database=database, host=host, port=port)
        except mysql.connector.Error:
            # Final fallback to TCP
            self.db = mysql.connector.connect(user=user, password=password, database=database, host=host, port=port)
        return self.db

class ChargingSessionDAL:
    def __init__(self, core):
        # Accept DAL or raw connection; resolve to connection
        self.db = getattr(core, "db", None)
        if not self.db and hasattr(core, "connect"):
            try:
                self.db = core.connect()
            except Exception:
                pass
        if not self.db:
            self.db = core


    def add_session(self, vehicle, tariff, start_dt, end_dt, kwh):
        sd, st = start_dt.date(), start_dt.time()
        ed, et = end_dt.date(), end_dt.time()
        cur = self.db.cursor()
        try:
            # Prefer stored procedure
            cur.callproc("addChargingSession", [vehicle, tariff, sd, st, ed, et, kwh])
            self.db.commit()
            return True, "Session added successfully."
        except Exception as e:
            try:
                # Fallback direct INSERT
                sql = ("INSERT INTO charging_sessions (VehicleID, TariffID, StartDate, StartTime, EndDate, EndTime, kWh) "
                       "SELECT v.VehicleID, t.TariffID, %s, %s, %s, %s, %s "
                       "FROM vehicles v JOIN tariffs t ON t.Name = %s "
                       "WHERE TRIM(v.Nickname) = TRIM(%s)")
                cur.execute(sql, (sd, st, ed, et, kwh, tariff, vehicle))
                self.db.commit()
                return True, "Session added via fallback."
            except Exception:
                try:
                    self.db.rollback()
                except Exception:
                    pass
                return False, f"ADD failed: {e}"
        finally:
            try:
                cur.close()
            except Exception:
                pass

    def update_session(self, session_id, start_dt, end_dt, kwh):
        # session_id format: "Vehicle Nickname,YYYY-MM-DD,HH:MM:SS"
        try:
            vehicle, sd_str, st_str = session_id.rsplit(",", 2)
        except Exception:
            return False, "Bad session_id format."
        vehicle = vehicle.strip()
        sd = sd_str.strip()
        st = st_str.strip()
        cur = self.db.cursor()
        try:
            # Prefer stored procedure
            try:
                cur.callproc("updateChargingSession", [vehicle, start_dt.date(), start_dt.time(), end_dt.date(), end_dt.time(), kwh])
                self.db.commit()
                return True, "Session updated."
            except Exception as e:
                # Fallback direct UPDATE
                try:
                    # Resolve VehicleID
                    cur.execute("SELECT VehicleID FROM vehicles WHERE TRIM(Nickname)=TRIM(%s)", (vehicle,))
                    row = cur.fetchone()
                    if not row:
                        return False, "Vehicle not found."
                    vid = row[0] if isinstance(row,(tuple,list)) else (row.get("VehicleID") if isinstance(row,dict) else row)
                    cur.execute(
                        "UPDATE charging_sessions SET EndDate=%s, EndTime=%s, kWh=%s WHERE VehicleID=%s AND StartDate=%s AND StartTime=%s",
                        (end_dt.date(), end_dt.time(), kwh, vid, sd, st)
                    )
                    self.db.commit()
                    return True, "Session updated."
                except Exception:
                    try: self.db.rollback()
                    except Exception: pass
                    return False, f"UPDATE failed: {e}"
        finally:
            try: cur.close()
            except Exception: pass

    def delete_session(self, session_id):
        # session_id format: "Vehicle Nickname,YYYY-MM-DD,HH:MM:SS"
        try:
            vehicle, sd_str, st_str = session_id.rsplit(",", 2)
        except Exception:
            return False, "Bad session_id format."
        vehicle = vehicle.strip()
        sd = sd_str.strip()
        st = st_str.strip()
        cur = self.db.cursor()
        try:
            # Prefer stored procedure
            try:
                cur.callproc("deleteChargingSession", [vehicle, sd, st])
                self.db.commit()
                return True, "Session deleted."
            except Exception as e:
                # Fallback direct DELETE
                try:
                    cur.execute("SELECT VehicleID FROM vehicles WHERE TRIM(Nickname)=TRIM(%s)", (vehicle,))
                    row = cur.fetchone()
                    if not row:
                        return False, "Vehicle not found."
                    vid = row[0] if isinstance(row,(tuple,list)) else (row.get("VehicleID") if isinstance(row,dict) else row)
                    cur.execute(
                        "DELETE FROM charging_sessions WHERE VehicleID=%s AND StartDate=%s AND StartTime=%s",
                        (vid, sd, st)
                    )
                    self.db.commit()
                    return True, "Session deleted."
                except Exception:
                    try: self.db.rollback()
                    except Exception: pass
                    return False, f"DELETE failed: {e}"
        finally:
            try: cur.close()
            except Exception: pass
    def get_all(self):
        cur = self.db.cursor(dictionary=True)
        try:
            cur.execute("SELECT Vehicle, Tariff, Start, End, kWh, Cost FROM session_details ORDER BY Start")
            return cur.fetchall()
        finally:
            try: cur.close()
            except Exception: pass
    def get_sessions(self):
        return self.get_all()
class VehiclesDAL:
    def __init__(self, core):
        # Accept DAL or raw connection; resolve to connection
        self.db = getattr(core, "db", None) or (core.connect() if hasattr(core, "connect") else core)

    def get_vehicles(self):
        cur = self.db.cursor()
        try:
            cur.execute("SELECT Nickname FROM vehicles ORDER BY Nickname")
            rows = cur.fetchall()
            # Normalize list of names
            return [ (r[0] if isinstance(r,(tuple,list)) else (r.get("Nickname") if isinstance(r,dict) else str(r)) ) for r in rows ]
        finally:
            try: cur.close()
            except Exception: pass


class TariffsDAL:
    def __init__(self, core):
        # Accept DAL or raw connection; resolve to connection
        self.db = getattr(core, "db", None) or (core.connect() if hasattr(core, "connect") else core)

    def get_tariffs(self):
        cur = self.db.cursor()
        try:
            cur.execute("SELECT Name FROM tariffs ORDER BY Name")
            rows = cur.fetchall()
            return [ (r[0] if isinstance(r,(tuple,list)) else (r.get("Name") if isinstance(r,dict) else str(r)) ) for r in rows ]
        finally:
            try: cur.close()
            except Exception: pass

