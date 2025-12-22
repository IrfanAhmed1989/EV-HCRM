import mysql.connector
from datetime import datetime

class Db:
    def __init__(self):
        self.conn = None

    def connect(self, host=None, port=3306, user=None, password=None, database='ev_hcrm'):
        # 1) Try Unix socket first (Homebrew/Oracle common paths)
        sockets = [
            '/tmp/mysql.sock',
            '/opt/homebrew/var/mysql/mysql.sock',
            '/opt/homebrew/var/run/mysql.sock',
            '/usr/local/var/run/mysql.sock'
        ]
        last_err = None
        for sock in sockets:
            try:
                self.conn = mysql.connector.connect(
                    unix_socket=sock, user=user, password=password,
                    database=database, connection_timeout=5
                )
                return
            except Exception as e:
                last_err = e

        # 2) Fallback to TCP
        try:
            self.conn = mysql.connector.connect(
                host=host, port=int(port), user=user, password=password,
                database=database, connection_timeout=5
            )
            return
        except Exception as e:
            last_err = e

        raise last_err

    def cursor(self):
        if not self.conn or not getattr(self.conn, 'is_connected', lambda: False)():
            raise RuntimeError('Database not connected. Call Db.connect(...) first.')
        return self.conn.cursor(dictionary=True)

    def commit(self):
        if self.conn:
            self.conn.commit()

    def close(self):
        try:
            if self.conn:
                self.conn.close()
        except:
            pass


class DAL:
    # bll.py imports: from dal import DAL as Db, and as ChargingSessionDAL
    def __init__(self, db_or_none=None):
        if db_or_none and hasattr(db_or_none, 'cursor') and hasattr(db_or_none, 'commit'):
            self.db = db_or_none
        else:
            self.db = Db()

    # Allow bll.py to call Db().connect(...)
    def connect(self, host=None, port=3306, user=None, password=None, database='ev_hcrm'):
        self.db.connect(host=host, port=port, user=user, password=password, database=database)

    def cursor(self): return self.db.cursor()
    def commit(self): return self.db.commit()
    def close(self): return self.db.close()

    # --- Views ---
    def get_all(self):
        cur = self.db.cursor()
        cur.execute("SELECT DriverFirstName, DriverLastName, Vehicle, Tariff, Start, End, kWh, Cost FROM session_details ORDER BY Start")
        rows = cur.fetchall()
        cur.close()
        # Add synthetic SessionID for exports: Vehicle,YYYY-MM-DD,HH:MM:SS
        out = []
        for r in rows:
            s = str(r.get("Start", ""))
            parts = s.split()
            sdate = parts[0] if len(parts) > 0 else ""
            stime = parts[1] if len(parts) > 1 else ""
            rr = dict(r)
            rr["SessionID"] = f"{r.get('Vehicle','')},{sdate},{stime}"
            out.append(rr)
        return out

    def get_monthly(self):
        cur = self.db.cursor()
        cur.execute("SELECT First_Name, Last_Name, Nickname, BillingMonth, TotalSessions, Total_kWh, TotalCost FROM monthly_statements ORDER BY BillingMonth, Nickname")
        rows = cur.fetchall()
        cur.close()
        return rows

    def get_vehicles(self):
        cur = self.db.cursor()
        cur.execute("SELECT Nickname FROM vehicles ORDER BY Nickname")
        rows = [r["Nickname"] for r in cur.fetchall()]
        cur.close()
        return rows

    def get_tariffs(self):
        cur = self.db.cursor()
        cur.execute("SELECT Name FROM tariffs ORDER BY Name")
        rows = [r["Name"] for r in cur.fetchall()]
        cur.close()
        return rows

    # --- CRUD via stored procedures ---
    def add_session(self, vehicle_name, tariff_name, start_date, start_time, end_date, end_time, kwh):
        cur = self.db.cursor()
        cur.callproc("addChargingSession", [vehicle_name, tariff_name, start_date, start_time, end_date, end_time, kwh])
        self.db.commit()
        cur.close()
        return True

    def update_session(self, session_id, start_date, start_time, end_date, end_time, kwh):
        vehicle, sdate, stime = self._parse_session_id(session_id)
        cur = self.db.cursor()
        sdate = start_date
        stime = start_time
        cur.callproc("updateChargingSession", [vehicle, sdate, stime, end_date, end_time, kwh])
        self.db.commit()
        cur.close()
        return True

    def delete_session(self, session_id):
        vehicle, sdate, stime = self._parse_session_id(session_id)
        cur = self.db.cursor()
        cur.callproc("deleteChargingSession", [vehicle, sdate, stime])
        self.db.commit()
        cur.close()
        return True

    # --- Helpers ---
    def _parse_session_id(self, session_id):
        from datetime import datetime as _dt
        vehicle = None; sdate = None; stime = None

        if isinstance(session_id, dict):
            vehicle = session_id.get('Vehicle') or session_id.get('Nickname') or session_id.get('vehicle')
            start = session_id.get('Start') or session_id.get('start')
            if start:
                try:
                    dt = _dt.strptime(str(start), "%Y-%m-%d %H:%M:%S")
                    sdate = dt.strftime("%Y-%m-%d")
                    stime = dt.strftime("%H:%M:%S")
                except Exception:
                    parts = str(start).split()
                    if len(parts) >= 2:
                        sdate, stime = parts[0], parts[1]

        elif isinstance(session_id, (tuple, list)) and len(session_id) >= 3:
            vehicle, sdate, stime = session_id[0], session_id[1], session_id[2]

        elif isinstance(session_id, str):
    s = session_id.strip()
    parts = s.split(",")
    if len(parts) >= 3:
        vehicle, sdate, stime = parts[0].strip(), parts[1].strip(), parts[2].strip()
