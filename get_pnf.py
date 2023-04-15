import re
from autobahn.asyncio.component import Component, Session, run
from src.stock.repos.report_database import ReportDatabase
from src.stock.repos.price_database import PricesDatabase, Prices, Price
from datetime import datetime


class UpdatePnf:
    def __init__(self):
        self.report_database = ReportDatabase()
        self.price_database = PricesDatabase()

    async def onJoin(self, session: Session, details):
        print("JOINED WAMP")
        self.session = session

        for symbol in self.report_database.symbols:
            prices: Prices = self.price_database.getPricesFromDB(symbol)
            dates: list[datetime] = self.report_database.getDatesForSymbol(symbol)

            for d in dates:
                date_prices: Prices = prices.getBefore(d)
                send_prices = date_prices.toDict()

                result = await session.call("my.func", symbol, date_prices.toDict2())
                column = result["column"]
                trend = result["trend"]
                print("GOT", column, trend)
                self.report_database.updatePnf(d, symbol, column, trend)

        self.session.leave()


import asyncio

update_pnf = UpdatePnf()
url = "ws://localhost:8080/ws"
realmv = "realm1"
component = Component(transports=url, realm=realmv)
component.on("join", update_pnf.onJoin)

run([component])
