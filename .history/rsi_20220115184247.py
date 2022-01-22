from Calculate.momentum import Momentum

prices = [
  5.18,
  5.55,
  5.0,
  5.03,
  5.55,
  5.58,
  6.73,
  6.42,
  5.84,
  5.63,
  5.13,
  5.34,
  5.37,
  5.31,
  5.25
  ]


# avg_gain = Momentum.initialAverageGain(prices, 14)
# avg_loss = Momentum.initialAverageLoss(prices, 14)
# rs = (avg_gain/avg_loss)
# irs = (100 - 100/(1+rs))
# print(round(avg_gain, 2), round(avg_loss, 2), rs, irs)
rsis = Momentum.calculateRsis(prices, 14)
rsis = [round(rsi, 2) for rsi in rsis]
print(rsis)