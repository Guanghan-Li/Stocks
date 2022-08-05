import asyncio, threading
from timeit import *
import os, math, subprocess, time
import mplfinance as mpf
from alpaca_trade_api.rest import *
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from pandas import DataFrame
from psycopg2 import Timestamp
from src.stock.broker import Broker
#import signal
from sty import fg
import txaio
txaio.use_asyncio()
from autobahn.asyncio.component import Component
from autobahn.asyncio.component import run
import queue, requests, pytz
from requests.auth import HTTPBasicAuth

from thespian.actors import *
from src.stock.actors.broker_actor import BrokerActor
from src.stock.values.prices import Prices, Price
from src.stock.actors.save_price import SavePriceActor
from src.stock.actors.messages import *

#personal
account_info1 = {
      "public_key": 'PKG77R4EUWQ76WC12PI5',
      "private_key": 'YvNim9ia5ov4oJ7WHLv6ElPYQMcMTZMMTP3pLjtp',
      "api_link": 'https://paper-api.alpaca.markets'
}
#08
account_info2 = {
  "public_key": "PKAJ6YB539JWBMJT81Q8",
  "private_key": "clxZoMjA1rc7RFA42aFcbnAwggp95buT1bwGCHxe",
  "api_link": "https://paper-api.alpaca.markets"
}
#02
account_info3 = {
  "public_key": "PKZBZND7F6PH39SMHJPQ",
  "private_key": "2gENBEvKNSEss7zWkY8N290eIANnv32iUeuHPRFy",
  "api_link": "https://paper-api.alpaca.markets"
}
#03
account_info4 = {
  "public_key": "PKQMDMXG2T2FMQ8AZOY5",
  "private_key": "YVdUWYT7hTVPxpkuwDFi07i3Ib8E1AceHPZha46a",
  "api_link": "https://paper-api.alpaca.markets"
}

account_info5 = {
  "public_key": "PKP33J9QMA0IK97MBED5",
  "private_key": "D2cP3slrGwPm3MeAdQdar2MawUNmYMwaK1Wq99lv",
  "api_link": "https://paper-api.alpaca.markets"
}


broker = Broker(account_info1)
prices: Prices = broker.getPriceData("AAPL", datetime(2021, 5, 20), datetime(2022,5,22))
foo = prices.splitByMonth()
for a in foo:
  print(a)
print()
quit()

assets = broker.getAllAssets()
asset_amount = len(assets)
#assets2 = broker2.getAllAssets()
amount = list(zip(*[iter(assets)]*(len(assets)//10)))


accounts = [account_info1, account_info2, account_info3, account_info4, account_info5]

def killed(sig, frame):
  pass
# signal.signal(signal.SIGINT, killed)
# signal.signal(signal.SIGTERM, killed)
# signal.signal(signal.SIGABRT, killed)

def main():
  asys = ActorSystem("multiprocQueueBase")
  broker_actor = asys.createActor(BrokerActor)
  save_price_actor = asys.createActor(SavePriceActor)
  setup_message = SetupMessage({"name": "Broker 1", "account_info": account_info1, "save_price_actor": save_price_actor})
  asys.ask(broker_actor, setup_message)
  asys.ask(save_price_actor, SetupMessage({"name": "Save Price Actor 1"}))

  get_message = GetPriceMessage(["AAPL"], datetime(2022, 7, 25), datetime(2022,7,26))
  asys.tell(broker_actor, get_message)

  asys.listen()
  asys.shutdown()

if __name__ == "__main__":
  main()