from re import A
from repos.announcement_model import *
from peewee import *

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from time import strftime
from lib.broker_api.announcement import Announcement

class AnnouncementDatabase:
  def __init__(self):
    self.proxy: DatabaseProxy = announcement_proxy
    self.database = PostgresqlDatabase(
      "announcement",
      user="postgres",
      password="stock",
      host="localhost",
      port=5433
    )
    self.proxy.initialize(self.database)
    self.proxy.connect()

  def setup(self):
    self.database.create_tables([AnnouncementModel])
  
  def dbToAnnouncement(self, db_announcement):
    return Announcement(
      db_announcement.id,
      db_announcement.corporate_action_id,
      db_announcement.ca_type,
      db_announcement.ca_sub_type,
      initiating_symbol=db_announcement.initiating_symbol,
      target_symbol=db_announcement.target_symbol,
      ex_date = db_announcement.ex_date,
      record_date = db_announcement.record_date,
      cash=db_announcement.cash,
      old_rate=db_announcement.old_rate,
      new_rate = db_announcement.new_rate
    )
  
  def saveAnnouncement(self, announcement: Announcement) -> Announcement:
    if announcement.record_date == None:
      record_date = None
    else:
      record_date = datetime.fromisoformat(announcement.record_date)

    if announcement.ex_date == None:
      ex_date = None
    else:
      ex_date = datetime.fromisoformat(announcement.ex_date)

    with self.database.atomic():
      if AnnouncementModel.select().where(AnnouncementModel.id == announcement.id).exists():
        db_announcement = AnnouncementModel.get_by_id(announcement.id)
      else:
        db_announcement = AnnouncementModel.create(
          id = announcement.id,
          corporate_action_id = announcement.corporate_action_id,
          ca_type = announcement.ca_type,
          ca_sub_type = announcement.ca_sub_type,
          initiating_symbol = announcement.initiating_symbol,
          target_symbol = announcement.target_symbol,
          ex_date = announcement.ex_date,
          record_date = announcement.record_date,
          cash = announcement.cash,
          old_rate = announcement.old_rate,
          new_rate = announcement.new_rate
        )

    return self.dbToAnnouncement(db_announcement)

  def listAnnouncements(self, target_symbol=None):
    if target_symbol == None:
      dbs = list(AnnouncementModel.select())
    else:
      dbs = list(AnnouncementModel.select().where(AnnouncementModel.target_symbol == target_symbol))

    return [self.dbToAnnouncement(a) for a in dbs]

  def exist(self, target_symbol):
    query = AnnouncementModel.select().where(AnnouncementModel.target_symbol == target_symbol)
    return query.exists()

  def get(self, target_symbol):
    if self.exist(target_symbol):
      query = list(AnnouncementModel.select().where(AnnouncementModel.target_symbol == target_symbol))[0]
      return self.dbToAnnouncement(query)
    else:
      return None
