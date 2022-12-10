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

from pyoink.values.chart import Chart

from src.stock.values.strategy import *
from src.stock.values.prices import Prices, Price

from src.stock.lib.log.log import Log

class ReportDatabase:
    def __init__(self, log=False):
        self.proxy = report_proxy
        #self.proxy.initialize(SqliteDatabase(name))
        self.database = PostgresqlDatabase(
          "reports",
          user="postgres",
          password="stock",
          host="localhost",
          port=5433
        )
        self.log = Log(can_log=log)
        self.proxy.initialize(self.database)
        self.proxy.connect()

    @property
    def symbols(self) -> list[str]:
      return self.proxy.get_tables()

    def deleteAll(self):
      tables = [newReport(t) for t in self.database.get_tables()]
      self.log.info("Reports Amount Before:", len(tables))
      self.database.drop_tables(tables)
      self.log.info("Reports Amount After:", len(self.database.get_tables()))

    def getEntryByDate(self, symbol, date):
      table: ReportsModel = newReport(symbol)
      query = list(table.select().where(table.date == date))
      return Entry.fromDB(query[0])

    def getDatesForSymbol(self, symbol):
      table: ReportsModel = newReport(symbol)
      query = list(table.select(table.date).tuples())
      return [q[0] for q in query]

    def getEntriesByDate(self, date):
      symbols = self.proxy.get_tables()
      entries = []
      for symbol in symbols:
        entry = self.getEntryByDate(symbol, date)
        entries.append(entry)
      
      return entries

    def setupReports(self, all_assets, start_date='2019-11-20', end_date='2022-02-17'):
      for asset in all_assets:
        self.log.info("Loading reports for ", asset)

        # tables = self.proxy.get_tables()
        # table = newReport(asset)
        # if table not in tables:
        #     self.report_proxy.create_tables([table])
        

        weekly_dates = self.getWeeklyDates('2019-11-20', '2022-02-17')

        for date in weekly_dates:
          date = datetime.fromisoformat(date)
          self.saveReport(date)

    def saveEntry(self, entry):
      table = newReport(entry.stock)
      tables = self.proxy.get_tables()
      if table not in tables:
        self.proxy.create_tables([table])
      with self.database.atomic():
        table.create(**entry.toDict())
        self.log.info(f"Saved {entry.stock} on {entry.dateString()}")
    
    def saveEntries(self, entries):
      data = [entry.toDict() for entry in entries]
      table = newReport(entries[0].stock)
      tables = self.proxy.get_tables()
      if table not in tables:
        self.proxy.create_tables([table])
      
      with self.database.atomic():
        table.insert_many(data).execute()
      
      print(f"SAVED {entries[0].stock} "*10)

    def saveReport(self, date):
      all_stocks = self.price_repo.getAllStocks()
      for asset in all_stocks:
        entry = self.generateEntry(asset, date)
        if entry != None:
          self.saveEntry(entry)

    def getWeeklyDates(self, start, end):
      start = datetime.fromisoformat(start)
      end = datetime.fromisoformat(end)
      dates = []
      current = start
      while (current < end):
        dates.append(current)
        current += relativedelta(days=7)

      return dates

    def filledPNF(self, date, stock):
      table_name = f"{date.year}-{date.month}-{date.day}"
      table = newReport(table_name)
      report = table.get(table.stock == stock)
      self.log.info(report.stock, report.column, report.trend)
      if report.column == 'UP' and report.trend == 'UP':
        return True
      else:
        return False

    def updatePnf(self, date, symbol, column, trend):
      table = newReport(symbol)
      with self.database.atomic():
        query = table.update({'column': column, 'trend': trend}).where(table.date == date)
        query.execute()

    def getTopResults(self, date, number_of_results=20):
      table_name = date.strftime("%Y-%m-%d")
      table = newReport(table_name)
      ordering = table.acceleration.desc()
      results = list(table.select().where(table.column == "UP", table.open_price != table.close_price).order_by(ordering).limit(number_of_results))
      #results = list(table.select().where(table.column == "UP" and 1 == 1).limit(number_of_results))
      entries =  [Entry.fromDB(result) for result in results]
      entries = sorted(entries, key=lambda entry: entry.current_momentum, reverse=False)
      return Report(date, entries, number_of_results)

    def getReports(self, date, strategy: Strategy, stocks_to_exclude: list[str]):
      number_of_results = 10
      table_name = date.strftime("%Y-%m-%d")
      table = newReport(table_name)

      ordering = Sorting.getFunc(table, strategy.initial_sort)
      secondary_ordering = Sorting.getFunc(table, strategy.secondary_sort)

      #query = table.select().where(table.rsi14 < 50, table.rsi28 < 50, table.rsi28 - table.rsi14 < 4, table.one_year_momentum > 2.3, table.one_year_momentum< 4)
      filters = [Filter.getFunc(table, filter) for filter in strategy.filters]
      query = table.select().where(table.stock.not_in(stocks_to_exclude), *filters)
      query = query.order_by(ordering).limit(strategy.cutoff.value)
      query = query.order_by(secondary_ordering).limit(strategy.portfolio_size.value)
      results = list(query)
      entries =  [Entry.fromDB(result) for result in results]
      return Report(date, entries, number_of_results)

    def generateWeeklyReports(self, stock, start, end):
      dates = self.getWeeklyDates(start, end)
      weekly_reports = []
      start_year = int(datetime.fromisoformat(start).year)

      for date in dates:
        prices = self.price_repo.getTwoYearPrices(stock, str(date))
        entry = self.generateEntry(stock, prices, start_year)
        weekly_reports.append([date, entry])

      return weekly_reports
    
    def generateRepotForStock(self, stock, date):
      pass

    def getReportByDate(self, stock, date):
      table_name = date.strftime("%Y-%m-%d")
      table = newReport(table_name)
      entry = list(table.select().where(table.stock == stock))[0]
      self.log.info(entry.stock)
      return Entry.fromDB(entry)

    @staticmethod
    def getPricesByMonth(prices, current_date):
      result = []
      for price in prices:
        if isinstance(price["date"], str):
          price_date = datetime.fromisoformat(price['date'])
        else:
          price_date = price["date"]

        if price_date.year == current_date.year and price_date.month == current_date.month:
          result.append(price)
      
      return result

    @staticmethod
    def generateEntry(prices: Prices):
      if not prices.canGetYears(2):
        return None
        
      years = prices.getLastYears(2).splitByYear()
      last_year_prices = years[0]
      two_year_prices = years[1]

      current_momentum = Momentum.momentumOneYear(last_year_prices)
      prev_momentum = Momentum.momentumOneYear(two_year_prices)

      rsi14 = Momentum.calculateRsis(prices, 14)[-1]
      rsi28= Momentum.calculateRsis(prices, 28)[-1]

      acceleration = prev_momentum - current_momentum
      price = prices.prices[-1]

      box_size = Chart.getBoxSize(price.open)
      chart = Chart(prices.symbol, box_size, 3)
      chart.generate(prices.toSimpleDict())
      column_direction = ("DOWN", "UP")[chart.last_direction.value]
      entry = Entry(
        prices.symbol,
        prices.end_date,
        price.open,
        price.close,
        0,
        0,
        current_momentum,
        prev_momentum,
        acceleration,
        rsi14,
        rsi28,
        column=column_direction
      )
      return entry