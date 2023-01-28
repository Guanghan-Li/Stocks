from timeit import *
from time import sleep
import os, math, subprocess, time
import mplfinance as mpf
from alpaca_trade_api.rest import *
import alpaca_trade_api.rest_async
from peewee import *
from pandas import DataFrame
from src.stock.calculate.calculations import Calculations
from src.stock.values.report import Entry
from src.stock.repos.price_database import PricesDatabase
from src.stock.calculate.momentum import Momentum
from src.stock.values.order import Order
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from src.stock.repos.report_database import ReportDatabase
from src.stock.values.prices import Prices, Price
from src.stock.lib.log.log import Log

class Broker:
  def __init__(self, account_info, log=False):
    self.api = REST(
      account_info['public_key'],
      account_info['private_key'],
      account_info['api_link']
    )
    self.async_api = alpaca_trade_api.rest_async.AsyncRest(
      account_info['public_key'],
      account_info['private_key'],
      account_info['api_link']  
    )
    self.log = Log(can_log=log)

  def getAllAssets(self):
    active_assets = self.api.list_assets(status='active')
    nasdaq_assets = [a.symbol for a in active_assets if a.exchange == 'NASDAQ']
    nyse_assets = [a.symbol for a in active_assets if a.exchange == 'NYSE']
    #every_asset = [a.symbol for a in active_assets]
    return nasdaq_assets+nyse_assets

  now = datetime.now()

  def getPriceData(self, asset, start_date: datetime, end_date: datetime, thread_name=""):
    self.log.info("Getting Price data for", asset)
    start_date = start_date.strftime("%Y-%m-%d")
    end_date = end_date.strftime("%Y-%m-%d")

    whole_data = self.api.get_bars(asset, TimeFrame.Day, start_date, end_date, adjustment='raw')
    prices = Prices.fromDataFrame(asset, whole_data.df)

    return prices
  
  async def getPrices(self, asset, start_date: datetime, end_date: datetime):
    start_date = start_date.strftime("%Y-%m-%d")
    end_date = end_date.strftime("%Y-%m-%d")

    whole_data = await self.async_api.get_bars_async(asset, "day", start_date, end_date, adjustment='raw')
    print(whole_data)
    prices = Prices.fromDataFrame(asset, whole_data.df)

    return prices

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


    for stock in stocks:
      percentage = round((round(stock.current_momentum,3) * 1000) / sum_momentum, 4)
      funds = buying_power * percentage
      amount = int(funds // stock.price)
      self.log.info(stock.stock, amount, amount * stock.price)

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
    self.log.info("Purchased:", entry.stock)

  def sell(self, order, entry):
    self.api.submit_order(
        symbol=order.stock,
        qty=order.amount,
        side='sell',
        type='market',
        time_in_force='gtc'
    )
    self.log.info("Sold:", entry.stock)

  def executeOrders(self, orders, entry):
    for order in orders:
      if order.position == "buy":
        self.buy(order, entry)
      elif order.position == 'sell':
        self.sell(order, entry)