import thespian
from thespian.actors import *
from sty import fg

class ReportSaveActor(ActorTypeDispatcher):
  def __init__(self, name):
    super().__init__()
    self.name = name
    self.report_database = ReportDatabase(report_proxy, "Data/reports.db")
  
  def receiveMsg_SetupMessage(self, message, sender):
    pass

  def receiveMsg_SaveReport(self, message, sender):
    pass

  def saveReport(self, entry):
    print(f"{fg.li_blue}START saveReport{fg.rs} {self.name}")
    self.report_database.saveEntry(entry)
    print(f"{fg.li_blue}END saveReport{fg.rs} {self.name}")
  
  def on_failure(self, exception_type, exception_value: BaseException, traceback) -> None:
      print(exception_type, exception_value)
      #self.stop()