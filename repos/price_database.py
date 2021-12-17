from repos.price_model import *
from peewee import *
from pandas import DataFrame
from alpaca_trade_api.rest import *
from alpaca_trade_api.rest import REST
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from time import sleep, strftime
class PricesDatabase:
  def __init__(self, proxy, db_path):
    self.proxy: DatabaseProxy = proxy
    self.database = SqliteDatabase(db_path)
    self.database.connect()
    #self.proxy.initialize(self.database)
    #self.proxy.connect()

  def getAllStocks(self):
    return self.proxy.get_tables()

  def getPricesByMonth(self, stock, current_date):
    end = current_date + relativedelta(days=1)
    start = end - relativedelta(weeks=4)
    table = newPrices(stock)
    result = list(table.select().dicts().where(table.date.between(start, end)))
    return result

  def getTwoYearPrices(self, stock, date):
    end = date
    start = end - relativedelta(weeks=104)
    end = end + timedelta(days=1)
    table = newPrices(stock)
    result = list(table.select().dicts().where(table.date.between(start, end)))
    return result

  def loadPrices(self, prices, table):
    dates = [str(date) for date in prices['open'].keys()]
    for date in dates:
      with self.database.atomic():
        table.create(date=date, open=prices['open'][date], close=prices['close'][date], high=prices['high'][date], low=prices['low'][date])

  def setupPrices(self, api, all_assets, thread_name='Default', start_date='2017-11-22', end_date='2021-11-24'):
    # self.proxy.create_tables([Info])
    # Info.create(last_updated = datetime.datetime.now())

    # db_tables = self.proxy.get_tables()
    # tables = [newPrices(asset) for asset in all_assets if asset not in db_tables]
    # self.proxy.create_tables(tables)

    for asset in all_assets:
      whole_data = None

      try:
        whole_data = api.get_bars(asset, TimeFrame.Day, start_date, end_date, adjustment='raw').df
      except:
        print("CANNOT GET ASSET:", asset)
        pass

      #print(asset, len(whole_data['open']))

      if isinstance(whole_data, DataFrame) and len(whole_data['open']) > 980:
        print("Loading prices for ", asset, "on thread", thread_name)
        tables = self.database.get_tables()
        table = newPrices(asset)
        if table not in tables:
          self.database.create_tables([table])
        print(tables)
        self.loadPrices(whole_data, table)
  
  def getPriceByDay(self, stock, date: datetime):
    table = newPrices(stock)
    date = date + timedelta(hours=4)
    query = table.select().where(table.date == date)
    print(query.count())
    return list(query)
  
  def updatePrices(self, api):
    assets = self.proxy.get_tables()
    assets.remove('info')

    print(assets)


  def getPricesFromDB(self, stock):
    table = newPrices(stock)
    return list(table.select().dicts())
