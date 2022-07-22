from peewee import *
from repos.report_model import *
from pandas import DataFrame
from alpaca_trade_api.rest import *
from alpaca_trade_api.rest import REST
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from Calculate.calculations import Calculations
from Calculate.momentum import Momentum
from values.report import Entry, Report
from time import sleep, strftime
from peewee import FieldAccessor

from values.strategy import *

class ReportDatabase:
    def __init__(self, proxy, price_repo, name="Data/reports.db"):
        self.proxy = report_proxy
        #self.proxy.initialize(SqliteDatabase(name))
        self.database = PostgresqlDatabase(
          "reports",
          user="postgres",
          password="stock",
          host="localhost",
          port=5433
        )
        self.proxy.initialize(self.database)
        self.proxy.connect()
        self.price_repo = price_repo
    

    def setupReports(self, all_assets, start_date='2019-11-20', end_date='2022-02-17'):
      for asset in all_assets:
        print("Loading reports for ", asset)

        # tables = self.proxy.get_tables()
        # table = newReport(asset)
        # if table not in tables:
        #     self.report_proxy.create_tables([table])
        

        weekly_dates = self.getWeeklyDates('2019-11-20', '2022-02-17')

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
      print(report.stock, report.column, report.trend)
      if report.column == 'UP' and report.trend == 'UP':
        return True
      else:
        return False

    def updatePnf(self, date, stock, column, trend):
      table_name = date.strftime("%Y-%m-%d")
      table = newReport(table_name)
      
      query = table.update({'column': column, 'trend': trend}).where(table.stock == stock)
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

    def generateReport(self, all_stocks, date):
        report = []

        for stock in all_stocks:
            #print('Getting ATR for ' + stock)
            prices = self.price_repo.getPricesFromDB(stock, date)
            entry = self.generateEntry(stock, prices, date)
            report.append(entry)
        
        return report
    
    def generateRepotForStock(self, stock, date):
      pass

    def getReportByDate(self, stock, date):
      table_name = date.strftime("%Y-%m-%d")
      table = newReport(table_name)
      entry = list(table.select().where(table.stock == stock))[0]
      print(entry.stock)
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
    def generateEntry(stock, prices, current_date):
        print("generateEntry", stock, current_date)
        current_year = current_date.year
        now = current_date
        # atr = round(Calculations.averageTrueRange(prices, len(prices)), 2)
        # close_price = prices[-1]['close']
        # percent_atr = (atr / close_price) * 100

        monthly_last_year = []
        monthly_two_year = []
        last_year = current_date - relativedelta(weeks=52)
        two_year = last_year - relativedelta(weeks=52)

        while current_date > last_year:
          month = ReportDatabase.getPricesByMonth(prices, current_date)
          monthly_last_year.append(month)
          current_date = current_date - relativedelta(weeks=4)

        while current_date > two_year:
          month = ReportDatabase.getPricesByMonth(prices, current_date)
          monthly_two_year.append(month)
          current_date = current_date - relativedelta(weeks=4)

        print("Entry Gen", len(monthly_last_year), len(monthly_two_year))

        # while len(monthly_last_year) > 0 and [] in monthly_last_year:
        #   monthly_last_year.remove([])

        # while len(monthly_two_year) > 0 and [] in monthly_two_year:
        #   monthly_two_year.remove([])

        # if [] in monthly_last_year or [] in monthly_two_year:
        #   print("Returning None", monthly_last_year, monthly_two_year)
        #   return None

        if monthly_last_year == [] or monthly_two_year == []:
          return None


        current_momentum = Momentum.momentumOneYear(monthly_last_year)
        prev_momentum = Momentum.momentumOneYear(monthly_two_year)


        rsi14 = Momentum.calculateRsis(prices, 14)[-1]
        rsi28= Momentum.calculateRsis(prices, 28)[-1]
        #acceleration = current_momentum - prev_momentum
        acceleration = prev_momentum - current_momentum
        price = prices[-1]
        entry = Entry(
          stock,
          now,
          price['open'],
          price['close'],
          0,
          0,
          current_momentum,
          prev_momentum,
          acceleration,
          rsi14,
          rsi28
        )
        return entry