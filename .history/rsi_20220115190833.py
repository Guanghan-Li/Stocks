from Calculate.momentum import Momentum

prices = [
142.15,
147.2,
146.22,
150.37,
150.81,
153.34,
152.94,
152.71,
150.43,
149.1,
150.4,
148.75,
148.76,,
146.47,
151.05,
151.88,
153.63,
152.8,
155.2,
154.87,
155.93,
154.89,
156.76,
155.73,
155.19,
156.9,
157.83,
156.6,
157.89,
157.8,
155.44,
151.94
  ]


# avg_gain = Momentum.initialAverageGain(prices, 14)
# avg_loss = Momentum.initialAverageLoss(prices, 14)
# rs = (avg_gain/avg_loss)
# irs = (100 - 100/(1+rs))
# print(round(avg_gain, 2), round(avg_loss, 2), rs, irs)
rsis = Momentum.calculateRsis(prices, 14)
rsis = [round(rsi, 2) for rsi in rsis]
print(rsis)