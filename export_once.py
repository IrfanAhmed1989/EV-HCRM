from bll import BLL
b = BLL()
def run():
    # CSV
    r1 = b.export_monthly_csv("2025-12","EV_HCRM_Submission_2025-12-18/statement_2025-12.csv")
    if isinstance(r1, tuple):
        ok1, msg1 = r1
    else:
        ok1, msg1 = bool(r1), "CSV export done" if r1 else "CSV export failed"
    print("CSV:", ok1, msg1)
    # PDF
    r2 = b.export_monthly_pdf("2025-12","EV_HCRM_Submission_2025-12-18/statement_2025-12.pdf")
    if isinstance(r2, tuple):
        ok2, msg2 = r2
    else:
        ok2, msg2 = bool(r2), "PDF export done" if r2 else "PDF export failed"
    print("PDF:", ok2, msg2)
if __name__ == "__main__":
    run()
