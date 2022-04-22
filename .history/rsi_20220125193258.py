from repos.report_database import *
from repos.report_model import *
from datetime import datetime
rd = ReportDatabase(report_proxy, None, name="Data/reports.db")
now = datetime.fromisoformat("2022-01-24")
report = rd.getReports(now, 20)
for entry in report.entries:
  print(entry)