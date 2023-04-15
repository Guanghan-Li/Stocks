from src.stock.repos.report_database import ReportDatabase
from src.stock.repos.reports_by_year import ReportYearDatabase
from datetime import datetime

rd = ReportDatabase()
d = datetime(2022, 2, 14, 21, 0, 0)
entries = rd.getDatesForSymbol("AAL")
for entry in entries:
    print(entry)
