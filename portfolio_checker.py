import asyncio, threading

from src.stock.lib.broker_api.announcement import Announcement
from timeit import *
import os, math, subprocess, time
import mplfinance as mpf
from alpaca_trade_api.rest import *
from src.stock.repos.report_model import *
from src.stock.repos.price_database import *
from src.stock.calculate.calculations import Calculations
from src.stock.values.report import Entry, Report
from src.stock.repos.price_database import PricesDatabase
from src.stock.calculate.momentum import Momentum
from src.stock.values.order import Order
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from src.stock.repos.report_database import ReportDatabase
from src.stock.broker import Broker
from src.stock.values.portfolio import Portfolio
import janus, math
from src.stock.repos.announcement_database import AnnouncementDatabase
from sty import fg
from src.stock.values.strategy import *

account_info1 = {
  "public_key": 'PKG77R4EUWQ76WC12PI5',
  "private_key": 'YvNim9ia5ov4oJ7WHLv6ElPYQMcMTZMMTP3pLjtp',
  "api_link": 'https://paper-api.alpaca.markets'
}

announcement_database = AnnouncementDatabase()
report_database = ReportDatabase(False)
broker = Broker(account_info1)

def dfToDict(date, prices):
  return {
    "open": prices['open'][date],
    "close": prices['close'][date],
    "high": prices['high'][date],
    "low": prices['low'][date]
  }

def getAllStrategies():
  strategies = []

  for filter in list(Filter)[:-4]:
    for initial_sorting in list(Sorting):
      for cutoff in list(Cutoff):
        for secondary_sorting in list(Sorting):
          for portfolio_size in list(PortfolioSize):
            strategy = Strategy([filter, Filter.TREND_UP, Filter.COLUMN_UP], initial_sorting, cutoff, secondary_sorting, portfolio_size)
            strategies.append(strategy)
  
  return strategies



async def main():
  strategies = getAllStrategies()
  #strategy = Strategy([Filter.TREND_UP], Sorting.ACCELERATION_UP, Cutoff.FIFTY, Sorting.TWO_YEAR_MOMENTUM_DOWN, PortfolioSize.SIX)

  now = datetime.fromisoformat("2022-05-18")
  # await checkStrategy(now, strategy)
  results = []
  announcements = announcement_database.listAnnouncements()
  exclude_stocks = [announcement.initiating_symbol for announcement in announcements if announcement.target_symbol != '']
  exclude_stocks += [announcement.target_symbol for announcement in announcements if announcement.target_symbol != '' and not announcement.target_symbol in exclude_stocks]

  data = {}
  print("Getting reports")
  # strategy = Strategy([Filter.RSI14_MAX, Filter.TREND_UP, Filter.COLUMN_UP], Sorting.ACCELERATION_UP, Cutoff.TEN, Sorting.RSI28_DOWN, PortfolioSize.TWO)
  # highest = [strategy]
  for strategy in strategies:
    report = report_database.getReports(now, strategy, exclude_stocks)
    print("Got Report")
    data[strategy] = report
    result = await checkStrategy(now, strategy, report)
    print(strategy)
    print("")
    results.append(result)
  
  highest = max(results, key=lambda result: result[1])
  print(highest[0], highest[1])
  report = report_database.getReports(now, highest[0], exclude_stocks)
  await checkStrategy(now, highest[0], report)

def getNewAmount(amount, announcement: Announcement):
  new_rate = announcement.new_rate
  old_rate = announcement.old_rate
  result = math.floor((new_rate / old_rate) * amount)
  print(announcement.target_symbol, result)
  return result

async def checkStrategy(date, strategy, report):
  api = broker.api

  #original_order_stocks = [entry.stock for entry in report.entries if not announcement_database.exist(entry.stock)]
  #stocks = [entry.stock for entry in report.entries if not announcement_database.exist(entry.stock)]
  stocks = report.stocks
  queue = janus.Queue()
  price_data = {}

  for stock in stocks:
    data = api.get_bars(stock, TimeFrame.Day, "2022-05-25", "2022-05-26", adjustment='raw')
    price_data[stock] = data[-1].c

  sum_profit = 0
  info = []
  percents = []
  for entry in report.entries:
    stock_amount = 100
    announcement = announcement_database.get(entry.stock)
    if announcement != None:
      new_stock_amount = getNewAmount(stock_amount, announcement)
    else:
      new_stock_amount = stock_amount
    
    if announcement != None:
      continue

    recent_price = price_data[entry.stock]
    buy_price = entry.close_price * stock_amount
    sell_price = recent_price * new_stock_amount
    profit = sell_price - buy_price
    sum_profit += profit
    percent = (profit/buy_price)*100
    #print(entry, round(profit,2), round(percent,3))
    info.append([entry, profit, percent, recent_price])
    percents.append(percent)
  
  info = sorted(info, key=lambda foo: foo[2], reverse=True)
  for res in info:
    print(res[0], round(res[1], 2), round(res[2], 3), res[3])
  
  percent_profit = round(sum(percents), 2)
  if percent_profit > 0:
    color = fg.green
  else:
    color = fg.red

  print("Percent Profit", f"{color}{percent_profit}{fg.rs}")
  print(stocks)
  return (strategy, percent_profit)

asyncio.run(main())