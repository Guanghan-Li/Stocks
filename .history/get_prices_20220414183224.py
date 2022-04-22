import asyncio, threading
from timeit import *
import os, math, subprocess, time
import mplfinance as mpf
from alpaca_trade_api.rest import *
from repos.report_model import *
from repos.price_database import *
from Calculate.calculations import Calculations
from values.report import Entry, Report
from repos.price_database import PricesDatabase
from Calculate.momentum import Momentum
from values.order import Order
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from repos.report_database import ReportDatabase
from broker import Broker
from values.portfolio import Portfolio
import janus
from sty import fg
import pandas as pd
import pykka
from pykka import *

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
broker2 = Broker(account_info2)
broker3 = Broker(account_info3)
broker4 = Broker(account_info4)
broker5 = Broker(account_info5)


count = 0

assets = broker.getAllAssets()
asset_amount = len(assets)
#assets2 = broker2.getAllAssets()
amount = list(zip(*[iter(assets)]*(len(assets)//10)))

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

brokers = [broker,broker2,broker3,broker4,broker5]

def timeFunc(func):
  def wrapper(*args, **kwargs):
    start_time = datetime.now().timestamp()
    value = func(*args, **kwargs)
    end_time = datetime.now().timestamp()
    print(f"{fg.yellow}TIME:{fg.rs} {func.__name__} took {end_time - start_time}")
    return value
  return wrapper


def dfToDict(date, prices):
  return {
    "date":date,
    "open": prices['open'][date],
    "close": prices['close'][date],
    "high": prices['high'][date],
    "low": prices['low'][date]
  }

@timeFunc
def getTwoYearPrices(stock, prices: DataFrame, orig_date: datetime):
  date_format = "%Y-%m-%d"
  start = orig_date - relativedelta(weeks=104)
  date = orig_date.strftime(date_format)
  start = start.strftime(date_format)
  prices.index = pd.to_datetime(prices.index, format=date_format)
  prices = prices.loc[str(start):str(date)]
  dates = [str(date) for date in prices['open'].keys()]
  data = [dfToDict(date, prices) for date in dates]
  return data


class BrokerActor(ThreadingActor):
  def __init__(self, name, save_price_actor):
    super().__init__()
    print(f"{fg.yellow}STARTING{fg.rs} {name}")
    self.name = name
    self.save_price_actor: SavePriceActor = save_price_actor
    #self.gen_report_actor = gen_report_actor
  
  def getPrices(self, asset_group: list[str], broker: Broker):
    start_date = datetime(2018, 2, 21)
    end_date = datetime(2022, 2, 23)
    for asset in asset_group:
      print(f"{fg.green}START getPrices{fg.rs} {self.name}")
      prices = broker.getPriceData(asset, start_date=start_date, end_date=end_date, thread_name=self.name)
      self.save_price_actor.savePrice(prices).get()
      print(f"{fg.green}END getPrices{fg.rs} {self.name}")
    return prices


def createPriceSaveThreadFunc(thread_name, asset_amount):
  def threadFunc(save_price_queue):
    prices_database = PricesDatabase(price_proxy, "Data/prices.db")
    print(f"Starting {thread_name}")
    for i in range(asset_amount):
      print(i, f"{thread_name} getting data now...")
      message = save_price_queue.sync_q.get()
      asset = message["asset"]
      data = message["data"]
      print(i, f"{thread_name} GOT data for {asset}")
      prices_database.setupPrices(asset, data)
      save_price_queue.sync_q.task_done()
      print(f"{thread_name} done saving for {asset}")
  
  return threadFunc

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

# async def updateReport(session, stock, prices, current_date):
#   price_data = prepareData(prices)
#   if len(price_data) > 500:
#     result = await session.call('my.func', stock, price_data)
#     column = result['column']
#     trend = result['trend']
    
#     return (trend, column)
#   return None

def generateReportThreadFunc(thread_name):
  def threadFunc(gen_report_queue, save_report_queue):
    keepRunning = True

    while keepRunning:
      try:
        message = gen_report_queue.sync_q.get(timeout=1.0)
        print("MESSAGE"*3, type(message))
        asset = message["asset"]
        data = message["data"]
        end_date = message["date"]
        start_date = datetime(2018, 2, 21)

      except:
        keepRunning = False
        continue

      print(f"Processing {asset}")
      #result = await updateReport(wamp_session, asset, prices, now)
      now = datetime.fromisoformat(end_date)
      foo = True
      while start_date < now:
        prices = getTwoYearPrices(asset, data, now)
        try:
          entry = ReportDatabase.generateEntry(asset, prices, now)
          print(entry)
        except Exception as e:
          raise e
          keepRunning = False
          print(f"{fg.red}GETTING ENTRY FAILED{fg.rs}")
          entry = None

        now = now - relativedelta(days=7)
        print(f"{fg.cyan}NOW{fg.rs}", str(now))
        print("ENTRY", entry!=None, entry)
        if entry != None:
          print("SENDING", entry.stock)
          print(f"{fg.green}DATE:{fg.rs}", entry.date)
          #save_report_queue.sync_q.put(entry)
        foo = False

    print(f"{thread_name} DONE!")
    keepRunning = False
  return threadFunc

class GenerateReportActor(ThreadingActor):
  def __init__(self, name):
    super().__init__()
    self.name = name

  def generateReport(self, message):
    asset = message["asset"]
    data = message["data"]
    end_date = message["date"]
    start_date = datetime(2018, 2, 21)

class ReportSaveActor(ThreadingActor):
  def __init__(self, name):
    super().__init__()
    self.name = name
    self.report_database = ReportDatabase(report_proxy, "Data/reports.db")
  
  def saveReport(self, entry):
    self.report_database.saveEntry(entry)

async def main():
  for i in range(2):
    save_price = SavePriceActor.start(f"Save Price {i}").proxy()
    broker_actor = BrokerActor.start(f"Broker {i}", save_price).proxy()
    broker_actor.getPrices(amount[i], brokers[i//2])
  
  try:
    while True: pass
  except:
    pykka.ActorRegistry.stop_all(timeout=2.0)






# thread2 = threading.Thread(target=main)
# thread2.setDaemon(True)
# thread2.start()
asyncio.run(main())
#main()
#prices_database.setupPrices(broker.api, assets)
