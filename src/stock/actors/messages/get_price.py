from datetime import datetime


class GetPriceMessage:
    def __init__(self, assets: list[str], start_date: datetime, end_date: datetime):
        self.assets: list[str] = assets
        self.start_date: datetime = start_date
        self.end_date: datetime = end_date
