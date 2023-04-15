from datetime import datetime
from dateutil import relativedelta
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

    def simpleDict(self):
        return {"o": self.open, "c": self.close, "h": self.high, "l": self.low}

    def toDict(self):
        date = self.date.strftime("%Y-%m-%d")
        return {
            "date": date,
            "open": self.open,
            "close": self.close,
            "high": self.high,
            "low": self.low,
        }

    def toDict2(self):
        return {
            "date": self.date.strftime("%Y-%m-%d"),
            "open": self.open,
            "close": self.close,
            "high": self.high,
            "low": self.low,
        }

    def toDataFrame(self):
        price_dict = self.toDict()
        return pd.DataFrame([self.toDict()], index=[])

    @staticmethod
    def fromDict(symbol, data):
        return Price(
            symbol, data["date"], data["open"], data["close"], data["high"], data["low"]
        )

    @staticmethod
    def fromDataFrame(symbol, date: datetime, data: DataFrame):
        return Price(
            symbol,
            date,
            data["open"][date],
            data["close"][date],
            data["high"][date],
            data["low"][date],
        )

    def stockSplit(self, new_rate, old_rate):
        self.open = round(self.open * new_rate / old_rate, 3)
        self.close = round(self.close * new_rate / old_rate, 3)
        self.high = round(self.high * new_rate / old_rate, 3)
        self.low = round(self.low * new_rate / old_rate, 3)
        return self

    def stockReverseSplit(self, new_rate, old_rate):
        self.open = round(self.open * old_rate / new_rate, 3)
        self.close = round(self.close * old_rate / new_rate, 3)
        self.high = round(self.high * old_rate / new_rate, 3)
        self.low = round(self.low * old_rate / new_rate, 3)
        return self
