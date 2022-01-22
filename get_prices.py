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

account_info3 = {
  "public_key": "PKZBZND7F6PH39SMHJPQ",
  "private_key": "2gENBEvKNSEss7zWkY8N290eIANnv32iUeuHPRFy",
  "api_link": "https://paper-api.alpaca.markets"
}

account_info4 = {
  "public_key": "PKQMDMXG2T2FMQ8AZOY5",
  "private_key": "YVdUWYT7hTVPxpkuwDFi07i3Ib8E1AceHPZha46a",
  "api_link": "https://paper-api.alpaca.markets"
}

account_info5 = {
  "public_key": "PKJMSG502IDF8X3FZQPO",
  "private_key": "ovPyDR5oebP13KoDNolHXus2nLjHo4PERENLUNNj",
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

def createThreadFunc(thread_name):
  def threadFunc(queue, asset_group, broker):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    broker.getPriceData(asset_group, queue.sync_q, thread_name)
    print(f"{thread_name} Done")
  
  return threadFunc

async def main():
  queue = janus.Queue()

  for i in range(10):
    threadFunc = createThreadFunc(f"Thread {i}")
    broker = brokers[i//2]
    thread = threading.Thread(target=threadFunc, args=[queue, amount[i], broker])
    thread.setDaemon(True)
    thread.start()


  prices_database = PricesDatabase(price_proxy, "Data/prices3.db")
  for i in range(asset_amount):
    asset, data = await queue.async_q.get()
    asyncio.create_task(prices_database.setupPrices(asset, data))
    #await prices_database.setupPrices(asset, data)




# thread2 = threading.Thread(target=main)
# thread2.setDaemon(True)
# thread2.start()
asyncio.run(main())
#main()
#prices_database.setupPrices(broker.api, assets)
