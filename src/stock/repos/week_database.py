from peewee import *
from src.stock.repos.report_model import *
from pandas import DataFrame
from alpaca_trade_api.rest import *
from alpaca_trade_api.rest import REST
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from src.stock.calculate.calculations import Calculations
from src.stock.calculate.momentum import Momentum
from src.stock.values.report import Entry, Report
from time import sleep, strftime
from peewee import FieldAccessor
import traceback
from pyoink.values.chart import Chart

from src.stock.values.strategy import *
from src.stock.values.prices import Prices, Price

from src.stock.lib.log.log import Log
import json

class ReportWeekDatabase:
    def __init__(self, log=False):
        self.proxy = week_proxy
        #self.proxy.initialize(SqliteDatabase(name))
        self.database = PostgresqlDatabase(
          "reports_by_week",
          user="postgres",
          password="stock",
          host="localhost",
          port=5433
        )
        self.log = Log(can_log=log)
        self.proxy.initialize(self.database)
        self.proxy.connect()

    def setupReports(self, all_assets, start_date='2019-11-20', end_date='2021-11-24'):
      for asset in all_assets:
        print("Loading reports for ", asset)

        # tables = self.proxy.get_tables()
        # table = newReport(asset)
        # if table not in tables:
        #     self.report_proxy.create_tables([table])
        

        weekly_dates = self.getWeeklyDates('2019-11-20', '2021-11-24')

        for date in weekly_dates:
          date = datetime.fromisoformat(date)
          self.saveReport(date)

    def saveEntry(self, entry):

      date = entry.date.strftime("%Y-%m-%d")
      table = newReport(date)
      tables = self.proxy.get_tables()
      if table not in tables:
        self.proxy.create_tables([table])

      table.create(
        date = entry.date.strftime("%Y-%m-%d"),
        stock = entry.stock,
        open_price = entry.open_price,
        close_price = entry.close_price,
        atr = entry.atr,
        percent_atr = entry.percent_atr,
        two_year_momentum = entry.prev_momentum,
        one_year_momentum = entry.current_momentum,
        acceleration = entry.acceleration,
        rsi14 = entry.rsi14,
        rsi28 = entry.rsi28,
        column = entry.column,
        trend = entry.trend
      )
      print(f"Saved {entry.stock} on {entry.date.strftime('%Y-%m-%d')}")