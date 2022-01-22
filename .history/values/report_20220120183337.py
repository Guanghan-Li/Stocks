from Calculate.momentum import Momentum

class Report:
  def __init__(self, date, entries, number_of_positions):
    self.date = date
    self.entries = entries[:number_of_positions]
    self.stocks = [entry.stock for entry in self.entries]
  
  def get(self, stock):
    for entry in self.entries:
      if entry.stock == stock:
        return entry
    
    return None

  def __str__(self):
    str_entries = [str(entry) for entry in self.entries]
    report = [
      f"Report for {self.date.isoformat()}"
    ] + str_entries
    return "\n".join(report)

class Entry:
  def __init__(self, stock, current_date, open_price, close_price, atr, percent_atr, current_momentum, prev_momentum, acceleration, rsi, column='', trend=''):
    self.stock = stock
    self.date = current_date
    self.atr = atr
    self.open_price = open_price
    self.close_price = close_price
    self.percent_atr = percent_atr
    self.current_momentum = round(current_momentum, 4)
    self.prev_momentum = round(prev_momentum, 4)
    self.acceleration = round(acceleration, 4)
    self.rsi = round(rsi, 2)
    self.column = column
    self.trend = trend

  @staticmethod
  def fromDB(db_entry):
    return Entry(
      db_entry.stock,
      db_entry.date,
      db_entry.open_price,
      db_entry.close_price,
      db_entry.atr,
      db_entry.percent_atr,
      db_entry.one_year_momentum,
      db_entry.two_year_momentum,
      db_entry.acceleration,
      db_entry.rsi,
      column = db_entry.column,
      trend = db_entry.trend
    )

  def __str__(self):
    return f"Stock: {self.stock} | Close Price {self.close_price} | Open Price: {self.open_price} | ATR: {self.atr} | Percent ATR: {self.percent_atr} | 2Y Momentum: {self.prev_momentum} | 1Y Momentum: {self.current_momentum} | Accel: {self.acceleration} | Column: {self.column} | Trend: {self.trend}"