import thespian
from thespian.actors import *
from sty import fg
from dateutil.relativedelta import relativedelta
from datetime import datetime
from src.stock.repos.report_database import ReportDatabase
from src.stock.repos.price_database import PricesDatabase, Price, Prices

from src.stock.actors.messages.generate_report import GenerateReportMessage
from src.stock.actors.messages import *
from src.stock.lib.log.log import Log
from src.stock.repos.announcement_database import AnnouncementDatabase
import time
from src.stock.values.tasks import Task, Tasks


class GenerateReportActor(ActorTypeDispatcher):
  def __init__(self):
    super().__init__()
  
  def receiveMsg_SetupMessage(self, message: SetupMessage, sender):
    self.report_database = ReportDatabase()
    self.price_database = PricesDatabase()
    self.announce_db = AnnouncementDatabase()
    self.log = Log(message.log)
    self.name = message.info["name"]
    self.save_report_actor = message.info["save_report_actor"]
    self.task_manager = message.info.get("task_manager", None)
    # self.pnf_actor = message.info["pnf_actor"]
    self.send(sender, 0)

  def receiveMsg_GetAllAssetsMessage(self, message: GetAllAssetsMessage, sender):
    for asset in message.assets:
      prices = self.price_database.getPricesFromDB(asset)
      self.generate_reports(asset, prices)

  def generate_reports(self, asset: str, prices: Prices):
    self.all_assets = []
    end_date = prices.end_date
    start_date = prices.start_date
    now = end_date
    weeks = 104
    entry = 1
    entries = []

    task = Task.create(self.name, prices.symbol)
    self.send(self.task_manager, task.toCreateMessage())
    self.log.info(f"{fg.yellow}START generateReport{fg.rs} {self.name} {asset}")
    start = datetime.now()
    while weeks > 0 and entry != None:
      new_task = Task.create(self.name, None)
      weeks -= 1

      now -= relativedelta(days=7)
      now = datetime(now.year, now.month, now.day)
      prices = prices.getBefore(now)

      if len(prices) > 0:
        entry = ReportDatabase.generateEntry(prices)

        if entry != None:
          entries.append(entry)
    
    end = datetime.now()
    time_spent = (end-start).microseconds*0.001
    self.log.info(f"{fg.yellow}DONE generateReport{fg.rs} {self.name} | {asset} | took: {time_spent}")
    if len(entries)>0:
      self.send(self.save_report_actor, SaveReportMessage(entries, None))
    else:
      self.log.info(f"No entries generated skipping {prices.symbol} {prices.pretty_date_range}")