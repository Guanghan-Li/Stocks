import thespian
from thespian.actors import *
from sty import fg
from src.stock.repos.price_database import PricesDatabase, price_proxy
from src.stock.actors.messages import *

class SavePriceActor(ActorTypeDispatcher):
  def __init__(self):
    super().__init__()
    self.running_task = False

  def receiveMsg_SetupMessage(self, message: SetupMessage, sender):
    self.name = message.info["name"]
    print("Got Setup message", self.name)
    self.prices_database = PricesDatabase(price_proxy, "Data/prices.db")
    self.send(sender, 0)

  def receiveMsg_SavePriceMessage(self, message: SavePriceMessage, sender):
    print(f"{fg.li_red}START savePrice{fg.rs} {self.name}")
    print(message.data)
    self.prices_database.setupPrices(message.asset, message.data)


    print(f"{fg.li_red}END savePrice{fg.rs} {self.name}")
    self.send(message.sender, 0)
    
  
  def receiveMsg_TaskFinishedMessage(self, message: TaskFinishedMessage, sender):
    self.send(sender, self.running_task)