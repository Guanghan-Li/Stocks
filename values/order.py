class Order:
    def __init__(self, stock, amount, position):
        self.stock = stock
        self.amount = amount
        self.position = position

    def __str__(self):
        return 'Order: Stock {}, Amount: {}, Position: {}'.format(self.stock, self.amount, self.position)