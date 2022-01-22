from Calculate.momentum import Momentum

prices = [
51.51,
51.67,
51.53,
51.44,
51.5,
51.5,
51.41,
51.41,
51.45,
51.57,
51.65,
51.63,
51.67,
51.59,
51.57,
51.64,
51.65,
51.68,
51.69,
51.62,
51.56,
51.61,
51.62,
51.61,
51.62,
51.65,
51.56,
51.63,
51.8
  ]


# avg_gain = Momentum.initialAverageGain(prices, 14)
# avg_loss = Momentum.initialAverageLoss(prices, 14)
# rs = (avg_gain/avg_loss)
# irs = (100 - 100/(1+rs))
# print(round(avg_gain, 2), round(avg_loss, 2), rs, irs)
rsis = Momentum.calculateRsis(prices, 14)
rsis = [round(rsi, 2) for rsi in rsis]
print(rsis)