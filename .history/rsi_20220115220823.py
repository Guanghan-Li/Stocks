from Calculate.momentum import Momentum

prices = [
9.9,
10.1,
10.27,
10.4,
10.32,
9.56,
9.64,
9.57,
9.905,
10.14,
10.2,
10.24,
10.035,
10.04,
9.9001,
9.65,
9.575,
9.84,
9.685,
9.53,
9.75,
10.05,
10.2,
10.3,
10.5741,
11.28,
11.59,
11.35
  ]


# avg_gain = Momentum.initialAverageGain(prices, 14)
# avg_loss = Momentum.initialAverageLoss(prices, 14)
# rs = (avg_gain/avg_loss)
# irs = (100 - 100/(1+rs))
# print(round(avg_gain, 2), round(avg_loss, 2), rs, irs)
rsis = Momentum.calculateRsis(prices, 14)
rsis = [round(rsi, 2) for rsi in rsis]
print(rsis)