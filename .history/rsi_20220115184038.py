from Calculate.momentum import Momentum

prices = [
  16.42,
  16.29,
  16.24,
  16.32,
  16.45,
  16.25,
  16.24,
  16.1,
  15.36,
  15.4,
  15.88,
  16.18,
  16.78,
  16.74,
  16.25
]


# avg_gain = Momentum.initialAverageGain(prices, 14)
# avg_loss = Momentum.initialAverageLoss(prices, 14)
# rs = (avg_gain/avg_loss)
# irs = (100 - 100/(1+rs))
# print(round(avg_gain, 2), round(avg_loss, 2), rs, irs)
rsis = Momentum.calculateRsis(prices, 14)
rsis = [round(rsi, 2) for rsi in rsis]
print(rsis)