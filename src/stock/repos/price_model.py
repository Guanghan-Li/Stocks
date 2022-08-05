from peewee import *

price_proxy = DatabaseProxy()

def newPrices(name):
  class Prices(Model):
    date = DateTimeField(unique=True)
    open = FloatField(null=True)
    high = FloatField(null=True)
    low = FloatField(null=True)
    close = FloatField(null=True)

    class Meta:
      database = price_proxy
      table_name = name
  
  return Prices

class Prices(Model):
  date = DateTimeField(unique=True)
  open = FloatField()
  high = FloatField()
  low = FloatField()
  close = FloatField()

  class Meta:
    database = price_proxy
    table_name = 'table'

