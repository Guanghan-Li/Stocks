from peewee import *

report_proxy = DatabaseProxy()

def newReport(name):
  class Reports(Model):
    date = DateTimeField()
    stock = CharField()
    open_price = FloatField()
    close_price = FloatField()
    atr = FloatField()
    percent_atr = FloatField()
    two_year_momentum = FloatField()
    one_year_momentum = FloatField()
    acceleration = FloatField()
    column = CharField(default='')
    trend = CharField(default='')

    class Meta:
      database = report_proxy
      table_name = name
  
  return Reports

class Reports(Model):
  date = DateTimeField()
  stock = CharField()
  open_price = FloatField()
  close_price = FloatField()
  atr = FloatField()
  percent_atr = FloatField()
  two_year_momentum = FloatField()
  one_year_momentum = FloatField()
  acceleration = FloatField()
  column = CharField(default='')
  trend = CharField(default='')


  class Meta:
    database = report_proxy
    table_name = 'table'

class Info(Model):
  last_updated = DateTimeField(unique=True)