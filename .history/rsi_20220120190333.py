from repos.report_database import *
from repos.report_model import *
from datetime import datetime
rd = ReportDatabase(report_proxy, None)
report = rd.getReports(datetime.now(), 20)

for entry in report.entries:
  print(entry)