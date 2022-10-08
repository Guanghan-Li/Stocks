import thespian
from thespian.actors import *
from sty import fg
from dateutil.relativedelta import relativedelta
from datetime import datetime
from src.stock.repos.report_database import ReportDatabase

from src.stock.actors.messages.generate_report import GenerateReportMessage
from src.stock.actors.messages import *
from src.stock.values.prices import Prices, Price
from src.stock.lib.log.log import Log
from src.stock.repos.announcement_database import AnnouncementDatabase
import time
from src.stock.values.tasks import Task, Tasks


class GenerateReportActor(ActorTypeDispatcher):
  def __init__(self):
    super().__init__()
  
  def receiveMsg_SetupMessage(self, message: SetupMessage, sender):
    self.report_database = ReportDatabase()
    self.announce_db = AnnouncementDatabase()
    self.log = Log(message.log)
    self.name = message.info["name"]
    self.save_report_actor = message.info["save_report_actor"]
    self.task_manager = message.info.get("task_manager", None)
    # self.pnf_actor = message.info["pnf_actor"]
    self.send(sender, 0)


  def receiveMsg_GenerateReportMessage(self, message: GenerateReportMessage, sender):
    self.all_assets = []
    self.log.info(self.name, "Got message")
    asset = message.asset
    prices:  Prices = message.data
    end_date = prices.end_date
    start_date = prices.start_date
    now = end_date
    weeks = 104
    entry = 1
    entries = []

    task = Task.create(self.name, prices.symbol)
    self.send(self.task_manager, task.toCreateMessage())

    while weeks > 0 and entry != None:
      new_task = Task.create(self.name, None)
      self.send(self.task_manager, new_task.toCreateMessage())
      weeks -= 1

      now -= relativedelta(days=7)
      now = datetime(now.year, now.month, now.day)
      prices = prices.getBefore(now)
      if len(prices) > 0:
        ann = self.announce_db.listAnnouncements(symbol=prices.symbol)
        for a in ann:
          ex_date = datetime(a.ex_date.year, a.ex_date.month, a.ex_date.day)
          if ex_date < now:
            prices = prices.adjust(a)
        entry = ReportDatabase.generateEntry(prices)

        if entry != None:
          self.log.info(entry)
          # foo = await self.pnf_actor.updateReport(asset, prices)
          # entry.trend = foo[0]
          # entry.column = foo[1]
          entries.append(entry)
          self.send(self.task_manager, new_task.toFinishedMessage())
          #self.send(self.save_report_actor, SaveReportMessage(entry, message.sender))
        else:
          self.send(self.task_manager, new_task.toFinishedMessage())
      else:
        self.send(self.task_manager, new_task.toFinishedMessage())
      
    self.send(self.save_report_actor, SaveReportMessage(entries, message.sender))
    self.send(self.task_manager, task.toFinishedMessage())
    self.log.info("DONE with", asset)