from datetime import datetime


class Entry:
    def __init__(
        self,
        stock,
        current_date,
        open_price,
        close_price,
        atr,
        percent_atr,
        current_momentum,
        prev_momentum,
        acceleration,
        rsi14,
        rsi28,
        column="",
        trend="",
    ):
        self.stock = stock
        self.date: datetime = current_date
        self.atr = atr
        self.open_price = open_price
        self.close_price = close_price
        self.percent_atr = percent_atr
        self.current_momentum = round(current_momentum, 4)
        self.prev_momentum = round(prev_momentum, 4)
        self.acceleration = round(acceleration, 4)
        self.rsi14 = round(rsi14, 2)
        self.rsi28 = round(rsi28, 2)
        self.column = column
        self.trend = trend

    def dateString(self):
        return self.date.strftime("%Y-%m-%d")

    @staticmethod
    def fromDB(db_entry):
        return Entry(
            db_entry.stock,
            db_entry.date,
            db_entry.open_price,
            db_entry.close_price,
            db_entry.atr,
            db_entry.percent_atr,
            db_entry.one_year_momentum,
            db_entry.two_year_momentum,
            db_entry.acceleration,
            db_entry.rsi14,
            db_entry.rsi28,
            column=db_entry.column,
            trend=db_entry.trend,
        )

    def toDict(self):
        return {
            "stock": self.stock,
            "date": self.date,
            "open_price": self.open_price,
            "close_price": self.close_price,
            "atr": self.atr,
            "percent_atr": self.percent_atr,
            "one_year_momentum": self.current_momentum,
            "two_year_momentum": self.prev_momentum,
            "acceleration": self.acceleration,
            "rsi14": self.rsi14,
            "rsi28": self.rsi28,
            "column": self.column,
            "trend": self.trend,
        }

    def to_list(self):
        return [
            self.dateString(),
            self.stock,
            self.close_price,
            self.open_price,
            self.prev_momentum,
            self.current_momentum,
            self.acceleration,
            self.rsi14,
            self.rsi28,
            self.column,
            self.trend,
        ]

    def __str__(self):
        return f"Stock: {self.stock} | Close Price {self.close_price} | Open Price: {self.open_price} | ATR: {self.atr} | Percent ATR: {self.percent_atr} | 2Y Momentum: {self.prev_momentum} | 1Y Momentum: {self.current_momentum} | Accel: {self.acceleration} | RSI14: {self.rsi14} | RSI28: {self.rsi28} | Column: {self.column} | Trend: {self.trend}"
