from pykka import ThreadingActor
from repos.report_database import ReportDatabase
from sty import fg
from repos.report_model import report_proxy

class ReportSaveActor(ThreadingActor):
  def __init__(self, name):
    super().__init__()
    self.name = name
    self.report_database = ReportDatabase(report_proxy, "Data/reports.db")
  
  def saveReport(self, entry):
    print(f"{fg.li_blue}START saveReport{fg.rs} {self.name}")
    self.report_database.saveEntry(entry)
    print(f"{fg.li_blue}END saveReport{fg.rs} {self.name}")
  
  def on_failure(self, exception_type, exception_value: BaseException, traceback) -> None:
      print(exception_type, exception_value)
      #self.stop()