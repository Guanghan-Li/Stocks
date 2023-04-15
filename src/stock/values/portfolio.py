class Position:
    def __init__(self, stock, price, amount):
        self.stock = stock
        self.price = price
        self.amount = amount

    @property
    def value(self):
        return self.price * self.amount


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
