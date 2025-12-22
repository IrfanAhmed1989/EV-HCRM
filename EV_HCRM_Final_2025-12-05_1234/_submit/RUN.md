EV-HCRM Final Project (Quick Run Guide)
1) Ensure MySQL is running. Load schema:  mysql -u root -piiii < ev_hcrm.sql
2) Activate venv:  source venv/bin/activate  (or use system Python)
3) Install deps:   python3 -m pip install mysql-connector-python matplotlib reportlab fpdf

4) Run GUI:        python3 GUI.py
5) Login screen:   enter host, port, user, password, database (defaults ok)
6) Verify CRUD:    add/update/delete sessions; view refreshes instantly
7) Advanced feat:  export December 2025 statements (CSV/PDF) and view charts
