from datetime import datetime

from pydantic import BaseModel, Field, root_validator

class Entry(BaseModel):
    stock: str 
    current_date: datetime = Field(..., alias="date")
    open_price: float
    close_price: float
    atr: float
    percent_atr: float
    current_momentum: float = Field(..., alias="one_year_momentum")
    prev_momentum: float = Field(..., alias="two_year_momentum")
    acceleration: float
    rsi14: float
    rsi28: float
    column: str = ""
    trend: str = ""

    def __hash__(self) -> int:
        return hash(f"{self.stock}{self.date_string()}")

    class Config:
        allow_population_by_field_name = True

    def date_string(self):
        return self.current_date.strftime("%Y-%m-%d")

    @staticmethod
    def fromDB(db_entry):
        return Entry(
            stock=db_entry.stock,
            current_date=db_entry.date,
            open_price=db_entry.open_price,
            close_price=db_entry.close_price,
            atr=db_entry.atr,
            percent_atr=db_entry.percent_atr,
            current_momentum=db_entry.one_year_momentum,
            prev_momentum=db_entry.two_year_momentum,
            acceleration=db_entry.acceleration,
            rsi14=db_entry.rsi14,
            rsi28=db_entry.rsi28,
            column=db_entry.column,
            trend=db_entry.trend,
        )

    def to_list(self):
        return [
            self.date_string(),
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
