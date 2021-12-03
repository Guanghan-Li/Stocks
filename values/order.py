class Order:
    def __init__(self, stock, amount, position, price):
        self.stock = stock
        self.amount = amount
        self.position = position
        self.price = price

    def __str__(self):
        return 'Order: Stock {}, Amount: {}, Position: {}, Price: {}'.format(self.stock, self.amount, self.position, self.price)