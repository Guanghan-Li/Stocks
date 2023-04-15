from autobahn.asyncio.component import Component, run
from src.stock.broker import Broker
from datetime import datetime
from dateutil.relativedelta import relativedelta
from pyoink.values.chart import Chart

account_info1 = {
    "public_key": "PK22ZH3C6B3Z2JB1JSDC",
    "private_key": "ihZzYfEPD94xIVzJANzUKpghdg1Y4Z2uCQO9Tn2w",
    "api_link": "https://paper-api.alpaca.markets",
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
        box_size = result["box_size"]
        print(result)

        chart = Chart("symbol", box_size, 3)
        chart.generate(prices.toSimpleDict())
        chart.generateTrends()
        print(chart.last_column.direction, chart.trends[-1].direction, box_size)
        possible_box_size = Chart.getBoxSizeATR(prices, length=20)
        chart = Chart("symbol", possible_box_size, 3)
        chart.generate(prices.toSimpleDict())
        chart.generateTrends()
        print(
            chart.last_column.direction, chart.trends[-1].direction, possible_box_size
        )
    else:
        print("No prices to send")
    session.leave()


run([component])
