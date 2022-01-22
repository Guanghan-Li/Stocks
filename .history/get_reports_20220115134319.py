import asyncio, threading
from timeit import *
import os, math, subprocess, time
import mplfinance as mpf
from alpaca_trade_api.rest import *
from autobahn.asyncio.component import Component, run, Session
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

url = os.environ.get('CBURL', u'ws://localhost:8080/ws')
realmv = os.environ.get('CBREALM', u'realm1')
print(url, realmv)
component = Component(transports=url, realm=realmv)

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

def dfToDict(date, prices):
  return {
    "date":date,
    "open": prices['open'][date],
    "close": prices['close'][date],
    "high": prices['high'][date],
    "low": prices['low'][date]
  }

def getTwoYearPrices(stock, prices: DataFrame, date: datetime):
  date_format = "%Y-%m-%d"
  start = date - relativedelta(weeks=104)
  date = date.strftime(date_format)
  start = start.strftime(date_format)
  prices.index = prices.index.strftime(date_format)
  prices = prices.loc[str(start):str(date)]
  dates = [str(date) for date in prices['open'].keys()]
  data = [dfToDict(date, prices) for date in dates]
  return data

def createThreadFunc(thread_name):
  def threadFunc(queue, asset_group, broker):
    # date_format = "%Y-%m-%d"
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    # now = datetime.now().strftime(date_format)
    broker.getPriceData(asset_group, queue.sync_q, thread_name)
    print(f"{thread_name} Done")
  
  return threadFunc

def prepareData(prices):
    price_data = []
    for price in prices:
        new_price = {
            'h': price['high'],
            'l': price['low']
        }
        price_data.append(new_price)
    return price_data

report_database = ReportDatabase(report_proxy, None)

async def updateReport(session, stock, prices, current_date):
  price_data = prepareData(prices)
  if len(price_data) > 500:
    result = await session.call('my.func', stock, price_data)
    column = result['column']
    trend = result['trend']
    
    return (trend, column)
  return None

wamp_session = None

@component.on_join
async def joined(session: Session, details):
    queue = janus.Queue()
    all_entries = []
    wamp_session = session..
    print("Connected")
    for i in range(10):
      threadFunc = createThreadFunc(f"Thread {i}")
      broker = brokers[i//2]
      thread = threading.Thread(target=threadFunc, args=[queue, amount[i], broker])
      thread.setDaemon(True)
      thread.start()

    for i in range(asset_amount):
      asset, data = await queue.async_q.get()
      now = datetime.now()
      prices = getTwoYearPrices(asset, data, now)
      result = await updateReport(wamp_session, asset, prices, now)
      if result != None and result == ("UP", "UP"):
        entry = report_database.generateEntry(asset, prices, now)
        print(all_entries)
        if entry != None:
          entry.column = result[1]
          entry.trend = result[0]
          report_database.saveEntry(entry)
          print(f"Saving {entry}")

async def main():
  await component.start(loop=asyncio.get_event_loop())
    # report_database.saveEntry(entry)
    # await prices_database.setupPrices(asset, data)




# thread2 = threading.Thread(target=main)
# thread2.setDaemon(True)
# thread2.start()
asyncio.run(main())
#main()
#prices_database.setupPrices(broker.api, assets)
