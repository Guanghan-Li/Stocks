from repos.report_database import *
from repos.report_model import *
from datetime import datetime
rd = ReportDatabase(report_proxy, None, name="Data/1_22.db")
now = datetime.fromisoformat("2022-01-20")
report = rd.getReports(now, 10)

for entry in report.entries:
  print(entry)