from bll import BLL
b = BLL()
m = '2025-12'
print("CSV:", b.export_monthly_csv(m, 'statement_2025-12.csv'))
print("PDF:", b.export_monthly_pdf(m, 'statement_2025-12.pdf'))
