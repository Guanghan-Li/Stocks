from datetime import datetime
from pandas import DataFrame
import pytz, itertools
import pandas as pd

class Price:
  def __init__(self, symbol, date: datetime, open, close, high, low):
    self.symbol = symbol
    self.date = datetime.fromtimestamp(date.timestamp(), tz=pytz.UTC)
    self.open = open
    self.close = close
    self.high = high
    self.low = low

  def __str__(self):
    date = self.date.strftime("%Y-%m-%d")
    return f"{self.symbol} -> date: {date} | o: {self.open} | c: {self.close} | h: {self.high} | l: {self.low}"
  
  def toDict(self):
    return {
      "date": self.date,
      "open": self.open,
      "close": self.close,
      "high": self.high,
      "low": self.low
    }
  
  def toDataFrame(self):
    price_dict = self.toDict()
    return pd.DataFrame([self.toDict()], index=[])

  @staticmethod
  def fromDict(symbol, data):
    return Price(
      symbol,
      data["date"],
      data["open"],
      data["close"],
      data["high"],
      data["low"]
    )
  
  @staticmethod
  def fromDataFrame(symbol, date: datetime, data: DataFrame):
    return Price(
      symbol,
      date,
      data["open"][date],
      data["close"][date],
      data["high"][date],
      data["low"][date]
    )

class Prices:
  def __init__(self, symbol, data: list[Price]):
    self.prices: list[Price] = data
    self.start_date = data[0].date
    self.end_date = data[-1].date
    self.symbol = symbol
    self.amount = len(data)

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

  def splitByMonth(self) -> list['Prices']:
    def groupFunc(price: Price):
      return (price.date.year, price.date.month)
    
    groups = itertools.groupby(self.prices, key=groupFunc)
    output = [Prices(self.symbol, group) for group in groups]
    return output

  def splitByYear(self) -> list['Prices']:
    def groupFunc(price: Price):
      return price.date.year
    
