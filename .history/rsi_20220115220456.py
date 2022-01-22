from Calculate.momentum import Momentum

prices = [
25.98,
26.17,
26.59,
25.93,
24.92,
23.9,
22.58,
22.31,
21.01,
20.94,
20.88,
22.13,
22.92,
24.0,
24.99,
24.57,
24.58,
24.33,
24.99,
24.75,
24.55,
23.7,
24.0,
24.31,
24.68,
24.41,
24.43,
24.16,
24.0
  ]


# avg_gain = Momentum.initialAverageGain(prices, 14)
# avg_loss = Momentum.initialAverageLoss(prices, 14)
# rs = (avg_gain/avg_loss)
# irs = (100 - 100/(1+rs))
# print(round(avg_gain, 2), round(avg_loss, 2), rs, irs)
rsis = Momentum.calculateRsis(prices, 14)
rsis = [round(rsi, 2) for rsi in rsis]
print(rsis)