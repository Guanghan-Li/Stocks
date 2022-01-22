from Calculate.momentum import Momentum

prices = [
9.79,
9.79,
9.81,
9.78,
9.79,
9.8,
9.79,
9.78,
9.77,
9.78,
9.76,
9.76,
9.75,
9.75,
9.74,
9.74,
9.74,
9.74,
9.74,
9.76,
9.78,
9.79,
9.76,
9.77,
9.77,
9.77,
9.76,
9.76,
9.74
  ]


# avg_gain = Momentum.initialAverageGain(prices, 14)
# avg_loss = Momentum.initialAverageLoss(prices, 14)
# rs = (avg_gain/avg_loss)
# irs = (100 - 100/(1+rs))
# print(round(avg_gain, 2), round(avg_loss, 2), rs, irs)
rsis = Momentum.calculateRsis(prices, 14)
rsis = [round(rsi, 2) for rsi in rsis]
print(rsis)