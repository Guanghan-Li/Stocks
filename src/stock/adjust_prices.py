from src.stock.repos.announcement_database import AnnouncementDatabase, Announcement
from datetime import datetime
from functools import partial


class AdjustPrice:
    def __init__(self):
        self.announcement_database = AnnouncementDatabase()

    def reverseSplit(self, price, old_rate, new_rate):
        return round(price * old_rate / new_rate, 3)

    def split(self, price, old_rate, new_rate):
        return round(price * new_rate / old_rate, 3)

    def applySplit(self, announcement: Announcement, price: dict):
        split_type = announcement.ca_sub_type
        new_rate = announcement.new_rate
        old_rate = announcement.old_rate
        adjusted_price = price.copy()
        o_price = price["open"]
        c_price = price["close"]
        h_price = price["high"]
        l_price = price["low"]
        if split_type == "reverse_split":
            func = self.reverseSplit
        elif split_type == "split":
            func = self.split

        adjusted_price["open"] = func(o_price, old_rate, new_rate)
        adjusted_price["close"] = func(c_price, old_rate, new_rate)
        adjusted_price["high"] = func(h_price, old_rate, new_rate)
        adjusted_price["low"] = func(l_price, old_rate, new_rate)

        return adjusted_price

    def dfToDict(self, date, prices):
        return {
            "date": datetime.fromisoformat(date),
            "open": prices["open"][date],
            "close": prices["close"][date],
            "high": prices["high"][date],
            "low": prices["low"][date],
        }

    def applyAnnouncement(self, announcement, prices):
        adjusted_prices = []
        rest_prices = []
        date_format = "%Y-%m-%d"

        for price in prices:
            try:
                price_date = price["date"]
                ann_date = datetime.fromisoformat(
                    announcement.ex_date.strftime(date_format)
                )
                if price_date < ann_date:
                    adjusted_prices.append(price)
                else:
                    rest_prices.append(price)
            except Exception as e:
                print("ERROR", price, e)
                quit()

        applySplit2 = partial(self.applySplit, announcement)
        adjusted_prices = list(map(applySplit2, adjusted_prices))
        new_prices = adjusted_prices + rest_prices
        return new_prices

    def applyAllAnnouncements(self, stock, prices):
        anns = self.announcement_database.listAnnouncements(target_symbol=stock)
        new_prices = prices["data"]
        dates = [str(date) for date in new_prices["open"].keys()]
        new_prices = [self.dfToDict(date, new_prices) for date in dates]

        for ann in anns:
            print(ann)
            new_prices = self.applyAnnouncement(ann, new_prices)
        prices["data"] = new_prices
        return prices
