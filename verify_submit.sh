#!/usr/bin/env bash
set -euo pipefail
mysql -u root -piiii < ev_hcrm_submit.sql
mysql -u root -piiii -e "USE ev_hcrm; SELECT COUNT(*) AS rows_in_charging_sessions FROM charging_sessions;"
mysql -u root -piiii -e "USE ev_hcrm; SELECT * FROM monthly_statements ORDER BY BillingMonth, Nickname;"
mysql -u root -piiii -e "USE ev_hcrm; SELECT * FROM session_details ORDER BY Start LIMIT 5;"
