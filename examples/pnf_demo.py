from pyoink.values.chart import Chart
from stock.broker import Broker
from datetime import datetime

account_info1 = {
    "public_key": "PK22ZH3C6B3Z2JB1JSDC",
    "private_key": "ihZzYfEPD94xIVzJANzUKpghdg1Y4Z2uCQO9Tn2w",
    "api_link": "https://paper-api.alpaca.markets",
}

broker = Broker(account_info1)
prices = broker.getPriceData("DIG", datetime(2021, 8, 9), datetime(2022, 8, 24))
chart = Chart("DIG", 1.0, 3)
chart.generate(prices.toSimpleDict())
chart.toHtml("dig.html")

