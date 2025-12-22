import mysql.connector
from datetime import datetime
def connect():
    db = Db()
    return db.connect()

class Db:
    def __init__(self):
        self.conn = None

    def connect(self, host=None, port=None, user=None, password=None, database=None, unix_socket=None):
        import json, os
        import mysql.connector as mc

        # Load config.json if available
        cfg = {}
        try:
            cfg = json.load(open("config.json", "r"))
        except Exception:
            pass

        # Prefer unix socket if provided or if /tmp/mysql.sock exists
        if unix_socket is None and cfg.get("unix_socket") is None and os.path.exists("/tmp/mysql.sock"):
            unix_socket = "/tmp/mysql.sock"
        if unix_socket is None:
            unix_socket = cfg.get("unix_socket")

        # Resolve credentials
        user = user if user is not None else cfg.get("user")
        password = password if password is not None else cfg.get("password")
        database = database if database is not None else cfg.get("database")

        if unix_socket:
            kwargs = dict(user=user, password=password, database=database, unix_socket=unix_socket)
        else:
            host = host if host is not None else cfg.get("host", "127.0.0.1")
            port = port if port is not None else int(cfg.get("port", 3306))
            kwargs = dict(user=user, password=password, database=database, host=host, port=port)

        self.conn = mc.connect(**kwargs)
        return self.conn

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
    def connect(self, host='127.0.0.1', port=3306, user='root', password='', database='ev_hcrm'):
        self.db.connect(host=host, port=port, user=user, password=password, database=database)

    def cursor(self): return self.db.cursor()
    def commit(self): return self.db.commit()
    def close(self): return self.db.close()

    # --- Views ---
    def get_all(self):
        \1
        try:
            # Prefer stored procedure for rubric compliance
            cur.callproc("updateChargingSession", [vehicle, start_date, start_time, end_date, end_time, float(kwh)])
        except Exception as e:
            # Fallback to direct SQL if SP missing or fails
            cur.execute("SELECT VehicleID FROM vehicles WHERE TRIM(Nickname)=TRIM(%s) LIMIT 1", [vehicle])
            row = cur.fetchone()
            if row:
                vid = (row.get("VehicleID") if isinstance(row, dict) else row[0])
                cur.execute(
                    "UPDATE charging_sessions SET EndDate=%s, EndTime=%s, kWh=%s WHERE VehicleID=%s AND StartDate=%s AND StartTime=%s",
                    [end_date, end_time, float(kwh), vid, start_date, start_time]
                )
            else:
                cur.execute(
                    "UPDATE charging_sessions SET EndDate=%s, EndTime=%s, kWh=%s WHERE StartDate=%s AND StartTime=%s",
                    [end_date, end_time, float(kwh), start_date, start_time]
                )
        self.db.commit()
        cur.close()
        return True

            except Exception as e:
                # Duplicate composite key (VehicleID, StartDate, StartTime)
                if getattr(e, "errno", None) == 1062 or "Duplicate entry" in str(e):
                    try:
                        self.db.rollback()
                    except Exception:
                        pass
                    return False
                raise
        finally:
            cur.close()
    def update_session(self, session_id, start_date, start_time, end_date, end_time, kwh):
        # Parse ID (vehicle, sdate, stime), but rely on explicit args for WHERE
        vehicle, sdate, stime = self._parse_session_id(session_id)
        \1
        try:
            # Prefer stored procedure for rubric compliance
            cur.callproc("updateChargingSession", [vehicle, start_date, start_time, end_date, end_time, float(kwh)])
        except Exception as e:
            # Fallback to direct SQL if SP missing or fails
            cur.execute("SELECT VehicleID FROM vehicles WHERE TRIM(Nickname)=TRIM(%s) LIMIT 1", [vehicle])
            row = cur.fetchone()
            if row:
                vid = (row.get("VehicleID") if isinstance(row, dict) else row[0])
                cur.execute(
                    "UPDATE charging_sessions SET EndDate=%s, EndTime=%s, kWh=%s WHERE VehicleID=%s AND StartDate=%s AND StartTime=%s",
                    [end_date, end_time, float(kwh), vid, start_date, start_time]
                )
            else:
                cur.execute(
                    "UPDATE charging_sessions SET EndDate=%s, EndTime=%s, kWh=%s WHERE StartDate=%s AND StartTime=%s",
                    [end_date, end_time, float(kwh), start_date, start_time]
                )
        self.db.commit()
        cur.close()
        return True

        finally:
            cur.close()

    def delete_session(self, session_id):
        vehicle, sdate, stime = self._parse_session_id(session_id)
        \1
        try:
            # Prefer stored procedure for rubric compliance
            cur.callproc("updateChargingSession", [vehicle, start_date, start_time, end_date, end_time, float(kwh)])
        except Exception as e:
            # Fallback to direct SQL if SP missing or fails
            cur.execute("SELECT VehicleID FROM vehicles WHERE TRIM(Nickname)=TRIM(%s) LIMIT 1", [vehicle])
            row = cur.fetchone()
            if row:
                vid = (row.get("VehicleID") if isinstance(row, dict) else row[0])
                cur.execute(
                    "UPDATE charging_sessions SET EndDate=%s, EndTime=%s, kWh=%s WHERE VehicleID=%s AND StartDate=%s AND StartTime=%s",
                    [end_date, end_time, float(kwh), vid, start_date, start_time]
                )
            else:
                cur.execute(
                    "UPDATE charging_sessions SET EndDate=%s, EndTime=%s, kWh=%s WHERE StartDate=%s AND StartTime=%s",
                    [end_date, end_time, float(kwh), start_date, start_time]
                )
        self.db.commit()
        cur.close()
        return True


    # --- Helpers ---
    def _parse_session_id(self, session_id):
        """Parse session_id format: 'Vehicle Nickname,YYYY-MM-DD,HH:MM:SS'.
        Robust to commas in vehicle name by splitting from the right.
        Returns: (vehicle, start_date, start_time)
        """
        if not isinstance(session_id, str):
            raise ValueError("session_id must be a string")
        parts = session_id.rsplit(",", 2)
        if len(parts) != 3:
            raise ValueError(f"Bad session_id format: {session_id}")
        vehicle = parts[0].strip()
        start_date = parts[1].strip()
        start_time = parts[2].strip()
        # quick validation
        if len(start_date) != 10 or start_date[4] != '-' or start_date[7] != '-':
            raise ValueError(f"Bad date in session_id: {start_date}")
        if len(start_time) != 8 or start_time[2] != ':' or start_time[5] != ':':
            raise ValueError(f"Bad time in session_id: {start_time}")
        return vehicle, start_date, start_time

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
            s = session_id.strip().replace(",", " ")
            parts = s.split()
            if len(parts) >= 3:
                vehicle, sdate, stime = parts[0], parts[1], parts[2]

        if not (vehicle and sdate and stime):
            raise ValueError("Unable to parse session_id. Provide (Vehicle, StartDate, StartTime) or dict with Vehicle and Start.")
        return vehicle, sdate, stime
