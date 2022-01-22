from Calculate.momentum import Momentum

prices = [
  35.44,
  34.77,
  34.06,
  35.01,
  35.43,
  37.2,
  37.02,
  37.28,
  40.1,
  41.3,
  40.42,
  41.45,
  40.53,
  40.43,
  44.86
]


# avg_gain = Momentum.initialAverageGain(prices, 14)
# avg_loss = Momentum.initialAverageLoss(prices, 14)
# rs = (avg_gain/avg_loss)
# irs = (100 - 100/(1+rs))
# print(round(avg_gain, 2), round(avg_loss, 2), rs, irs)
rsis = Momentum.calculateRsis(prices, 14)
rsis = [round(rsi, 2) for rsi in rsis]
print(rsis)