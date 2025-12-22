# EV-HCRM — Grader Quick-Run (2025-12-11)

Run these three commands:
1) mysql -u root -p < ev_hcrm_submit_2025-12-11_final.sql
2) mysql -u root -p -e "USE ev_hcrm; SHOW FULL TABLES WHERE Table_type='BASE TABLE'; SHOW FULL TABLES WHERE Table_type='VIEW';"
3) mysql -u root -p -e "SELECT * FROM ev_hcrm.monthly_statements WHERE BillingMonth='2025-12' AND Nickname='Tesla Model 3' ORDER BY First_Name, Last_Name, Nickname;"
Expected: Base tables (drivers, vehicles, tariffs, charging_sessions), Views (monthly_statements, session_details), Monthly statement shows Alice | Green | Tesla Model 3 | 2025-12 | 16 | 262.40 | 39.40
---
# EV Home Charging Reimbursement Manager (EV-HCRM)
## 📦 Project Overview & Folder Contents
This project is a Python GUI application with a MySQL backend for managing EV home charging sessions and generating monthly reimbursement statements.
**Folder contents:**
- `ev_hcrm_submit.sql` — Master SQL file (starts with `DROP DATABASE IF EXISTS ev_hcrm;`)
- `ev_hcrm_submit_YYYY-MM-DD_HHMM.sql` — Timestamped submission copy (e.g., `ev_hcrm_submit_2025-12-09_0206.sql`)
- `dal.py`, `bll.py`, `gui.py` — Python layers (Data Access, Business Logic, Tkinter GUI)
- `ER_Diagram_EV_HCRM.pdf` — ER diagram
- `README.md` — This guide
## ✅ System Requirements
- MySQL (local server)
- Python 3.10+ with `venv`
- Packages: `mysql-connector-python`, `matplotlib`, `fpdf`
## 🚀 Quick Start (SQL-only)
```bash
mysql -u root -piiii < ev_hcrm_submit.sql
mysql -u root -piiii -e "USE ev_hcrm; SELECT COUNT(*) AS rows_in_charging_sessions FROM charging_sessions;"
mysql -u root -piiii -e "USE ev_hcrm; SELECT * FROM monthly_statements ORDER BY BillingMonth, Nickname;"
mysql -u root -piiii -e "USE ev_hcrm; SELECT * FROM session_details ORDER BY Start LIMIT 5;"
## ✅ Grader Quick Checklist
- Run: `mysql -u root -piiii < ev_hcrm_submit.sql`
- Verify: `SELECT COUNT(*) FROM charging_sessions;` → should be ≥30
- Check views: `SELECT * FROM monthly_statements;` and `session_details;`
- Test cascade: `CALL deleteVehicleByNickname('Tesla Model 3');` → no orphans
- Run GUI: `python gui.py` after installing `mysql-connector-python matplotlib fpdf`
## MySQL connection note (macOS)
This app connects via Unix socket automatically (e.g., /tmp/mysql.sock). If a CLI command fails using TCP (127.0.0.1:3306), use:
mysql --socket=/tmp/mysql.sock -u root -p
Login screen defaults: Host 127.0.0.1, Port 3306, User root, Password iiii, DB ev_hcrm.
Even with TCP disabled (skip_networking=ON, port=0), the app connects via socket successfully.
This app connects via Unix socket automatically (e.g., /tmp/mysql.sock).
If a CLI command fails using TCP (127.0.0.1:3306), use:
Login defaults: Host 127.0.0.1, Port 3306, User root, Password iiii, DB ev_hcrm.
## Instructor Feedback Fixes (Dec 20, 2025)

- **Update & Delete**: Implemented end-to-end. DAL `update_session` now uses VehicleID lookup (by Nickname) and a targeted `UPDATE` on `(VehicleID, StartDate, StartTime)` with commit; `deleteChargingSession` via stored procedure with commit.
- **Date/Time Pickers**: Sessions tab provides validated `YYYY-MM-DD` date entries and Spinbox time pickers (`HH:MM:SS`) for Start/End.
- **Login-Driven Connection**: Login screen writes `config.json` (host, port, user, password, database, unix_socket). DAL/BLL read from config; no hardcoded values. Socket preferred with TCP fallback.

Verification: ADD ✅, UPDATE ✅ (End=22:30:00, kWh=36.50), view reflects change; DELETE ✅ (counts=0). CSV/PDF exports succeed.
