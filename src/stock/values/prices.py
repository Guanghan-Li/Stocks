from datetime import datetime
from dateutil import relativedelta
from pandas import DataFrame
import pytz, itertools
import pandas as pd
from src.stock.values.price import Price
from src.stock.lib.broker_api.announcement import Announcement

class Prices:
  def __init__(self, symbol, data: list[Price]):
    self.prices: list[Price] = sorted(data, key=lambda price: price.date)
    if len(data) > 0:
      self.start_date = data[0].date
      self.end_date = data[-1].date
    else:
      self.start_date = datetime.now()
      self.end_date = datetime.now()
    self.symbol = symbol.replace(".", "_")
    self.amount = len(data)

  def __len__(self):
    return self.amount

  def __str__(self):
    start_date = self.start_date.strftime("%Y-%m-%d")
    end_date = self.end_date.strftime("%Y-%m-%d")
    return f"{self.symbol} -> amount: {self.amount} | start_date: {start_date} | end_date: {end_date}"

  @staticmethod
  def fromDict(symbol, data):
    prices = []
    for p in data:
      price = Price.fromDict(p)
      prices.append(price)
    
    return Prices(symbol, prices)

  @staticmethod
  def fromDataFrame(symbol, data: DataFrame) -> 'Prices':
    date_format = "%Y-%m-%d"
    data.index = pd.to_datetime(data.index, format=date_format)
    dates = data.index.tolist()
    prices = []
    for date in dates:
      price = Price.fromDataFrame(symbol, date, data)
      prices.append(price)

    return Prices(symbol, prices)

  @property
  def empty(self):
    return len(self.prices) == 0

  def toDict(self):
    output = []
    for price in self.prices:
      output.append(price.toDict())
    return output

  def toDataFrame(self):
    price_dict = self.toDict()
    df = pd.DataFrame(price_dict)
    df = df.set_index("date")
    return df

  def amountOfYears(self):
    return len(self.splitByYear())

  def amountOfMonths(self):
    return len(self.splitByMonth())

  def amountOfWeeks(self):
    return len(self.splitByWeek())

  def splitByWeek(self):
    def groupFunc(price: Price):
      #return price.date.isocalendar().week
      return (self.end_date - price.date).days // 8
    groups = itertools.groupby(self.prices, key=groupFunc)
    return [Prices(self.symbol, list(group[1])) for group in groups]

  def splitByMonth(self) -> list['Prices']:
    def groupFunc(price: Price):
      return (price.date.year, price.date.month)
    
    groups = itertools.groupby(self.prices, key=groupFunc)
    return [Prices(self.symbol, list(group[1])) for group in groups]

  def splitByYear(self) -> list['Prices']:
    def groupFunc(price: Price):
      return (self.end_date - price.date).days // 366
    
    groups = itertools.groupby(self.prices, key=groupFunc)
    return [Prices(self.symbol, list(group[1])) for group in groups]
  
  def get(self, from_index, to_index=-1):
    return Prices(self.symbol, self.prices[from_index:to_index])
  
  def getLastYears(self, amount, from_date=None) -> 'Prices':
    if from_date != None:
      new_prices = [price for price in self.prices if price.date <= from_date]
    else:
      new_prices = self.prices

    output = []
    prices = Prices(self.symbol, new_prices).splitByYear()
    for i in range(-1, (amount+1)*-1, -1):
      output += prices[i].prices
    
    return Prices(self.symbol, output)
  
  def getBefore(self, date: datetime) -> 'Prices':
    date = self.makeDateGood(date)
    new_prices = [price for price in self.prices if self.makeDateGood(price.date) <= date]
    return Prices(self.symbol, new_prices)

  def makeDateGood(self, date):
    return datetime(date.year, date.month, date.day)

  def splitAt(self, date: datetime):
    date = self.makeDateGood(date)
    before_prices: list[Price] = [price for price in self.prices if self.makeDateGood(price.date) <= date]
    after_prices: list[Price] = [price for price in self.prices if self.makeDateGood(price.date) > date]
    return before_prices, after_prices
  
  def adjust(self, announcement: Announcement):
    date = datetime(announcement.ex_date.year, announcement.ex_date.month, announcement.ex_date.day, tzinfo=pytz.UTC)
    new_rate = announcement.new_rate
    old_rate = announcement.old_rate

    if announcement.ca_sub_type == "stock_split":
      new_prices = self.stockSplit(new_rate, old_rate, date)
    elif announcement.ca_sub_type == "reverse_split":
      new_prices = self.stockReverseSplit(new_rate, old_rate, date)
      
    return Prices(self.symbol, new_prices)

  def stockSplit(self, new_rate, old_rate, date):
    before_prices, after_prices = self.splitAt(date)
    adjusted_prices = [price.stockSplit(new_rate, old_rate) for price in before_prices]
    return adjusted_prices + after_prices

  def stockReverseSplit(self, new_rate, old_rate, date):
    before_prices, after_prices = self.splitAt(date)
    adjusted_prices = [price.stockReverseSplit(new_rate, old_rate) for price in before_prices]
    return adjusted_prices + after_prices

    
