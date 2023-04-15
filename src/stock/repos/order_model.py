from peewee import *

order_proxy = DatabaseProxy()


class Orders(Model):
    date = DateTimeField()
    price = FloatField()
    stock = CharField()
    amount = IntegerField()
    order_type = CharField()

    class Meta:
        database = order_proxy
        table_name = "table"
