import mysql.connector
from mysql.connector import Error

class Db:
    def __init__(self):
        self.cnx = None

    def connect(self, host, port, user, password, database="ev_hcrm"):
        last_err = None
        # Try TCP first
        try:
            self.cnx = mysql.connector.connect(
                host=host, port=port, user=user, password=password,
                database=database, autocommit=False
            )
        except Error as e:
            last_err = e
            self.cnx = None
            # Fallback to common UNIX sockets (macOS/Homebrew/Linux)
            for sock in ("/tmp/mysql.sock", "/opt/homebrew/var/mysql/mysql.sock", "/var/run/mysqld/mysqld.sock"):
                try:
                    self.cnx = mysql.connector.connect(
                        user=user, password=password, database=database,
                        unix_socket=sock, autocommit=False
                    )
                    break
                except Error as e2:
                    last_err = e2
            if not self.cnx:
                raise RuntimeError(f"MySQL connection error: {last_err}")
        if not self.cnx or not self.cnx.is_connected():
            raise RuntimeError("Connection failed.")

    def cursor(self):
        if not self.cnx or not self.cnx.is_connected():
            raise RuntimeError("No active MySQL connection.")
        return self.cnx.cursor(buffered=True)

    def commit(self):
        if self.cnx and self.cnx.is_connected():
            self.cnx.commit()

    def rollback(self):
        if self.cnx and self.cnx.is_connected():
            self.cnx.rollback()

    def close(self):
        if self.cnx and self.cnx.is_connected():
            self.cnx.close()

class ChargingSessionDAL:
    def __init__(self, db: Db):
        self.db = db

    def get_all(self):
        cur = self.db.cursor()
        try:
            cur.callproc("getChargingSessions")
            rows = []
            for result in cur.stored_results():
                cols = [d[0] for d in result.description]
                for r in result.fetchall():
                    rows.append(dict(zip(cols, r)))
            return rows
        finally:
            cur.close()

    def add_session(self, vehicle_name, tariff_name, start_date, start_time, end_date, end_time, kwh):
        cur = self.db.cursor()
        try:
            cur.callproc("addChargingSession", (vehicle_name, tariff_name, start_date, start_time, end_date, end_time, kwh))
            self.db.commit()
            return True, ""
        except Error as e:
            self.db.rollback()
            return False, str(e)
        finally:
            cur.close()

    def update_session(self, session_id, new_start_date, new_start_time, new_end_date, new_end_time, new_kwh):
        cur = self.db.cursor()
        try:
            cur.callproc("updateChargingSession", (session_id, new_start_date, new_start_time, new_end_date, new_end_time, new_kwh))
            self.db.commit()
            return True, ""
        except Error as e:
            self.db.rollback()
            return False, str(e)
        finally:
            cur.close()

    def delete_session(self, session_id):
        cur = self.db.cursor()
        try:
            cur.callproc("deleteChargingSession", (session_id,))
            self.db.commit()
            return True, ""
        except Error as e:
            self.db.rollback()
            return False, str(e)
        finally:
            cur.close()

    def get_vehicles(self):
        cur = self.db.cursor()
        try:
            try:
                cur.execute("SELECT Nickname FROM vehicles")  # schema in ev_hcrm.sql
                return [row[0] for row in cur.fetchall()]
            except Exception:
                cur.execute("SELECT VehicleName FROM vehicles")  # fallback if older schema
                return [row[0] for row in cur.fetchall()]
        finally:
            cur.close()

    def get_tariffs(self):
        cur = self.db.cursor()
        try:
            try:
                cur.execute("SELECT Name FROM tariffs")  # schema in ev_hcrm.sql
                return [row[0] for row in cur.fetchall()]
            except Exception:
                cur.execute("SELECT TariffName FROM tariffs")  # fallback if older schema
                return [row[0] for row in cur.fetchall()]
        finally:
            cur.close()
