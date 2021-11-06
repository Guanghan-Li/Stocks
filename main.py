from timeit import *
import os, math, subprocess, time
import mplfinance as mpf
from alpaca_trade_api.rest import *
from repos.report_model import *
from repos.price_database import *
from Calculate.calculations import Calculations
from values.report import Entry
from repos.price_database import PricesDatabase
from Calculate.momentum import Momentum
from values.order import Order
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from repos.report_database import ReportDatabase
from broker import Broker
from pnf.pnf import PNF

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
    end_date = date(i+2, 10, 13).isoformat()
    start_date = date(i, 10, 14).isoformat()
    print("Getting prices for the date {} -> {}".format(start_date, end_date))
    prices_database.setupPrices(broker.api, all_assets, start_date=start_date, end_date=end_date)

#assets = broker.getAllAssets()
#prices_database.setupPrices(broker.api, assets)
#getDecadeData(assets)

#report = reports_database.generateReport()
# account = api.get_account()
# buying_power = float(account.buying_power) // 1
# stocks_to_order = getOrders(report, buying_power)
# orders = rebalance(stocks_to_order)

# for order in orders:
#   print(order)

#executeOrders(orders, order)

now = date(2019, 10, 16)
for i in range(95):
   print('Making report for the date:', now)
   reports_database.saveReport(now)
   now += relativedelta(days=7)

print("My program took", time.time() - start_time, "to run")

