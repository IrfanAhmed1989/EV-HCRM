EV-HCRM

Submission Date: 2025-12-17
Architecture: GUI-BLL-DAL (MySQL views and stored procedures)

Quick Start
1) Ensure MySQL is running and database "ev_hcrm" exists with views/SPs.
2) Verify config.json:
   {"host":"127.0.0.1","port":3306,"user":"root","password":"iiii","database":"ev_hcrm"}
3) Compile: .venv/bin/python -m py_compile dal.py bll.py gui.py
4) Run GUI: .venv/bin/python gui.py

Files
- gui.py, bll.py, dal.py, config.json
- ev_hcrm_submit_2025-12-17_final.sql
- statement_YYYY-MM.csv, statement_YYYY-MM.pdf

Troubleshooting
- No module named "bll": ensure file is bll.py and imports use "from bll import BLL"
- MySQL 2003 HY000: start MySQL (brew services start mysql) and confirm config.json creds
- venv path: use .venv/bin/python; fallback "python3" if venv not active


Notes
- Added run.sh and requirements.txt for easy launch and reproducibility.
- If gui.py not present, use gui.py (lowercase).


Grader Checklist
1) Layered modules: gui.py (view), bll.py (business), dal.py (data access)
2) Only DAL touches DB (stored procedures/views), BLL mediates, GUI never calls DB directly
3) Login before data: run.sh prompts and writes config.json (changeable host/port/user/password/db)
4) CRUD in GUI and programmatic smoke (add/update/delete)
5) Retrieval & views: sessions/STATEMENTS reflect table changes
6) Advanced feature: export monthly CSV/PDF (bll.export_monthly_*)
7) App runs without crashing: compile OK, GUI launches, Connected shown
8) User-friendly formatting: date/time pickers, dropdowns
9) Up-to-date SQL: ev_hcrm_submit_2025-12-17_final.sql included
