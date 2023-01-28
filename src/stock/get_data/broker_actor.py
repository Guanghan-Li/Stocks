from pykka import ThreadingActor
from get_data.save_price_actor import SavePriceActor
from get_data.generate_report_actor import GenerateReportActor
from sty import fg
from datetime import datetime
from broker import Broker

class BrokerActor(ThreadingActor):
  def __init__(self, name, save_price_actor, gen_report_actor):
    super().__init__()
    print(f"{fg.yellow}STARTING{fg.rs} {name}")
    self.name = name
    self.save_price_actor: SavePriceActor = save_price_actor
    self.gen_report_actor: GenerateReportActor = gen_report_actor
  
  async def getPrices(self, asset_group: list[str], broker: Broker):
    start_date = datetime(2019, 1, 16)
    end_date = datetime(2023, 1, 18)
    for asset in asset_group:
      #print(f"{fg.green}START getPrices{fg.rs} {self.name}")
      prices = broker.getPriceData(asset, start_date=start_date, end_date=end_date, thread_name=self.name)
      if not prices["data"].empty:
        await self.gen_report_actor.generateReport(prices).get()
        self.save_price_actor.savePrice.defer(prices)

        #print(f"{fg.green}END getPrices{fg.rs} {self.name}")
      else:
        print(f"{fg.cyan}END getPrices nothing sent {prices.get('asset', '')} {fg.rs} {self.name}")
    return prices