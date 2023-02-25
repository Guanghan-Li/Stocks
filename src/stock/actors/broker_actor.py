from pandas import DataFrame
import thespian
from thespian.actors import *
from sty import fg
from src.stock.actors.messages import *
from src.stock.adjust_prices import AdjustPrice
from src.stock.broker import Broker
from src.stock.values.prices import Prices
from src.stock.lib.log.log import Log
from src.stock.values.tasks import Tasks, Task
from datetime import datetime

class BrokerActor(ActorTypeDispatcher):
  def __init__(self):
    self.ap = AdjustPrice()
  
  def receiveMsg_SetupMessage(self, message: SetupMessage, sender):
    self.log = Log(message.log)
    self.save_price_actor = message.info.get("save_price_actor", None)
    self.gen_report_actor = message.info.get("gen_report_actor", None)
    self.channel = message.info.get("channel", None)
    self.name = message.info.get("name", "Broker")
    self.broker = Broker(message.info.get("account_info", None))
    self.log.info(f"BrokerActor Got SetupMessage: {self.name}")
    self.send(sender, 0)

  def receiveMsg_GetPriceMessage(self, message: GetPriceMessage, sender):
    self.log.info("BrokerActor {self.name} getting prices")
    asset_group = message.assets
    #start_date = datetime(2018, 6, 8)
    #end_date = datetime(2022, 6, 15)

    start_date = message.start_date
    end_date = message.end_date

    new_task = Task.create(self.name, None)
    #self.send(self.task_manager, TaskCreate(new_task))

    for asset in asset_group:
      sub_task = Task.create(self.name, asset)
      #self.send(self.task_manager, TaskCreate(new_task))
      start = datetime.now()
      self.log.info(f"{fg.green}START getPrices{fg.rs} {self.name}")
      prices: Prices = self.broker.getPriceData(asset, start_date=start_date, end_date=end_date, thread_name=self.name)

      #prices = self.ap.applyAllAnnouncements(asset, prices)
      if (not prices.empty) and prices.amountOfYears() >= 4:
        if self.save_price_actor is not None:
          save_price_message = SavePriceMessage(asset, prices, sender)
          self.send(self.save_price_actor, save_price_message)
        if self.gen_report_actor is not None:
          gen_report_message = GenerateReportMessage(asset, prices, sender)
          self.send(self.gen_report_actor, gen_report_message)
        end = datetime.now()
        time_spent = (end-start).microseconds*0.001
        self.log.info(f"{fg.green}END getPrices{fg.rs} {self.name} | asset: {asset} | took: {time_spent}")
      else:
        end = datetime.now()
        time_spent = (end-start).microseconds*0.001
        self.log.info(f"{fg.green}END getPrices nothing sent {prices.symbol} {fg.rs} {self.name} | amount {len(prices)} | years: {prices.amountOfYears()} | took: {time_spent}")
      
      #self.send(self.task_manager, TaskFinishedMessage(sub_task.task_id, self.name))
    
    #self.send(self.task_manager, TaskFinishedMessage(new_task.task_id, self.name))
    
