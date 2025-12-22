EV-HCRM — EV Home Charging Reimbursement Manager

Overview:
EV-HCRM tracks EV charging sessions, tariffs, and monthly statements using a 3-layer architecture:
- View: gui.py (Tkinter)
- Business Logic: bll.py
- Data Access: dal.py (stored procedures & views only)

System Requirements:
- macOS/Linux, Python 3.10+, MySQL 8+
- Packages: mysql-connector-python, tkcalendar, fpdf, matplotlib, numpy, reportlab, python-dateutil

Quick Start:
1) Import SQL: mysql -u root -p < ev_hcrm_submit.sql
2) Activate venv: source .venv/bin/activate
3) Install deps: pip install -r requirements.txt
4) Run GUI: ./run.sh or python gui.py
Login with Host (default 127.0.0.1), Port 3306, User, Password.

Advanced Feature:
- Export Monthly Statements to CSV and PDF from GUI.

Rubric Conformance:
- Three modules: gui.py, bll.py, dal.py
- Only DAL talks to DB via SPs/views
- Login precedes data; credentials editable
- GUI shows status and errors
- CRUD: Add, Update, Delete sessions; changes reflect in views
- Retrieve/View: Sessions grid and Monthly Statements use DB views

Troubleshooting:
- Connection refused: ensure MySQL running; use host 127.0.0.1
- macOS socket: /tmp/mysql.sock
- Module not found: pip install -r requirements.txt
- PDF empty: pick a month with data

Grader Run Card:
- Verify DB with mysql queries
- Launch GUI, login, confirm Connected
- Perform Add/Edit/Delete; Refresh Sessions
- Export Monthly CSV and PDF
- Confirm files: gui.py, bll.py, dal.py, requirements.txt, run.sh, ev_hcrm_submit.sql, config.json, statement_*.csv, statement_*.pdf, README.md, GRADER_CHECKLIST.txt

Files Included:
- gui.py, bll.py, dal.py
- ev_hcrm_submit.sql
- requirements.txt, run.sh, config.json
- statement_2025-12.csv, statement_2025-12.pdf
- README.md, GRADER_CHECKLIST.txt


Advanced Feature - Sources / References:
- Python csv module (stdlib)
- FPDF (Python) for PDF
- Tkinter and tkcalendar
- mysql-connector-python

User-Friendly Formatting:
- Date picker via tkcalendar
- Dropdowns/combobox for tariff and time
- Status line and message boxes for errors
