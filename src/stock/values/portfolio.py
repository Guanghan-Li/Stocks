from pydantic import BaseModel

class Position(BaseModel):
    stock: str
    price: float
    amount: int = 1

    @property
    def value(self):
        return round(self.price * self.amount,2)
    
    def to_list(self) -> list:
        return [
            self.stock,
            self.price,
            self.amount,
            self.value
        ]


class Portfolio:
    def __init__(self):
        self.money = 100000
        self.positions = []

    def availableMoney(self):
        return self.money // 3

    @property
    def value(self):
        position_values = [position.value for position in self.positions]
        position_value = sum(position_values)
        return self.money + position_value

    def updatePrices(self):
        pass
