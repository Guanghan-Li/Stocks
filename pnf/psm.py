class PSM:
    def __init__(self, box_size, reversal):
        self.direction = 'DOWN'
        self.box_size = box_size
        self.reversal = reversal
        self.price_types = ['h', 'l']
        self.price_type = 'h'
        