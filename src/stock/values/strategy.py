import math
from enum import Enum
from src.stock.values.entry import Entry
import decimal


def round_down(value, decimal_place):
    with decimal.localcontext() as ctx:
        d = decimal.Decimal(value)
        ctx.rounding = decimal.ROUND_DOWN
        return float(round(d, decimal_place))


class Filter(Enum):
    ACCELERATION_MIN = ("acceleration", "min", -2)
    ACCELERATION_MAX = ("acceleration", "max", 0)
    # MOMENTUM_MIN = ("momentum", "min", 1)
    RSI14_MIN = ("rsi14", "min", 20)
    RSI14_MAX = ("rsi14", "max", 45)
    RSI28_MIN = ("rsi28", "min", 25)
    RSI28_MAX = ("rsi28", "max", 50)
    TREND_UP = ("trend", "UP")
    TREND_DOWN = ("trend", "DOWN")
    COLUMN_UP = ("column", "UP")
    COLUMN_DOWN = ("column", "DOWN")

    @staticmethod
    def getFunc(table, filter):
        values = filter.value
        if len(values) == 2:
            return table.__getattribute__(table, values[0]).field == values[1]
        elif values[1] == "min":
            return table.__getattribute__(table, values[0]).field >= values[2]
        elif values[1] == "max":
            return table.__getattribute__(table, values[0]).field <= values[2]

    def check_entry(entry, filter: "Filter") -> bool:
        values = filter.value
        if len(values) == 2:
            return entry.__getattribute__(values[0]) == values[1]

        raise Exception("Not implemented for filter")

    @staticmethod
    def to_list() -> list["Filter"]:
        return [e for e in Filter]


class Cutoff(Enum):
    TEN = 10
    FIFTY = 50
    HUNDRED = 100

    @staticmethod
    def to_list() -> list["Cutoff"]:
        return [e for e in Cutoff]


class PositionSize(Enum):
    EQUAL = "equal"
    RANKING = "ranking"
    # WEIGHT = "weight"

    def handle(self, portfolio_size: int) -> list[float]:
        if self == PositionSize.EQUAL:
            return PositionSize.handle_equal(portfolio_size)
        elif self == PositionSize.RANKING:
            return PositionSize.handle_ranking(portfolio_size)

    @staticmethod
    def handle_equal(portfolio_size: int) -> list[float]:
        percent = round_down(100 / portfolio_size, 2)
        return [percent] * portfolio_size

    @staticmethod
    def handle_ranking(portfolio_size: int) -> list[float]:
        equal = PositionSize.handle_equal(portfolio_size)
        cur = 0
        output = []
        for p in equal:
            res = p - (p * (cur / 100))
            cur += 3
            output.append(round_down(res, 2))

        difference = int(round_down(100 - sum(output), 2) * 100)
        while difference > 0:
            pos = difference % portfolio_size
            factor = portfolio_size - pos
            output[pos] += 0.01 * factor
            difference -= factor

        return sorted([round_down(n, 2) for n in output], reverse=True)

    def handle_weight() -> list[float]:
        raise NotImplementedError

    @staticmethod
    def to_list() -> list["PositionSize"]:
        return [e for e in PositionSize]


class Sorting(Enum):
    ACCELERATION_UP = ("acceleration", "asc")
    ACCELERATION_DOWN = ("acceleration", "desc")
    YEARLY_MOMENTUM_UP = ("current_momentum", "asc")
    YEARLY_MOMENTUM_DOWN = ("current_momentum", "desc")
    TWO_YEAR_MOMENTUM_UP = ("prev_momentum", "asc")
    TWO_YEAR_MOMENTUM_DOWN = ("prev_momentum", "desc")
    RSI14_UP = ("rsi14", "asc")
    RSI14_DOWN = ("rsi14", "desc")
    RSI28_UP = ("rsi28", "asc")
    RSI28_DOWN = ("rsi28", "desc")
    # DIFFERENCE_UP = "DIFFERENCE_UP"
    # DIFFERENCE_DOWN = "DIFFERENCE_DOWN"

    @staticmethod
    def getFunc(table, sorting):
        values = sorting.value
        return table.__getattribute__(table, values[0]).field.__getattribute__(
            values[1]
        )()

    @staticmethod
    def sort(entries: list[Entry], sorting: "Sorting") -> list[Entry]:
        field, order = sorting.value
        reverse = order == "desc"

        def unpack(entry: Entry):
            return entry.__getattribute__(field)

        return sorted(entries, key=unpack, reverse=reverse)

    @staticmethod
    def to_list() -> list["Sorting"]:
        return [e for e in Sorting]


class PortfolioSize(Enum):
    TWO = 2
    FOUR = 4
    SIX = 6

    @staticmethod
    def to_list() -> list["PortfolioSize"]:
        return [e for e in PortfolioSize]


class Strategy:
    def __init__(
        self,
        filters: list[Filter],
        initial_sort: Sorting,
        cutoff: Cutoff,
        secondary_sort: Sorting,
        portfolio_size: PortfolioSize,
        position_size: PositionSize,
    ):
        self.filters: list[Filter] = filters
        self.initial_sort: Sorting = initial_sort
        self.cutoff: Cutoff = cutoff
        self.secondary_sort: Sorting = secondary_sort
        self.portfolio_size: PortfolioSize = portfolio_size
        self.position_size: PositionSize = position_size

    def __str__(self):
        filter_names = ", ".join([filter.name for filter in self.filters])
        filters = f"Filters: [{filter_names}]"
        initial_sort = f"Initial Sort: {self.initial_sort.name}"
        cutoff = f"Cutoff: {self.cutoff.name}"
        secondary_sort = f"Secondary Sort: {self.secondary_sort}"
        portfolio_size = f"Portfolio Size: {self.portfolio_size.name}"
        position_size = f"Position Size: {self.position_size.value}"

        return "Strategy -> " + " | ".join(
            [
                filters,
                initial_sort,
                cutoff,
                secondary_sort,
                portfolio_size,
                position_size,
            ]
        )
