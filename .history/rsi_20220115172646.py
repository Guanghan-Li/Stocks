from Calculate.momentum import Momentum

prices = [
  115.02,
  102.32,
  100.56,
  105.75,
  97.37,
  94.76,
  97.37,
  92.21,
  97.52,
  90.95,
  81.09,
  82.33,
  83.16,
  86.17,
  88.46
]


# avg_gain = Momentum.initialAverageGain(prices, 14)
# avg_loss = Momentum.initialAverageLoss(prices, 14)
# rs = (avg_gain/avg_loss)
# irs = (100 - 100/(1+rs))
# print(round(avg_gain, 2), round(avg_loss, 2), rs, irs)
rsis = Momentum.calculateRsis(prices, 14)
rsis = [round(rsi, 2) for rsi in rsis]
print(rsis)