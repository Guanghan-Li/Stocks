import thespian
from thespian.actors import *
from sty import fg

class SavePriceActor(ActorTypeDispatcher):
  def __init__(self, name):
    super().__init__()
    print(f"{fg.li_cyan}STARTING{fg.rs} {name}")
    self.name = name
    self.prices_database = PricesDatabase(price_proxy, "Data/prices.db")

  def receiveMsg_SetupMessage(self, message, sender):
    pass

  def receiveMsg_SavePriceMessage(self, message, sender):
    pass

  def savePrice(self, message):
    print(f"{fg.li_red}START savePrice{fg.rs} {self.name}")
    asset = message["asset"]
    data = message["data"]

    if len(data) < 980:
      return None

    self.prices_database.setupPrices(asset, data)
    print(f"{fg.li_red}END savePrice{fg.rs} {self.name}")
  
  def on_stop(self):
    self.prices_database.database.close()