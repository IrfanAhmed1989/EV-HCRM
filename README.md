# EV-HCRM: EV Home Charging Reimbursement Manager

## 📌 Overview
EV-HCRM is a Python GUI application integrated with MySQL to manage EV home charging sessions for reimbursement purposes.
It supports CRUD operations, auto Session ID (Vehicle + DateTime), and monthly CSV/PDF exports.

## ✅ Features
- Login-driven DB connection
- CRUD (Add/Update/Delete) charging sessions
- Auto-generated Session ID (Vehicle + DateTime)
- Monthly statements in CSV & PDF
- Stored Procedures & Views
- Input validation & error handling

## 🛠 Tech Stack
- Python 3.x, Tkinter
- MySQL
- ReportLab

## 🚀 Setup
pip install -r requirements.txt
mysql -u root -p < ev_hcrm.sql
Update config.json for DB credentials

## ▶ Run
python GUI.py

## 🔗 Links
- GitHub: https://github.com/IrfanAhmed1989/EV-HCRM
