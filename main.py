import asyncio
import math
from src.stock.broker import Broker
from src.stock.values.entry import Entry
from src.stock.repos.report_database import ReportDatabase
from src.stock.values.portfolio import Position
from src.stock.values.report import Report
from prettytable import PrettyTable
from src.stock.values.strategy import (
    Strategy,
    Sorting,
    Cutoff,
    Filter,
    PortfolioSize,
    PositionSize,
    round_down,
)
from src.stock.values.strategy_result import ProfitResult, StrategyResult

from datetime import datetime
from dateutil.relativedelta import relativedelta

account_info1 = {
    "public_key": "PKG77R4EUWQ76WC12PI5",
    "private_key": "YvNim9ia5ov4oJ7WHLv6ElPYQMcMTZMMTP3pLjtp",
    "api_link": "https://paper-api.alpaca.markets",
}

def get_units(budget: float, percent: float, price: float) -> int:
    cost = (budget * percent) / 100

    if price > cost:
        return 0

    return math.floor(cost / price)

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
    
def get_positions(strategy: Strategy, report: Report, budget=10_000) -> list[Position]:
    out: list[Position] = []
    percents = PositionSize(strategy.position_size).handle(len(report.entries))
    data = zip(percents, report.entries)
    for percent, entry in data:
        units = get_units(budget, percent, entry.open_price)
        pos = Position(stock=entry.stock, price=entry.open_price, amount=units)
        out.append(pos)
    return out

    
async def main():
    now = datetime.now() - relativedelta(days=1)
    before = now - relativedelta(weeks=104)

    broker = Broker(account_info1)
    report_database = ReportDatabase(False)

    strategy = Strategy.parse_file("best_strategy.json")

    print(strategy)
    date = datetime(2023, 5, 17)
    results = report_database.get_reports(date, strategy, [])
    positions = get_positions(strategy, results)

    headers = [
        "Stock",
        "Open Price",
        "Amount",
        "Cost"
    ]
    table = PrettyTable(headers)

    for position in positions:
        table.add_row(position.to_list())

    print(table)
    #print(prices)

asyncio.run(main())