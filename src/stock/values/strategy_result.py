from pydantic import BaseModel
from typing import Optional
from src.stock.values.report import Report
from src.stock.values.strategy import Strategy

class ProfitResult(BaseModel):
    symbol: str
    profit: Optional[float] = None
    cost: Optional[float] = None
    buy_price: Optional[float] = None
    units: Optional[int] = None

    def is_valid(self) -> bool:
        return self.profit is not None or self.cost is not None


class StrategyResult(BaseModel):
    report: Report
    strategy: Strategy
    profit_results: list[ProfitResult]

    class Config:
        arbitrary_types_allowed = True

    @property
    def is_empty(self) -> bool:
        return len(self.profit_results) < 1

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
        if self.cost == 0:
            raise Exception(f"Cost should not be zero -> {self.cost}")
        
        return round(self.profit / self.cost, 3) * 100

    def __str__(self):
        line1 = str(self.strategy)
        line2 = str(self.report.pretty())
        line3 = f"P/L: {self.profit} | Cost: {self.cost} | Percent: {self.percent}"
        lines = ["", line1, line2, line3, ""]

        return "\n".join(lines)


