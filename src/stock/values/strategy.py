"""
Biased
filter(7)
> acceleration min
> momentum min
> rsi range




Sorting Schemes (12)
> acceleration (up, down)
> yearly momentum (up, down)
> two year momentum (up, down)
> rsi14 (up, down)
> rsi28 (up, down)
> difference between rsi (up, down)

cutoff (3)
> 10
> 50
> 100

secondary sorting (10)
> see above

portfolio size (6)
> 2
> 4
> 6




weight (1)
> evenly


"""
from enum import Enum

class Filter(Enum):
  ACCELERATION_MIN = ("acceleration", "min", -2)
  ACCELERATION_MAX = ("acceleration", "max", 0)
  #MOMENTUM_MIN = ("momentum", "min", 1)
  RSI14_MIN = ("rsi14", "min", 20)
  RSI14_MAX = ("rsi14", "max", 45)
  RSI28_MIN = ("rsi28", "min", 25)
  RSI28_MAX = ("rsi28", "max", 50)
  TREND_UP = ("trend", "UP")
  TREND_DOWN = ("trend", "DOWN")
  COLUMN_UP = ("column", "UP")
  COLUMN_DOWN = ("column", "DOWN")

  @staticmethod
  def getFunc(table, filter):
    values = filter.value
    if len(values) == 2:
      return table.__getattribute__(table, values[0]).field == values[1]
    elif values[1] == "min":
      return table.__getattribute__(table, values[0]).field >= values[2]
    elif values[1] == "max":
      return table.__getattribute__(table, values[0]).field <= values[2]

class Cutoff(Enum):
  TEN = 10
  FIFTY = 50
  HUNDRED = 100

class Sorting(Enum):
  ACCELERATION_UP = ("acceleration", "asc")
  ACCELERATION_DOWN = ("acceleration", "desc")
  YEARLY_MOMENTUM_UP = ("one_year_momentum", "asc")
  YEARLY_MOMENTUM_DOWN = ("one_year_momentum", "desc")
  TWO_YEAR_MOMENTUM_UP = ("two_year_momentum", "asc")
  TWO_YEAR_MOMENTUM_DOWN = ("two_year_momentum", "desc")
  RSI14_UP = ("rsi14", "asc")
  RSI14_DOWN = ("rsi14", "desc")
  RSI28_UP = ("rsi28", "asc")
  RSI28_DOWN = ("rsi28", "desc")
  # DIFFERENCE_UP = "DIFFERENCE_UP"
  # DIFFERENCE_DOWN = "DIFFERENCE_DOWN"

  @staticmethod
  def getFunc(table, sorting):
    values = sorting.value
    return table.__getattribute__(table, values[0]).field.__getattribute__(values[1])()

class PortfolioSize(Enum):
  TWO = 2
  FOUR = 4
  SIX = 6

class Strategy:
  def __init__(self, filters, initial_sort, cutoff, secondary_sort, portfolio_size):
    self.filters = filters
    self.initial_sort = initial_sort
    self.cutoff = cutoff
    self.secondary_sort = secondary_sort
    self.portfolio_size = portfolio_size

  def __str__(self):
    filter_names = ', '.join([filter.name for filter in self.filters])
    filters = f"Filters: [{filter_names}]"
    initial_sort = f"Initial Sort: {self.initial_sort.name}"
    cutoff = f"Cutoff: {self.cutoff.name}"
    secondary_sort = f"Secondary Sort: {self.secondary_sort}"
    portfolio_size = f"Portfolio Size: {self.portfolio_size.name}"

    return "Strategy -> " + " | ".join([filters, initial_sort, cutoff, secondary_sort, portfolio_size])

    