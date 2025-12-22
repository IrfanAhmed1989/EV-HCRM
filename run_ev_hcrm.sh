set -e

echo "== Step 1: Write dal.py safely =="
cat > dal.py <<'PY'
import mysql.connector

class DAL:
    def __init__(self, host="127.0.0.1", port=3306, user="root", password="", database="ev_hcrm"):
        # Credentials come from GUI login; only DB name may default.
        self.cfg = dict(host=host, port=int(port), user=user, password=password, database=database)
        self.conn = None

    def connect(self):
        self.conn = mysql.connector.connect(**self.cfg)

    def _cursor(self):
        if not self.conn or not self.conn.is_connected():
            self.connect()
        return self.conn.cursor(dictionary=True)

    # ----- READS via views -----
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

    # ----- CRUD via stored procedures -----
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
PY
echo "✅ dal.py written"

echo "== Step 2: Ensure mysql-connector in venv =="
.venv/bin/python - <<'PY'
import sys, subprocess
try:
    import mysql.connector
    print("✅ mysql-connector-python already installed")
except Exception:
    print("⏳ Installing mysql-connector-python in venv...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "mysql-connector-python"])
    print("✅ mysql-connector-python installed")
PY

echo "== Step 3: Compile modules =="
.venv/bin/python -m py_compile dal.py bll.py gui.py && echo "✅ all syntax OK"

echo "== Step 4: Optional DB rebuild if dump exists =="
if [ -f "ev_hcrm_submit_2025-12-11_final.sql" ]; then
  echo "⏳ Recreating database from ev_hcrm_submit_2025-12-11_final.sql ..."
  mysql -u root -piiii < ev_hcrm_submit_2025-12-11_final.sql && echo "✅ DB ev_hcrm recreated"
else
  echo "ℹ️ SQL dump not found in this folder; skipping DB rebuild"
fi

echo "== Step 5: Launch GUI =="
.venv/bin/python gui.py
