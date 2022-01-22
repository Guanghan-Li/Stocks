from Calculate.momentum import Momentum

prices = [
  9.94,
  9.94,
  9.94,
  9.96,
  9.94,
  9.92,
  9.95,
  9.9437,
  9.96,
  9.96,
  9.96,
  9.97,
  9.97,
  9.97,
  9.98
]


# avg_gain = Momentum.initialAverageGain(prices, 14)
# avg_loss = Momentum.initialAverageLoss(prices, 14)
# rs = (avg_gain/avg_loss)
# irs = (100 - 100/(1+rs))
# print(round(avg_gain, 2), round(avg_loss, 2), rs, irs)
rsis = Momentum.calculateRsis(prices, 14)
rsis = [round(rsi, 2) for rsi in rsis]
print(rsis)