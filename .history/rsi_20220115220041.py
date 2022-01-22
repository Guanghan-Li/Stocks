from Calculate.momentum import Momentum

prices = [
10.09,
10.09,
10.09,
10.09,
10.09,
10.12,
10.11,
10.11,
10.13,
10.13,
10.11,
10.11,
10.13,
10.1,
10.1,
10.09,
10.1,
10.13,
10.13,
10.13,
10.13,
10.13,
10.2,
10.2,
10.1931,
10.1,
10.15,
10.0901,
10.13,
10.06,
10.06,
10.17,
10.17,
10.17,
10.17,
10.17,
10.17,
10.15,
10.15,
10.16,
10.1,
10.1
  ]


# avg_gain = Momentum.initialAverageGain(prices, 14)
# avg_loss = Momentum.initialAverageLoss(prices, 14)
# rs = (avg_gain/avg_loss)
# irs = (100 - 100/(1+rs))
# print(round(avg_gain, 2), round(avg_loss, 2), rs, irs)
rsis = Momentum.calculateRsis(prices, 14)
rsis = [round(rsi, 2) for rsi in rsis]
print(rsis)