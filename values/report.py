from Calculate.momentum import Momentum


class Entry:
  def __init__(self, stock, current_date, open_price, close_price, atr, percent_atr, current_momentum, prev_momentum, acceleration):
    self.stock = stock
    self.date = current_date
    self.atr = atr
    self.open_price = open_price
    self.close_price = close_price
    self.percent_atr = percent_atr
    self.current_momentum = round(current_momentum, 4)
    self.prev_momentum = round(prev_momentum, 4)
    self.acceleration = round(acceleration, 4)

  def __str__(self):
    return f"Stock: {self.stock} | Close Price {self.close_price} | Open Price: {self.open_price} | ATR: {self.atr} | Percent ATR: {self.percent_atr} | 2Y Momentum: {self.prev_momentum} | 1Y Momentum: {self.current_momentum} | Accel: {self.acceleration}"