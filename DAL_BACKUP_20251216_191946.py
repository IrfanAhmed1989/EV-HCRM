import mysql.connector

class DAL:
    def __init__(self, host="127.0.0.1", port=3306, user="root", password="", database="ev_hcrm"):
        self.cfg = dict(host=host, port=int(port), user=user, password=password, database=database)
        self.conn = None

    def connect(self):
        if self.conn and self.conn.is_connected():
            return
        self.conn = mysql.connector.connect(**self.cfg)
        self.conn.autocommit = True

    def close(self):
        try:
            if self.conn and self.conn.is_connected():
                self.conn.close()
        except:
            pass

    def _cursor(self):
        if not self.conn or not self.conn.is_connected():
            self.connect()
        return self.conn.cursor(dictionary=True)

    # ---- READ via VIEWS / STORED PROC ----
    def view_session_details(self):
        cur = self._cursor()
        cur.execute("SELECT * FROM session_details ORDER BY Start")
        rows = cur.fetchall()
        cur.close()
        return rows

    def view_monthly_statements(self):
        cur = self._cursor()
        cur.execute("SELECT * FROM monthly_statements ORDER BY BillingMonth, Nickname")
        rows = cur.fetchall()
        cur.close()
        return rows

    def proc_getChargingSessions(self):
        cur = self._cursor()
        cur.callproc('getChargingSessions')
        rows = []
        for result in cur.stored_results():
            rows = [dict(zip(result.column_names, row)) for row in result.fetchall()]
            break
        cur.close()
        return rows

    # ---- WRITE via STORED PROCS ----
    def add_session(self, vehicle_nickname, tariff_name, start_date, start_time, end_date, end_time, kwh):
        cur = self._cursor()
        cur.callproc('addChargingSession', [vehicle_nickname, tariff_name, start_date, start_time, end_date, end_time, float(kwh)])
        cur.close()

    def update_session(self, vehicle_nickname, start_date, start_time, new_end_date, new_end_time, new_kwh):
        cur = self._cursor()
        cur.callproc('updateChargingSession', [vehicle_nickname, start_date, start_time, new_end_date, new_end_time, float(new_kwh)])
        cur.close()

    def delete_session(self, vehicle_nickname, start_date, start_time):
        cur = self._cursor()
        cur.callproc('deleteChargingSession', [vehicle_nickname, start_date, start_time])
        cur.close()
