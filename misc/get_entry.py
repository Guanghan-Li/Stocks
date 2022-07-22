import asyncio, threading
import txaio
txaio.use_asyncio()

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
component = Component(transports=url, realm=realmv)

account_info1 = {
  "public_key": 'PKG77R4EUWQ76WC12PI5',
  "private_key": 'YvNim9ia5ov4oJ7WHLv6ElPYQMcMTZMMTP3pLjtp',
  "api_link": 'https://paper-api.alpaca.markets'
}
broker = Broker(account_info1)

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

def prepareData(prices):
    price_data = []
    for price in prices:
        new_price = {
            'h': price['high'],
            'l': price['low']
        }
        price_data.append(new_price)
    return price_data

@component.on_join
async def joined(session: Session, details):
    queue = janus.Queue()
    report_database = ReportDatabase(report_proxy, None)
    all_entries = []
    wamp_session = session
    print("Connected")
    stock = "AMC"
    now = datetime.fromisoformat('2022-01-21')
    end_date = now.strftime("%Y-%m-%d")
    data = broker.getPriceData([stock], queue.sync_q, "", end_date = end_date )
    prices = getTwoYearPrices(stock, data, now)
    price_data = prepareData(prices)
    result = await session.call('my.func', stock, price_data)
    print(result)
    column = result['column']
    trend = result['trend']
    entry = report_database.generateEntry(stock, prices, now)
    entry.column = column
    entry.trend = trend
    print(entry)
    session.leave()

async def main():
  await component.start(loop=asyncio.get_event_loop())


asyncio.run(main())