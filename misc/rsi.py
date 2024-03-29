from stock.repos.report_database import *
from stock.repos.report_model import *
from datetime import datetime

rd = ReportDatabase(report_proxy, None, name="Data/reports.db")
now = datetime.fromisoformat("2023-09-13")
report = rd.getReports(now, 20)
for entry in report.entries:
    print(entry)
