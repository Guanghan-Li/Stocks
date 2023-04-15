from peewee import *

price_proxy = DatabaseProxy()


def newPrices(name):
    class PricesModel(Model):
        date = DateTimeField(unique=True)
        open = FloatField(null=True)
        high = FloatField(null=True)
        low = FloatField(null=True)
        close = FloatField(null=True)

        class Meta:
            database = price_proxy
            table_name = name

    return PricesModel


class PricesModel(Model):
    date = DateTimeField(unique=True)
    open = FloatField()
    high = FloatField()
    low = FloatField()
    close = FloatField()

    class Meta:
        database = price_proxy
        table_name = "table"
