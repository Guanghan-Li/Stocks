from Calculate.momentum import Momentum

prices = [
23.11,
23.72,
23.5,
22.91,
23.07,
22.97,
23.02,
22.8,
23.89,
24.66,
25.11,
25.72,
25.28,
24.89,
24.64,
24.81,
26.14,
26.41,
26.08,
26.38,
26.33,
26.51,
26.95,
26.78,
26.31,
26.12
  ]


# avg_gain = Momentum.initialAverageGain(prices, 14)
# avg_loss = Momentum.initialAverageLoss(prices, 14)
# rs = (avg_gain/avg_loss)
# irs = (100 - 100/(1+rs))
# print(round(avg_gain, 2), round(avg_loss, 2), rs, irs)
rsis = Momentum.calculateRsis(prices, 14)
rsis = [round(rsi, 2) for rsi in rsis]
print(rsis)