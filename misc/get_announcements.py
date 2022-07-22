from repos.announcement_database import AnnouncementDatabase
from lib.broker_api.corp import CorporateApi

database = AnnouncementDatabase()
database.setup()
pub_key = "CK2MUIPWZYJOA0RK99NU"
priv_key = "7NNARkkrcdEepZcIJM29PZhkvQZMxXoCXzbT9Swx"
api_link = "https://broker-api.sandbox.alpaca.markets"

corp = CorporateApi(pub_key, priv_key)
announcements = corp.getAllAnnouncements(["split"], '2018-01-01', '2022-06-22')


# announcements = corp.getAnnoucements(['split'], '2020-11-01', '2020-12-01', subtype="reverse_split")
for announcement in announcements:
  try:
    a = database.saveAnnouncement(announcement)
    print(a)
  except Exception as e:
    raise e
    quit()
    #print("ERROR", e, announcement)

announcements = database.get("METX")
print(announcements)