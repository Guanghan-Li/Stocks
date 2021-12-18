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



account_info1 = {
      "public_key": 'PKG77R4EUWQ76WC12PI5',
      "private_key": 'YvNim9ia5ov4oJ7WHLv6ElPYQMcMTZMMTP3pLjtp',
      "api_link": 'https://paper-api.alpaca.markets'
}

account_info2 = {
  "public_key": "PKAJ6YB539JWBMJT81Q8",
  "private_key": "clxZoMjA1rc7RFA42aFcbnAwggp95buT1bwGCHxe",
  "api_link": "https://paper-api.alpaca.markets"
}

broker = Broker(account_info1)
broker2 = Broker(account_info2)

assets = broker.getAllAssets()
#assets2 = broker2.getAllAssets()
amount = list(zip(*[iter(assets)]*(len(assets)//10)))

#amount = list(zip(*[iter(assets)]*(len(assets)//1)))


asset_group0 = amount[0]
asset_group1 = amount[1]
asset_group2 = amount[2]
asset_group3 = amount[3]
asset_group4 = amount[4]
asset_group5 = amount[5]
asset_group6 = amount[6]
asset_group7 = amount[7]
asset_group8 = amount[8]
asset_group9 = amount[9]

# asset_group0 = amount1[0]
# asset_group1 = amount2[1]

def thread1Main():
  loop = asyncio.new_event_loop()
  asyncio.set_event_loop(loop)
  pd = PricesDatabase(DatabaseProxy(), db_path="Data/prices2.db")
  pd.setupPrices(broker2.api, asset_group1[:6], thread_name="Thread 1")

def thread2Main():
  loop = asyncio.new_event_loop()
  asyncio.set_event_loop(loop)

def main():
  loop = asyncio.get_event_loop()
  pd = broker.getPriceData(['AAPL'])
  print(pd)
  #prices_database = PricesDatabase(price_proxy, "Data/prices.db")
  #prices_database.setupPrices(broker.api, asset_group0[:6], thread_name="Thread 0")

# thread = threading.Thread(target=secondMain)
# thread.setDaemon(True)
# thread.start()

# thread2 = threading.Thread(target=main)
# thread2.setDaemon(True)
# thread2.start()
main()
#main()
#prices_database.setupPrices(broker.api, assets)
