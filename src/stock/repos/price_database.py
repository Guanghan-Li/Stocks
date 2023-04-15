from weakref import proxy
from src.stock.repos.price_model import *
from peewee import *
from playhouse.reflection import generate_models
from pandas import DataFrame
from alpaca_trade_api.rest import *
from alpaca_trade_api.rest import REST
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from time import sleep, strftime

from src.stock.values.prices import Prices, Price
from src.stock.lib.log.log import Log


class PricesDatabase:
    def __init__(self, proxyA=None, db_path=None, log=False):
        info = {"name": db_path, "engine": "peewee.SqliteDatabase"}
        self.log = Log(can_log=log)
        self.proxy: DatabaseProxy = price_proxy
        self.database = PostgresqlDatabase(
            "prices", user="postgres", password="stock", host="localhost", port=5433
        )
        self.proxy.initialize(self.database)
        self.proxy.connect()

    def deleteAll(self):
        tables = [newPrices(t) for t in self.database.get_tables()]
        self.log.info("Prices Amount Before:", len(tables))
        for t in chunked(tables, 50):
            self.database.drop_tables(t)
        self.log.info("Prices Amount After:", len(self.database.get_tables()))

    def getAllStocks(self):
        return self.proxy.get_tables()

    def loadPrices(self, prices: Prices, table, asset=None):
        with self.database.atomic():
            table.insert_many(prices.toDict()).on_conflict_ignore().execute()
        self.log.info("DONE LOADING")

    def setupPrices(self, prices: Prices):
        if len(prices) > 0:
            self.log.info("Loading prices for ", prices.symbol)
            tables = self.proxy.get_tables()
            asset = prices.symbol.replace(".", "_")
            table = newPrices(asset)

            if table not in tables:
                with self.database.atomic():
                    self.proxy.create_tables([table])
            self.loadPrices(prices, table, asset)

        elif len(prices) < 980:
            self.log.info(f"{prices.symbol} not enough data")
            pass

    def getPriceByDay(self, stock, date: datetime) -> Price:
        table = newPrices(stock)
        date = date + timedelta(hours=4)
        query = list(table.select().where(table.date == date))
        price: PricesModel = query[0]

        return Price(stock, price.date, price.open, price.close, price.high, price.low)

    # def updatePrices(self, api):
    #   assets = self.proxy.get_tables()
    #   assets.remove('info')

    #   self.log.info(assets)

    def getPricesFromDB(self, stock) -> Prices:
        table = newPrices(stock)
        db_prices = list(table.select().dicts())
        return Prices.fromDict(stock, db_prices)
