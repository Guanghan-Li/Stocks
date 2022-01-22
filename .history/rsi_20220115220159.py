from Calculate.momentum import Momentum

prices = [
8.6,
8.85,
8.4,
8.4,
8.38,
7.69,
7.99,
7.9,
7.37,
7.15,
6.79,
6.78,
6.44,
6.85,
6.89,
6.84,
6.84,
6.71,
6.21,
6.24,
6.47,
5.89,
5.55,
5.28,
5.45,
5.55,
5.61,
5.6,
5.48,
5.57,
5.74,
5.68,
6.06
6.39,
6.0,
5.94,
5.46,
5.435,
5.84,
6.02,
6.0,
5.67
  ]


# avg_gain = Momentum.initialAverageGain(prices, 14)
# avg_loss = Momentum.initialAverageLoss(prices, 14)
# rs = (avg_gain/avg_loss)
# irs = (100 - 100/(1+rs))
# print(round(avg_gain, 2), round(avg_loss, 2), rs, irs)
rsis = Momentum.calculateRsis(prices, 14)
rsis = [round(rsi, 2) for rsi in rsis]
print(rsis)