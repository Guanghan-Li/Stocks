from peewee import *

announcement_proxy = DatabaseProxy()

class AnnouncementModel(Model):
  id = CharField(primary_key=True, index=True, unique=True)
  corporate_action_id = CharField()
  ca_type = CharField()
  ca_sub_type = CharField()
  old_rate = FloatField()
  new_rate = FloatField()
  initiating_symbol = CharField()
  target_symbol = CharField()
  ex_date = DateTimeField(null=True)
  record_date = DateTimeField(null=True)
  cash = FloatField()

  class Meta:
      database = announcement_proxy