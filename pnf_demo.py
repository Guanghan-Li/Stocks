from pyoink.values.chart import Chart
from stock.broker import Broker
from datetime import datetime

account_info1 = {
      "public_key": 'PK22ZH3C6B3Z2JB1JSDC',
      "private_key": 'ihZzYfEPD94xIVzJANzUKpghdg1Y4Z2uCQO9Tn2w',
      "api_link": 'https://paper-api.alpaca.markets'
}

broker = Broker(account_info1)
stock = "F"
prices = broker.getPriceData(stock, datetime(2021, 8, 9), datetime(2022, 12, 2))
chart = Chart(stock, 0.25, 3)
chart.generate(prices.toSimpleDict())
chart.generateTrends()
chart.toHtml("dig.html")