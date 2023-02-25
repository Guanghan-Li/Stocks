from autobahn.asyncio.component import Component, run
from src.stock.broker import Broker
from datetime import datetime
from dateutil.relativedelta import relativedelta
from pyoink.values.chart import Chart

account_info1 = {
      "public_key": 'PK22ZH3C6B3Z2JB1JSDC',
      "private_key": 'ihZzYfEPD94xIVzJANzUKpghdg1Y4Z2uCQO9Tn2w',
      "api_link": 'https://paper-api.alpaca.markets'
}
component = Component(transports={"url": "ws://0.0.0.0:8080"}, realm="realm1")
broker = Broker(account_info1)

@component.on_join
async def joined(session, details):
    print("session ready")
    now = datetime.now()
    date = datetime(now.year, now.month, now.day)
    end = date - relativedelta(days=1)
    start = date - relativedelta(years=4)
    prices = broker.getPriceData("AAPL", start, end)
    if prices.prices:
      result = await session.call("my.func", "AAPL", prices.toDict())
      print(result)
      #chart = Chart("symbol")
    else:
       print("No prices to send")
    session.leave()
  
run([component])