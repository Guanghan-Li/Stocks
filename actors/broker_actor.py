import thespian
from thespian.actors import *
from sty import fg
from actors.messages import *

class BrokerActor(ActorTypeDispatcher):
  def __init__(self):
    self.ap = AdjustPrice()
  
  def receiveMsg_SetupMessage(self, message: SetupMessage, sender):
    self.save_price_actor = message.info["save_price_actor"]
    self.gen_report_actor = message.info["gen_report_actor"]
    self.name = message.info["name"]

  def receiveMsg_GetPrice(self, message, sender):
    pass
  
  
  async def getPrices(self, asset_group: list[str], broker: Broker):
    start_date = datetime(2018, 6, 8)
    end_date = datetime(2022, 6, 15)
    for asset in asset_group:
      #print(f"{fg.green}START getPrices{fg.rs} {self.name}")
      prices = broker.getPriceData(asset, start_date=start_date, end_date=end_date, thread_name=self.name)
      prices = self.ap.applyAllAnnouncements(asset, prices)
      if prices["data"] != []:
        # TODO check amount of prices here
        await self.gen_report_actor.generateReport(prices).get()
        self.save_price_actor.savePrice.defer(prices)

        #print(f"{fg.green}END getPrices{fg.rs} {self.name}")
      else:
        print(f"{fg.cyan}END getPrices nothing sent {prices.get('asset', '')} {fg.rs} {self.name}")
    return prices