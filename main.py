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

broker = Broker()
prices_database = PricesDatabase(price_proxy)
reports_database = ReportDatabase(report_proxy, prices_database)

start_time = time.time()


def rebalance(stocks_to_order):
  sell_orders = []
  buy_orders = []

  order_stocks = [order.stock for order in stocks_to_order]
  portfolio = broker.api.list_positions()
  position_stocks = [position.symbol for position in portfolio]

  for position in portfolio:
    if position.symbol not in order_stocks:
      order = Order(position.symbol, position.qty, 'sell')
      sell_orders.append(order)

    if position.symbol in order_stocks:
      stock = [order for order in stocks_to_order if order.stock == position.symbol][0]
      difference = stock.amount - int(position.qty)
      if (difference > 0):
        order = Order(position.symbol, difference, 'buy')
        buy_orders.append(order)
      else:
        order = Order(position.symbol, difference, 'sell')
        sell_orders.append(order)

  for position in stocks_to_order:
    if position.stock not in position_stocks:
      order = Order(position.stock, position.amount, 'buy')
      buy_orders.append(order)

  orders = sell_orders + buy_orders
  return orders
  
def getDecadeData(all_assets):
  for i in range(2017, 2021, 2):
    end_date = date(i+2, 11, 24).isoformat()
    start_date = date(i, 11, 23).isoformat()
    print("Getting prices for the date {} -> {}".format(start_date, end_date))
    prices_database.setupPrices(broker.api, all_assets, start_date=start_date, end_date=end_date)

# assets = broker.getAllAssets()
# prices_database.setupPrices(broker.api, assets)
# getDecadeData(assets)

#report = reports_database.generateReport()

# account = api.get_account()
# buying_power = float(account.buying_power) // 1
# stocks_to_order = getOrders(report, buying_power)
# orders = rebalance(stocks_to_order)

# for order in orders:
#   print(order)

#executeOrders(orders, order)

now = date(2019, 11, 20)
for i in range(104):
  print('Making report for the date:', now)
  reports_database.saveReport(now)
  now += relativedelta(days=7)

'''
now = date(2021,9,1)
def getNewReport(date):
  return reports_database.getTopResults(date, number_of_results=100)

def getReports(start_date, weeks):
  reports = []
  for i in range(weeks):
    report = getNewReport(start_date)
    reports.append(report)
    start_date += relativedelta(days=7)
  
  return reports


reports = getReports(now, 10)

def printReports(reports):
  for report in reports:
    print(report.date)
    for entry in report.entries:
      print(entry)
    print("="*10)

def getMoney(reports):
  first_stock = None
  start_price = 0
  profit = 0
  end_price = 0
  broke = False
  for report in reports:
    if first_stock == None:
      first_stock = report.stocks[0]
      entry = report.get(first_stock)
      start_price = entry.open_price


    if not first_stock in report.stocks:
      entry = reports_database.getReportByDate(first_stock, report.date)
      end_price = entry.close_price
      profit = end_price - start_price
      broke = True
      break
  
  if broke == False:
    last_date = reports[-1].date
    entry = reports_database.getReportByDate(first_stock, report.date)
    end_price = entry.close_price
    profit = end_price - start_price


  print(first_stock, profit,start_price, end_price)
  print("PROFIT:", profit, f"Still Holding: {not broke}")

printReports(reports)
getMoney(reports)

'''
'''
portfolio = Portfolio()
position_stocks = [position.stock for position in portfolio.positions]
report = getNewReport(now)
orders = []
free_money = portfolio.availableMoney()

for entry in report.entries:
  amount_of_stocks = (free_money // 5) // entry.open_price
  print(entry.stock, amount_of_stocks)
  if not entry.stock in position_stocks:
    order = Order(entry.stock, amount_of_stocks, "BUY", entry.open_price)
    orders.append(order)

order_stocks = [order.stock for order in orders]

for position in portfolio.positions:
  if not position.stock in order_stocks:
    order = Order(position.stock, position.amount, "SELL", position.price)
    orders.insert(0, order)

'''




print("My program took", time.time() - start_time, "to run")

