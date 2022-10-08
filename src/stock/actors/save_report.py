import thespian
from thespian.actors import *
from sty import fg
from src.stock.actors.messages import *
from src.stock.repos.report_database import ReportDatabase
from src.stock.lib.log.log import Log
from src.stock.values.report import Entry
from datetime import datetime
from src.stock.values.tasks import Task,Tasks

class SaveReportActor(ActorTypeDispatcher):
  def __init__(self):
    super().__init__()
  
  def receiveMsg_SetupMessage(self, message: SetupMessage, sender):
    self.name = message.info["name"]
    self.log = Log(message.log)
    self.log.info("SaveReportActor Got Setup message", self.name)
    self.report_database = ReportDatabase()
    self.weeks: dict[datetime, list] = {}
    self.task_manager = message.info.get("task_manager", None)
    self.send(sender, 0)

  def receiveMsg_SaveReportMessage(self, message: SaveReportMessage, sender):
    self.log.info(f"{fg.li_blue}START saveReport{fg.rs} {self.name}")
    task = Task.create(self.name, None)

    self.send(self.task_manager,task.toCreateMessage())
    self.report_database.saveEntries(message.entries)
    self.send(self.task_manager, task.toFinishedMessage())

    self.log.info(f"{fg.li_blue}END saveReport{fg.rs} {self.name}")