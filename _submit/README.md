# EV Home Charging Reimbursement Manager (EV-HCRM)

## Overview
EV-HCRM is a Python GUI app to manage EV home charging sessions, calculate costs, and generate monthly reimbursement statements.

## Features
- Add, Edit, Delete charging sessions
- Export monthly statements (CSV & PDF)
- View cost charts
- Dropdowns for Vehicle & Tariff

## Setup
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install mysql-connector-python fpdf matplotlib

# Load database
mysql -u root -p < ev_hcrm.sql

# Run app
python GUI.py
```

## Testing Checklist
1. Add Session → Fill details → Submit → Refresh
2. Edit Session → Change kWh → Refresh
3. Delete Session → Confirm → Refresh
4. Monthly Statements → Enter YYYY-MM → Export CSV & PDF
5. Charts → Refresh Chart → See cost bars

## Screenshots
screenshots/gui.png

## ER Diagram
er_diagram.png

## Screenshots
- Login prompt: screenshot_login_prompt.png
- Sessions tab: screenshot_sessions_tab.png
- Charts tab: screenshot_charts_tab.png

## Exact grader commands
source venv/bin/activate
python3 -c "import mysql.connector, reportlab, fpdf, matplotlib; print('✓ imports OK')"
mysqladmin -u root -piiii ping
mysql -u root -piiii -e "SHOW DATABASES LIKE 'ev_hcrm';"
python3 -c "from BLL import BLL; b=BLL(); m='2025-12'; b.export_monthly_csv(m,'statement_'+m+'.csv'); b.export_monthly_pdf(m,'statement_'+m+'.pdf'); print('✓ CSV+PDF exported again')"
ls -lh statement_2025-12.csv statement_2025-12.pdf

## Screenshots
- Login prompt: screenshot_login_prompt.png
- Sessions tab: screenshot_sessions_tab.png
- Charts tab: screenshot_charts_tab.png

## Exact grader commands
source venv/bin/activate
python3 -c "import mysql.connector, reportlab, fpdf, matplotlib; print('✓ imports OK')"
mysqladmin -u root -piiii ping
mysql -u root -piiii -e "SHOW DATABASES LIKE 'ev_hcrm';"
python3 -c "from BLL import BLL; b=BLL(); m='2025-12'; b.export_monthly_csv(m,'statement_'+m+'.csv'); b.export_monthly_pdf(m,'statement_'+m+'.pdf'); print('✓ CSV+PDF exported again')"
ls -lh statement_2025-12.csv statement_2025-12.pdf
