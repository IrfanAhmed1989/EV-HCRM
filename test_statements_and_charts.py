from BLL import BLL
import os

def main():
    bll = BLL()
    month = "2025-12"

    # Export CSV
    csv_file = f"statement_{month}.csv"
    if bll.export_monthly_csv(month, csv_file):
        print(f"✅ CSV exported: {csv_file} ({os.path.getsize(csv_file)} bytes)")

    # Export PDF
    pdf_file = f"statement_{month}.pdf"
    if bll.export_monthly_pdf(month, pdf_file):
        print(f"✅ PDF exported: {pdf_file} ({os.path.getsize(pdf_file)} bytes)")

    print("✅ Now open GUI and check Charts tab for cost bars.")

if __name__ == "__main__":
    main()
