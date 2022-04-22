import asyncio, threading
from timeit import *
import os, math, subprocess, time
import mplfinance as mpf
from alpaca_trade_api.rest import *
from autobahn.asyncio.component import Component, run, Session
from torch import Size
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

from values.strategy import *

account_info1 = {
  "public_key": 'PKG77R4EUWQ76WC12PI5',
  "private_key": 'YvNim9ia5ov4oJ7WHLv6ElPYQMcMTZMMTP3pLjtp',
  "api_link": 'https://paper-api.alpaca.markets'
}

def dfToDict(date, prices):
  return {
    "open": prices['open'][date],
    "close": prices['close'][date],
    "high": prices['high'][date],
    "low": prices['low'][date]
  }

def getAllStrategies():
  strategies = []



async def main():
  strategy = Strategy(
    [Filter.ACCELERATION_MAX],
    Sorting.RSI14_UP,
    Cutoff.FIFTY,
    Sorting.RSI28_UP,
    PortfolioSize.FOUR
  )

  print(Filter.ACCELERATION_MAX.name)

  now = datetime.fromisoformat("2021-10-13")
  strategies = [strategy]

  results = []
  for strategy in strategies:
    result = await checkStrategy(now, strategy)
    results.append(result)
  
  print(results)


async def checkStrategy(date, strategy):
  report_database = ReportDatabase(report_proxy, None)

  broker = Broker(account_info1)
  api = broker.api
  report = report_database.getReports(date, strategy)
  original_order_stocks = [entry.stock for entry in report.entries]
  stocks = [entry.stock for entry in report.entries]
  queue = janus.Queue()
  price_data = {}
  for stock in stocks:
    data = api.get_bars(stock, TimeFrame.Day, "2021-11-10", "2021-11-11", adjustment='raw')
    price_data[stock] = data[-1].c

  sum_profit = 0
  info = []
  percents = []
  for entry in report.entries:
    recent_price = price_data[entry.stock]
    profit = recent_price - entry.close_price
    sum_profit += profit
    percent = (profit/entry.close_price)*100
    #print(entry, round(profit,2), round(percent,3))
    info.append([entry, profit, percent])
    percents.append(percent)
  
  info = sorted(info, key=lambda foo: foo[2], reverse=True)
  for res in info:
    print(res[0], round(res[1], 2), round(res[2], 3))
  
  percent_profit = round(sum(percents), 2)
  print("Percent Profit", percent_profit)
  print(original_order_stocks)
  return percent_profit

asyncio.run(main())