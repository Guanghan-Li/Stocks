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

async def main():
  report_database = ReportDatabase(report_proxy, None)

  broker = Broker(account_info1)
  api = broker.api

  now = datetime.fromisoformat("2021-12-15")
  report = report_database.getReports(now, 300)
  original_order_stocks = [entry.stock for entry in report.entries]
  report.entries = sorted(report.entries, key=lambda entry: entry.prev_momentum, reverse=False)
  report.entries = report.entries[:5]
  stocks = [entry.stock for entry in report.entries]
  queue = janus.Queue()
  price_data = {}
  for stock in stocks:
    data = api.get_bars(stock, TimeFrame.Day, "2022-01-27", "2022-01-28", adjustment='raw')
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
  
  print("Percent Profit", round(sum(percents), 2))
  print(original_order_stocks)

asyncio.run(main())