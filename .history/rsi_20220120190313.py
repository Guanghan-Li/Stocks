from repos.report_database import *
from repos.report_model import *
from datetime import datetime
rd = ReportDatabase(report_proxy, None)
reports = rd.getReports(datetime.now(), 20)