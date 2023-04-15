import asyncio
import math
from alpaca_trade_api.rest import *
from src.stock.repos.report_model import *
from src.stock.repos.price_database import *
from src.stock.values.report import Entry, Report
from src.stock.repos.price_database import PricesDatabase
from src.stock.calculate.momentum import Momentum
from src.stock.values.order import Order
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from src.stock.repos.report_database import ReportDatabase
from src.stock.broker import Broker
from src.stock.values.portfolio import Portfolio
import itertools
from dataclasses import dataclass
from tqdm import tqdm
from itertools import islice

from src.stock.values.strategy import (
    Strategy,
    Sorting,
    Cutoff,
    Filter,
    PortfolioSize,
    PositionSize,
    round_down,
)
from threading import Thread


@dataclass
class ProfitResult:
    symbol: str
    profit: float = None
    cost: float = None
    buy_price: float = None
    units: int = None

    def is_valid(self) -> bool:
        return self.profit is not None or self.cost is not None


@dataclass
class StrategyResult:
    report: Report
    strategy: Strategy
    profit_results: list[ProfitResult]

    @property
    def cost(self) -> float:
        costs = [pr.cost for pr in self.profit_results]
        cost = sum(costs)
        return round(cost, 5)

    @property
    def profit(self) -> float:
        profits = [pr.profit for pr in self.profit_results]
        profit = sum(profits)
        return round(profit, 5)

    @property
    def percent(self) -> float:
        return round(self.profit / self.cost, 3) * 100

    def __str__(self):
        line1 = str(self.strategy)
        line2 = str(self.report.pretty())
        line3 = f"P/L: {self.profit} | Cost: {self.cost} | Percent: {self.percent}"
        lines = ["", line1, line2, line3, ""]

        return "\n".join(lines)


account_info1 = {
    "public_key": "PKG77R4EUWQ76WC12PI5",
    "private_key": "YvNim9ia5ov4oJ7WHLv6ElPYQMcMTZMMTP3pLjtp",
    "api_link": "https://paper-api.alpaca.markets",
}


async def get_profit(
    broker: Broker, entry: Entry, date: datetime, percent: float
) -> ProfitResult:
    prices = await broker.getPrices(entry.stock, date, date)
    budget = 10_000
    units = get_units(budget, percent, entry.open_price)
    buy_price = entry.open_price * units
    if prices.prices:
        profit = (prices.prices[0].close * units) - (entry.open_price * units)
        return ProfitResult(
            symbol=entry.stock,
            profit=profit,
            cost=buy_price,
            buy_price=entry.open_price,
            units=units,
        )

    return ProfitResult(symbol=entry.stock)


async def get_all_profit(
    broker: Broker, entries: list[Entry], date: datetime, strategy: Strategy
):
    tasks = []
    percents = strategy.position_size.handle(len(entries))
    data = dict(zip(entries, percents))
    for entry, percent in data.items():
        task = asyncio.create_task(get_profit(broker, entry, date, percent))
        tasks.append(task)

    results: list[ProfitResult] = await asyncio.gather(*tasks)
    out_results = [pr for pr in results if pr.is_valid()]

    return out_results


def chunk(arr_range, arr_size):
    arr_range = iter(arr_range)
    return iter(lambda: tuple(islice(arr_range, arr_size)), ())


def get_units(budget: float, percent: float, price: float) -> int:
    cost = (budget * percent) / 100

    if price > cost:
        return 0

    return math.floor(cost / price)


def generate_strategies():
    p = itertools.product(
        Sorting.to_list(),
        Cutoff.to_list(),
        Sorting.to_list(),
        PortfolioSize.to_list(),
        PositionSize.to_list(),
    )
    strategies = []
    for strat in p:
        options = [[Filter.COLUMN_UP, Filter.TREND_UP]] + list(strat)
        strategy = Strategy(*options)
        strategies.append(strategy)

    return strategies


def thread_runner(loop: asyncio.AbstractEventLoop):
    ...


async def run_strategy(
    report_database: ReportDatabase, account_info: dict, strategy: Strategy
) -> StrategyResult:
    broker = Broker(account_info)
    now = datetime(2023, 3, 22)
    later = now + relativedelta(weeks=1)
    report = report_database.get_reports(now, strategy, [])
    results = await get_all_profit(broker, report.entries, later, strategy)

    return StrategyResult(report=report, profit_results=results, strategy=strategy)


async def main():
    all_strategies = list(chunk(generate_strategies(), 10))
    report_database = ReportDatabase()
    results = []
    loop = asyncio.get_running_loop()
    for strategies in tqdm(all_strategies[:10]):
        tasks = []

        for strategy in strategies:
            task = asyncio.create_task(
                run_strategy(report_database, account_info1, strategy)
            )
            tasks.append(task)
        result = await asyncio.gather(*tasks)
        results += result

    results = sorted(results, key=lambda r: r.profit, reverse=True)
    for r in results[:2]:
        print(r)


asyncio.run(main())
