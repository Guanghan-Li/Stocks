import asyncio, threading
from timeit import *
import os, math, subprocess, time
from tracemalloc import start
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
#import signal
from sty import fg
import pandas as pd
import pykka
from pykka import *
import txaio
txaio.use_asyncio()
from autobahn.asyncio.component import Component
from autobahn.asyncio.component import run
import queue, requests, pytz
from requests.auth import HTTPBasicAuth
from adjust_prices import AdjustPrice

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


class Helpers(ThreadingActor):
  def __init__(self):
    super().__init__()

  #@timeFunc
  def getTwoYearPrices(self, stock, prices: DataFrame, orig_date: datetime):
    date_format = "%Y-%m-%d"
    start = orig_date - relativedelta(weeks=104)
    date = orig_date.strftime(date_format)
    start = start.strftime(date_format)
    prices.index = pd.to_datetime(prices.index, format=date_format)
    prices = prices.loc[str(start):str(date)]
    dates = [str(date) for date in prices['open'].keys()]
    data = [dfToDict(date, prices) for date in dates]
    return data
  
  def getTwoYearPrices2(self, stock, prices:list[dict], orig_date: datetime):
    date_format = "%Y-%m-%d"
    start = orig_date - relativedelta(weeks=104)
    date = orig_date.strftime(date_format)
    str_start = start.strftime(date_format)
    output = []
    for price in prices:
      price_date = price["date"]
      start = start.replace(tzinfo=pytz.UTC)
      price_date = price_date.replace(tzinfo=pytz.UTC)
      orig_date = orig_date.replace(tzinfo=pytz.UTC)
      if price_date >= start and price_date <= orig_date:
        output.append(price)
    return output


class BrokerActor(ThreadingActor):
  def __init__(self, name, save_price_actor, gen_report_actor):
    super().__init__()
    print(f"{fg.yellow}STARTING{fg.rs} {name}")
    self.name = name
    self.save_price_actor: SavePriceActor = save_price_actor
    self.gen_report_actor: GenerateReportActor = gen_report_actor
    self.ap = AdjustPrice()
  
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

    if len(data) < 980:
      return None

    self.prices_database.setupPrices(asset, data)
    print(f"{fg.li_red}END savePrice{fg.rs} {self.name}")
  
  def on_stop(self):
    self.prices_database.database.close()


class GenerateReportActor(ThreadingActor):
  def __init__(self, name, save_report_actor):
    super().__init__()
    self.name = name
    Helpers.use_deamon_thread = True
    self.helpers = Helpers.start().proxy()
    self.save_report_actor: ReportSaveActor = save_report_actor
    PNFActor.use_deamon_thread = True
    self.pnf_actor = PNFActor.start("PNF Actor").proxy()

  def on_failure(self, exception_type, exception_value: BaseException, traceback) -> None:
      print("GenerateReport Failed:", exception_type)

  async def generateReport(self, message):
    asset = message["asset"]
    data = message["data"]
    end_date = message["date"]
    start_date = datetime(2018, 6, 22)
    now = datetime.fromisoformat(end_date)
    weeks = 2
    entry = 1

    if len(data) < 980:
      return None

    while weeks > 0 and entry != None:
      weeks -= 1
      now -= relativedelta(days=7)
      prices = self.helpers.getTwoYearPrices2(asset, data, now).get()
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


class ReportSaveActor(ThreadingActor):
  def __init__(self, name):
    super().__init__()
    self.name = name
    self.report_database = ReportDatabase(report_proxy, "Data/reports.db")
  
  def saveReport(self, entry):
    print(f"{fg.li_blue}START saveReport{fg.rs} {self.name}")
    self.report_database.saveEntry(entry)
    print(f"{fg.li_blue}END saveReport{fg.rs} {self.name}")
  
  def on_failure(self, exception_type, exception_value: BaseException, traceback) -> None:
      print(exception_type, exception_value)
      #self.stop()

class PNFActor(ThreadingActor):
  def __init__(self, name):
    super().__init__()
    self.name = name

  async def onJoin(self, session, details):
    print("JOINED WAMP")
    self.session = session
    message = {"stop": False}

    while not message["stop"]:
      message: dict = self.o_queue.get()
      message.setdefault("stop", False)
      if message["action"] == "update":
        price_data = message["prices"]
        stock = message["stock"]

        print("CALL START")
        result = await self.session.call('my.func', stock, price_data)
        print("CALL END")
        column = result['column']
        trend = result['trend']
        i_message = {"action": "pnf", "trend": trend, "column": column}
        self.i_queue.put(i_message)

  def updateReport(self, stock, prices):
    print("SENT MESSAGE", stock)
    self.o_queue.put({"action": "update", "stock": stock, "prices": prices}, block=True)
    result = self.i_queue.get()
    trend, column = result["trend"], result["column"]
    print(trend, column, stock)
    return (trend, column)

  def on_start(self):
    print("Starting", self.name)
    self.loop = asyncio.new_event_loop()
    asyncio.set_event_loop(self.loop)
    print("HELLO FROM HERE")
    self.o_queue = queue.Queue()
    self.i_queue = queue.Queue()
    thread = threading.Thread(target=self.runComp, daemon=True)
    thread.start()

  def runComp(self):
    print("Run comp")
    self.loop2 = asyncio.new_event_loop()
    asyncio.set_event_loop(self.loop2)
    url = os.environ.get('CBURL', u'ws://localhost:8080/ws')
    realmv = os.environ.get('CBREALM', u'realm1')
    self.component = Component(transports=url, realm=realmv)
    self.component.on("join", self.onJoin)
    run([self.component])
  
  def foo(self):
    print("Foo")
    return 1

  def on_stop(self):
    self.component.stop()
    self.loop.stop()

  def on_failure(self, exception_type, exception_value: BaseException, traceback) -> None:
      print("THIS DIED")

def killed(sig, frame):
  pykka.ActorRegistry.stop_all(timeout=2.0)

# signal.signal(signal.SIGINT, killed)
# signal.signal(signal.SIGTERM, killed)
# signal.signal(signal.SIGABRT, killed)

async def foo(session):
  print("HELLO")

async def main():
  tasks = []
  loop = asyncio.get_event_loop()

  for i in range(10):
    SavePriceActor.use_deamon_thread = True
    BrokerActor.use_deamon_thread = True
    GenerateReportActor.use_deamon_thread = True
    ReportSaveActor.use_deamon_thread = True
    save_price = SavePriceActor.start(f"Save Price {i}").proxy()

    save_report = ReportSaveActor.start(f"Save Report {i}").proxy()
    gen_report_actor = GenerateReportActor.start(f"GenReport {i}", save_report).proxy()
    broker_actor = BrokerActor.start(f"Broker {i}", save_price, gen_report_actor).proxy()
    task = loop.create_task(broker_actor.getPrices(amount[i], brokers[i//2]).get())
    tasks.append(task)

  await asyncio.wait(tasks)



asyncio.run(main())

