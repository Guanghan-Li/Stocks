from peewee import *
from src.stock.repos.report_model import *
from pandas import DataFrame
from alpaca_trade_api.rest import *
from alpaca_trade_api.rest import REST
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from src.stock.calculate.calculations import Calculations
from src.stock.calculate.momentum import Momentum
from src.stock.values.report import Entry, Report
from time import sleep, strftime
from peewee import FieldAccessor

from src.stock.values.strategy import *
from src.stock.values.prices import Prices, Price

from src.stock.lib.log.log import Log


class ReportYearDatabase:
    def __init__(self, log=False):
        self.proxy = report_proxy
        # self.proxy.initialize(SqliteDatabase(name))
        self.database = PostgresqlDatabase(
            "reports_by_year",
            user="postgres",
            password="stock",
            host="localhost",
            port=5433,
        )
        self.log = Log(can_log=log)
        self.proxy.initialize(self.database)
        self.proxy.connect()
        # self.price_repo = price_repo

    def deleteAll(self):
        tables = [newReport(t) for t in self.database.get_tables()]
        self.log.info("Reports Amount Before:", len(tables))
        self.database.drop_tables(tables)
        self.log.info("Reports Amount After:", len(self.database.get_tables()))

    def saveEntries(self, entries):
        data = [entry.toDict() for entry in entries]
        table = newReport(entries[0].stock)
        tables = self.proxy.get_tables()
        if table not in tables:
            self.proxy.create_tables([table])

        with self.database.atomic():
            table.insert_many(data).execute()

        print(f"SAVED {entries[0].stock} " * 10)
