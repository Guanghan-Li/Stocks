from Calculate.momentum import Momentum

prices = [
17.64,
17.79,
17.57,
17.07,
16.41,
16.18,
15.68,
15.77,
15.27,
14.83,
14.88,
15.92,
15.63,
15.63,
16.16

  ]


# avg_gain = Momentum.initialAverageGain(prices, 14)
# avg_loss = Momentum.initialAverageLoss(prices, 14)
# rs = (avg_gain/avg_loss)
# irs = (100 - 100/(1+rs))
# print(round(avg_gain, 2), round(avg_loss, 2), rs, irs)
rsis = Momentum.calculateRsis(prices, 14)
rsis = [round(rsi, 2) for rsi in rsis]
print(rsis)
