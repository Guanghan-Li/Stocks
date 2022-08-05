from pandas import DataFrame
import thespian
from thespian.actors import *
from sty import fg
from src.stock.actors.messages import *
from src.stock.adjust_prices import AdjustPrice
from src.stock.broker import Broker

class BrokerActor(ActorTypeDispatcher):
  def __init__(self):
    self.ap = AdjustPrice()
  
  def receiveMsg_SetupMessage(self, message: SetupMessage, sender):
    self.save_price_actor = message.info.get("save_price_actor", None)
    self.gen_report_actor = message.info.get("gen_report_actor", None)
    self.name = message.info.get("name", "Broker")
    self.broker = Broker(message.info.get("account_info", None))
    print(f"Got SetupMessage: {self.name}")
    self.send(sender, 0)

  def receiveMsg_GetPriceMessage(self, message: GetPriceMessage, sender):
    print("Got message", message.assets)
    asset_group = message.assets
    #start_date = datetime(2018, 6, 8)
    #end_date = datetime(2022, 6, 15)

    start_date = message.start_date
    end_date = message.end_date

    for asset in asset_group:
      print(f"{fg.green}START getPrices{fg.rs} {self.name}")
      prices = self.broker.getPriceData(asset, start_date=start_date, end_date=end_date, thread_name=self.name)
      #prices = self.ap.applyAllAnnouncements(asset, prices)
      if not prices["data"].empty:
        # TODO check amount of prices here
        #await self.gen_report_actor.generateReport(prices).get()
        save_price_message = SavePriceMessage(asset, prices["data"], sender)
        self.send(self.save_price_actor, save_price_message)
      else:
        print(f"{fg.cyan}END getPrices nothing sent {prices.get('asset', '')} {fg.rs} {self.name}")
