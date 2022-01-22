from asyncio import set_event_loop


class Momentum:

  @staticmethod
  def netReturn(start_price, end_price):
    return (end_price-start_price) / start_price
  
  @staticmethod
  def grossReturn(start_price, end_price):
    return Momentum.netReturn(start_price, end_price) + 1
  
  @staticmethod
  def momentumOneMonth(month_data):
    start = month_data[0]['open']
    end = month_data[-1]['close']
    return Momentum.grossReturn(start, end)
  
  @staticmethod
  def momentumOneYear(year_data):
    gross_returns = []

    for month in year_data:
      one_month_momentum = Momentum.momentumOneMonth(month)
      gross_returns.append(one_month_momentum)
    
    momentum = Momentum.product(gross_returns) + 1

    return momentum
#https://school.stockcharts.com/doku.php?id=technical_indicators:relative_strength_index_rsi

  @staticmethod
  def calculateRsis(prices, period):
    rsis = []
    initial_avg_gain = Momentum.initialAverageGain(prices, period)
    initial_avg_loss = Momentum.initialAverageLoss(prices, period)
    prices = prices[period:]
    for i in range(1, len(prices)):
      rs = Momentum.rs(initial_avg_gain, initial_avg_loss)
      rsi = Momentum.rsi(rs)
      rsis.append(rsi)
      first_price = prices[i-1]["close"]
      second_price = prices[i]["close"]
      gain = Momentum.gain(first_price, second_price)
      loss = Momentum.loss(first_price, second_price)
      initial_avg_gain = Momentum.averageGain(initial_avg_gain, gain, period)
      initial_avg_loss = Momentum.averageLoss(initial_avg_loss, loss, period)
    rs = Momentum.rs(initial_avg_gain, initial_avg_loss)
    rsi = Momentum.rsi(rs)
    rsis.append(rsi)
    return rsis

  @staticmethod
  def rs(averageGain, averageLoss):
    if averageLoss == 0:
      return 100.0
    return averageGain / averageLoss

  @staticmethod
  def averageLoss(initial_average_loss, current_loss, period):
    return (initial_average_loss*(period-1) + current_loss) / period

  @staticmethod
  def averageGain(initial_average_gain, current_gain, period):
    return (initial_average_gain*(period-1) + current_gain) / period

  @staticmethod
  def rsi(rs):
    return 100 - 100/(1+rs)

  @staticmethod
  def initialAverageGain(prices, period):
    gains = []
    lookback = len(prices) - period - 1
    for i in range(1, len(prices[lookback:])):
      first_price = prices[i-1]["close"]
      second_price = prices[i]["close"]
      gain = Momentum.gain(first_price, second_price)
      gains.append(gain)
    
    return sum(gains) / period

  @staticmethod
  def initialAverageLoss(prices, period):
    losses = []
    lookback = len(prices) - period - 1
    for i in range(1, len(prices[:period])):
      first_price = prices[i-1]["close"]
      second_price = prices[i]["close"]
      loss = Momentum.loss(first_price, second_price)
      losses.append(loss)
    
    return sum(losses) / period

  @staticmethod
  def gain(price1, price2):
    result = price2 - price1
    if result > 0:
      return result
    else:
      return 0

  @staticmethod
  def loss(price1, price2):
    result = price2 -  price1
    if result < 0:
      return abs(result)
    else:
      return 0

  @staticmethod
  def product(numbers):
    result = 1
    for number in numbers:
      result *= number
    
    return result