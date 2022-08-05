import thespian
from thespian.actors import *
from sty import fg

class GenerateReportActor(ActorTypeDispatcher):
  def __init__(self, name, save_report_actor):
    super().__init__()
    self.name = name
    # Helpers.use_deamon_thread = True
    # self.helpers = Helpers.start().proxy()
    self.save_report_actor: ReportSaveActor = save_report_actor
    # PNFActor.use_deamon_thread = True
    # self.pnf_actor = PNFActor.start("PNF Actor").proxy()
  
  def receiveMsg_SetupMessage(self, message, sender):
    self.save_report_actor = message.info["save_report_actor"]


  def receiveMsg_GenerateReport(self, message, sender):
    pass

  def on_failure(self, exception_type, exception_value: BaseException, traceback) -> None:
      print("GenerateReport Failed:", exception_type)

  async def generateReport(self, message):
    asset = message["asset"]
    data = message["data"]
    end_date = message["date"]
    start_date = datetime(2018, 6, 22)
    now = datetime.fromisoformat(end_date)
    weeks = 2
    entry = 1

    if len(data) < 980:
      return None

    while weeks > 0 and entry != None:
      weeks -= 1
      now -= relativedelta(days=7)
      prices = self.helpers.getTwoYearPrices2(asset, data, now).get()
      if len(prices) > 0:
        entry = ReportDatabase.generateEntry(asset, prices, now)

        if entry != None:
          print(entry.stock)
          foo = await self.pnf_actor.updateReport(asset, prices)
          entry.trend = foo[0]
          entry.column = foo[1]
          print("Generated Entry", now, entry)
          self.save_report_actor.saveReport.defer(entry)
        else:
          print("Got None")
    print("DONE with", asset)