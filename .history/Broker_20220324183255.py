from timeit import *
from time import sleep
import os, math, subprocess, time
import mplfinance as mpf
from alpaca_trade_api.rest import *
from repos.report_model import *
from repos.price_database import *
from peewee import *
from pandas import DataFrame
from Calculate.calculations import Calculations
from values.report import Entry
from repos.price_database import PricesDatabase
from Calculate.momentum import Momentum
from values.order import Order
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from repos.report_database import ReportDatabase

class Broker:
  def __init__(self, account_info):
    self.api = REST(
      account_info['public_key'],
      account_info['private_key'],
      account_info['api_link']
    )

  def getAllAssets(self):
    active_assets = self.api.list_assets(status='active')
    nasdaq_assets = [a.symbol for a in active_assets if a.exchange == 'NASDAQ']
    nyse_assets = [a.symbol for a in active_assets if a.exchange == 'NYSE']
    #every_asset = [a.symbol for a in active_assets]
    return nasdaq_assets+nyse_assets

  now = datetime.now()

  def getPriceData(self, all_assets, price_queue, report_queue, thread_name, start_date: datetime, end_date: datetime):
    start_date = start_date.strftime("%Y-%m-%d")
    end_date = end_date.strftime("%Y-%m-%d")
    for asset in all_assets:
      whole_data = None

      try:
       # print(f"{thread_name} getting prices for {asset}")
        whole_data = self.api.get_bars(asset, TimeFrame.Day, start_date, end_date, adjustment='raw').df
        print("Got asset", asset)
        message = {
          "asset": asset,
          "data": whole_data,
          "date": end_date
        }
        price_queue.put(message)
        report_queue.put(message)
        price_queue.done()
        price_queue.done()
      except:
        print(f"{thread_name} CANNOT GET ASSET:", asset)
  
    
    sleep(0.01)
    return whole_data

  def getLongStocks(self, report, amount):
    report.sort(key=lambda entry: entry.acceleration, reverse = True)
    stocks = report[:20]
    stocks.sort(key=lambda entry: entry.current_momentum, reverse = True)
    stocks = stocks[:amount]
    return stocks

  def getShortStocks(self, report, amount):
    report.sort(key=lambda entry: entry.acceleration)
    stocks = report[:20]
    stocks.sort(key=lambda entry: entry.current_momentum)
    stocks = stocks[:amount]

  def getOrders(self, report, buying_power):
    long_stocks = self.getLongStocks(report, 5)
    #short_stocks = getShortStocks(report, 2)
    short_stocks = []
    stocks = long_stocks + short_stocks
    sum_momentum = sum([round(abs(stock.current_momentum), 3) * 1000 for stock in stocks])

    stocks_to_order = []
    buying_power = buying_power // 3

    print()

    for stock in stocks:
      percentage = round((round(stock.current_momentum,3) * 1000) / sum_momentum, 4)
      funds = buying_power * percentage
      amount = int(funds // stock.price)
      print(stock.stock, amount, amount * stock.price)

      if stock in long_stocks:
        order = Order(stock.stock, amount, 'buy')
      elif stock in short_stocks:
        order = Order(stock.stock, amount, 'sell')

      stocks_to_order.append(order)

    return stocks_to_order

  def buy(self, order, entry):
    self.api.submit_order(
        symbol=order.stock,
        qty=order.amount,
        side='buy',
        type='market',
        time_in_force='gtc'
    )
    print("Purchased:", entry.stock)

  def sell(self, order, entry):
    self.api.submit_order(
        symbol=order.stock,
        qty=order.amount,
        side='sell',
        type='market',
        time_in_force='gtc'
    )
    print("Sold:", entry.stock)

  def executeOrders(self, orders, entry):
    for order in orders:
      if order.position == "buy":
        self.buy(order, entry)
      elif order.position == 'sell':
        self.sell(order, entry)