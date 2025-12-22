import mysql.connector

class DAL:
    def __init__(self, host="127.0.0.1", port=3306, user="root", password="", database="ev_hcrm"):
        self.cfg = dict(host=host, port=int(port), user=user, password=password, database=database)
        self.conn = None

    def connect(self):
        self.conn = mysql.connector.connect(**self.cfg)

    def _cursor(self):
        if not self.conn or not self.conn.is_connected():
            self.connect()
        return self.conn.cursor(dictionary=True)

    def view_session_details(self):
        cur = self._cursor()
        cur.execute("SELECT * FROM session_details")
        rows = cur.fetchall()
        cur.close()
        return rows

    def view_monthly_statements(self):
        cur = self._cursor()
        cur.execute("SELECT * FROM monthly_statements")
        rows = cur.fetchall()
        cur.close()
        return rows

    def addsession(self, vehicle_nickname, tariff_name, start_date, start_time, end_date, end_time, kwh):
        cur = self._cursor()
        cur.callproc("addChargingSession", [vehicle_nickname, tariff_name, start_date, start_time, end_date, end_time, kwh])
        self.conn.commit()
        cur.close()

    def updatesession(self, vehicle_nickname, start_date, start_time, end_date, end_time, kwh):
        cur = self._cursor()
        cur.callproc("updateChargingSession", [vehicle_nickname, start_date, start_time, end_date, end_time, kwh])
        self.conn.commit()
        cur.close()

    def deletesession(self, vehicle_nickname, start_date, start_time):
        cur = self._cursor()
        cur.callproc("deleteChargingSession", [vehicle_nickname, start_date, start_time])
        self.conn.commit()
        cur.close()
