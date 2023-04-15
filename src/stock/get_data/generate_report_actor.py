from get_data.helpers import *
from get_data.pnf_actor import PNFActor
from get_data.report_save_actor import ReportSaveActor
from repos.report_database import ReportDatabase


class GenerateReportActor(ThreadingActor):
    def __init__(self, name, save_report_actor):
        super().__init__()
        self.name = name
        Helpers.use_deamon_thread = True
        self.helpers = Helpers.start().proxy()
        self.save_report_actor: ReportSaveActor = save_report_actor
        PNFActor.use_deamon_thread = True
        self.pnf_actor = PNFActor.start("PNF Actor").proxy()

    def on_failure(
        self, exception_type, exception_value: BaseException, traceback
    ) -> None:
        print("GenerateReport Failed:", exception_type)

    async def generateReport(self, message):
        asset = message["asset"]
        data = message["data"]
        end_date = message["date"]
        start_date = datetime(2018, 2, 21)
        now = datetime.fromisoformat(end_date)
        weeks = 52
        entry = 1

        while weeks > 0 and entry != None:
            weeks -= 1
            now -= relativedelta(days=7)
            prices = self.helpers.getTwoYearPrices(asset, data, now).get()
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
