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
    info = {
      'name': db_path,
      'engine': 'peewee.SqliteDatabase'
    }
    self.proxy: DatabaseProxy = proxy
    self.database = PostgresqlDatabase(
      "prices",
      user="postgres",
      password="stock",
      host="localhost",
      port=5433
    )
    self.proxy.initialize(self.database)
    self.proxy.connect()

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

  def dfToDict(self, date, prices):
    return {
      "date":date,
      "open": prices['open'][date],
      "close": prices['close'][date],
      "high": prices['high'][date],
      "low": prices['low'][date]
    }

  def loadPrices(self, prices, table, asset=None):
    dates = [str(date) for date in prices['open'].keys()]
    data = [self.dfToDict(date, prices) for date in dates]
    table.insert_many(data).on_conflict_ignore().execute()
    print("DONE LOADING")

    # for date in dates:
    #   with self.proxy.atomic():
    #     table.create(date=date, open=prices['open'][date], close=prices['close'][date], high=prices['high'][date], low=prices['low'][date])

  def setupPrices(self, asset, whole_data: DataFrame):
      print(whole_data.empty)
      print(whole_data.keys())
      try:
        data_points = len(whole_data["open"])
      except:
        raise Exception("Joel was right!")
      if isinstance(whole_data, DataFrame) and data_points > 980:
        print("Loading prices for ", asset)
        tables = self.proxy.get_tables()
        asset = asset.replace(".", "_")
        table = newPrices(asset)
        if table not in tables:
          self.proxy.create_tables([table])
        print(len(tables))
        self.loadPrices(whole_data, table, asset)
      elif len(whole_data['open']) < 980:
       #print(f"{asset} not enough data")
       pass
  
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
