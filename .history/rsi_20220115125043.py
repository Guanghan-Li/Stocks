from Calculate.momentum import Momentum

prices = [
  44.34,
  44.09,
  44.15,
  43.61,
  44.33,
  44.83,
  45.10,
  45.42,
  45.84,
  46.08,
  45.89,
  46.03,
  45.61,
  46.28,
  46.28,
  46.00,
  46.03,
  46.41,
  46.22,
  45.64,
  46.21,
  46.25,
  45.71,
  46.45,
  45.78,
  45.35,
  44.03,
  44.18,
  44.22,
  44.57,
  43.42,
  42.66,
  43.13
]


# avg_gain = Momentum.initialAverageGain(prices, 14)
# avg_loss = Momentum.initialAverageLoss(prices, 14)
# rs = (avg_gain/avg_loss)
# irs = (100 - 100/(1+rs))
# print(round(avg_gain, 2), round(avg_loss, 2), rs, irs)
rsis = Momentum.calculateRsis(prices, 14)
rsis = [round(rsi, 2) for rsi in rsis]
print(rsis)