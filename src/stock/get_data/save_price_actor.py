from pykka import ThreadingActor
from repos.price_database import PricesDatabase
from repos.price_model import price_proxy
from sty import fg

class SavePriceActor(ThreadingActor):
  def __init__(self, name):
    super().__init__()
    print(f"{fg.li_cyan}STARTING{fg.rs} {name}")
    self.name = name
    self.prices_database = PricesDatabase(price_proxy, "Data/prices.db")
    

  def savePrice(self, message):
    print(f"{fg.li_red}START savePrice{fg.rs} {self.name}")
    asset = message["asset"]
    data = message["data"]
    self.prices_database.setupPrices(asset, data)
    print(f"{fg.li_red}END savePrice{fg.rs} {self.name}")
  
  def on_stop(self):
    self.prices_database.database.close()