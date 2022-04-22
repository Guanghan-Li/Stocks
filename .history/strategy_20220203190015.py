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
  ACCELERATION_MIN = "ACCELERATION_MIN"
  MOMENTUM_MIN = "MOMENTUM_MIN"
  RSI_RANGE = "RSI_RANGE"

class Cutoff(Enum):
  TEN = 10
  FIFTY = 50
  HUNDRED = 100

class Sorting(Enum):
  ACCELERATION_UP = "ACCELERATION_UP"
  ACCELERATION_DOWN = "ACCELERATION_DOWN"
  YEARLY_MOMENTUM_UP = "YEARLY_MOMENTUM_UP"
  YEARLY_MOMENTUM_DOWN ="YEARLY_MOMENTUM_DOWN"
  TWO_YEAR_MOMENTUM_UP = "TWO_YEAR_MOMENTUM_UP"
  TWO_YEAR_MOMENTUM_DOWN = "TWO_YEAR_MOMENTUM_DOWN"
  RSI14_UP = "RSI14_UP"
  RSI14_DOWN = "RSI14_DOWN"
  RSI28_UP = "RSI28_UP"
  RSI28_DOWN = "RSI28_DOWN"
  DIFFERENCE_UP = "DIFFERENCE_UP"
  DIFFERENCE_DOWN = "DIFFERENCE_DOWN"

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
    self.portolio_size = portfolio_size

  def __str__(self):
    return f"Strategy -> "
    