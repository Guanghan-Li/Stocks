from peewee import *
from repos.report_model import *
from pandas import DataFrame
from alpaca_trade_api.rest import *
from alpaca_trade_api.rest import REST
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from Calculate.calculations import Calculations
from Calculate.momentum import Momentum
from values.report import Entry

class ReportDatabase:
    def __init__(self, proxy, price_repo):
        self.proxy = report_proxy
        self.proxy.initialize(SqliteDatabase('Data/reports.db'))
        self.proxy.connect()
        self.price_repo = price_repo
    

    def setupReports(self, all_assets, start_date='2018-10-03', end_date='2020-10-21'):
      for asset in all_assets:
        print("Loading reports for ", asset)

        # tables = self.proxy.get_tables()
        # table = newReport(asset)
        # if table not in tables:
        #     self.report_proxy.create_tables([table])
        

        weekly_dates = self.getWeeklyDates('2016-09-07', '2021-09-08')

        for date in weekly_dates:
          date = datetime.fromisoformat(date)
          self.saveReport(date)

    def saveEntry(self, entry):
      date = entry.date.isoformat()
      table = newReport(date)
      tables = self.proxy.get_tables()
      if table not in tables:
        self.proxy.create_tables([table])

      table.create(
        date = entry.date,
        stock = entry.stock,
        open_price = entry.open_price,
        close_price = entry.close_price,
        atr = entry.atr,
        percent_atr = entry.percent_atr,
        two_year_momentum = entry.prev_momentum,
        one_year_momentum = entry.current_momentum,
        acceleration = entry.acceleration
      )

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

    def updatePnf(self, date, stock, column, trend):
      table_name = f"{date.year}-{date.month}-{date.day}"
      table = newReport(table_name)
      query = table.update({'column': column, 'trend': trend}).where(table.stock == stock)
      query.execute()

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

    def generateEntry(self, stock, current_date):
        prices = self.price_repo.getTwoYearPrices(stock, current_date)
        if len(prices) < 500:
          return None

        current_year = current_date.year
        now = current_date
        atr = round(Calculations.averageTrueRange(prices, len(prices)), 2)
        close_price = prices[-1]['close']
        percent_atr = (atr / close_price) * 100

        monthly_last_year = []
        monthly_two_year = []
        last_year = current_date - relativedelta(weeks=52)
        two_year = last_year - relativedelta(weeks=52)

        while current_date > last_year:
          month = self.price_repo.getPricesByMonth(stock, current_date)
          monthly_last_year.append(month)
          current_date = current_date - relativedelta(weeks=4)

        while current_date > two_year:
          month = self.price_repo.getPricesByMonth(stock, current_date)
          monthly_two_year.append(month)
          current_date = current_date - relativedelta(weeks=4)

        current_momentum = Momentum.momentumOneYear(monthly_last_year)
        prev_momentum = Momentum.momentumOneYear(monthly_two_year)
        acceleration = current_momentum - prev_momentum
        price = prices[-1]
        entry = Entry(stock, now, price['open'], price['close'], atr, percent_atr, current_momentum, prev_momentum, acceleration)
        return entry