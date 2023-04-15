from datetime import datetime
from sty import fg
from pandas import DataFrame
from dateutil.relativedelta import relativedelta
from pykka import ThreadingActor
import pandas as pd


def timeFunc(func):
    def wrapper(*args, **kwargs):
        start_time = datetime.now().timestamp()
        value = func(*args, **kwargs)
        end_time = datetime.now().timestamp()
        print(f"{fg.yellow}TIME:{fg.rs} {func.__name__} took {end_time - start_time}")
        return value

    return wrapper


def dfToDict(date, prices):
    return {
        "date": date,
        "open": prices["open"][date],
        "close": prices["close"][date],
        "high": prices["high"][date],
        "low": prices["low"][date],
    }


class Helpers(ThreadingActor):
    def __init__(self):
        super().__init__()

    # @timeFunc
    def getTwoYearPrices(self, stock, prices: DataFrame, orig_date: datetime):
        date_format = "%Y-%m-%d"
        start = orig_date - relativedelta(weeks=104)
        date = orig_date.strftime(date_format)
        start = start.strftime(date_format)
        prices.index = pd.to_datetime(prices.index, format=date_format)
        prices = prices.loc[str(start) : str(date)]
        dates = [str(date) for date in prices["open"].keys()]
        data = [dfToDict(date, prices) for date in dates]
        return data
