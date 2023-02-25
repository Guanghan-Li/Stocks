from timeit import *
from alpaca_trade_api.rest import *
from datetime import datetime
from src.stock.broker import Broker
import signal

from thespian.actors import *
from src.stock.actors.broker_actor import BrokerActor
from src.stock.actors.save_price import SavePriceActor
from src.stock.actors.task_manager import TaskManagerActor


from src.stock.actors.messages import *
from chan import Chan


# #personal
# account_info1 = {
#       "public_key": 'PKG77R4EUWQ76WC12PI5',
#       "private_key": 'YvNim9ia5ov4oJ7WHLv6ElPYQMcMTZMMTP3pLjtp',
#       "api_link": 'https://paper-api.alpaca.markets'
# }
# #08
# account_info2 = {
#   "public_key": "PKAJ6YB539JWBMJT81Q8",
#   "private_key": "clxZoMjA1rc7RFA42aFcbnAwggp95buT1bwGCHxe",
#   "api_link": "https://paper-api.alpaca.markets"
# }
# #02
# account_info3 = {
#   "public_key": "PKZBZND7F6PH39SMHJPQ",
#   "private_key": "2gENBEvKNSEss7zWkY8N290eIANnv32iUeuHPRFy",
#   "api_link": "https://paper-api.alpaca.markets"
# }
# #03
# account_info4 = {
#   "public_key": "PKQMDMXG2T2FMQ8AZOY5",
#   "private_key": "YVdUWYT7hTVPxpkuwDFi07i3Ib8E1AceHPZha46a",
#   "api_link": "https://paper-api.alpaca.markets"
# }

# account_info5 = {
#   "public_key": "PKP33J9QMA0IK97MBED5",
#   "private_key": "D2cP3slrGwPm3MeAdQdar2MawUNmYMwaK1Wq99lv",
#   "api_link": "https://paper-api.alpaca.markets"
# }

#1
account_info1 = {
      "public_key": 'PK22ZH3C6B3Z2JB1JSDC',
      "private_key": 'ihZzYfEPD94xIVzJANzUKpghdg1Y4Z2uCQO9Tn2w',
      "api_link": 'https://paper-api.alpaca.markets'
}
#2
account_info2 = {
  "public_key": "PKXTOW2DFRAOYDU29XO9",
  "private_key": "JeMTNZXWJoge0dIoRbndOelTcWqlxysbQndh3XGw",
  "api_link": "https://paper-api.alpaca.markets"
}
#3
account_info3 = {
  "public_key": "PKMXHRH2KM0Z29935SH9",
  "private_key": "YkO4Izloj3mxN9rSvJsCS5BJtzPvyl38IvAsgBO2",
  "api_link": "https://paper-api.alpaca.markets"
}
#4
account_info4 = {
  "public_key": "PKKYX28AK5ON4C2BT4F3",
  "private_key": "EtnwXKOQYfDx2qcwaboKNSJjoNnOZNaL9gvNJKnm",
  "api_link": "https://paper-api.alpaca.markets"
}
#5
account_info5 = {
  "public_key": "PKCOPWLFO2UW71KJ6F6S",
  "private_key": "36Au0YQnlxZF9tHiRYFOcOYey7dIgiBah01GjPcK",
  "api_link": "https://paper-api.alpaca.markets"
}


# # from src.stock.repos.announcement_database import AnnouncementDatabase, Announcement
# from src.stock.repos.report_database import ReportDatabase
# # announce_db = AnnouncementDatabase()
# import json

broker = Broker(account_info1)

# # start = datetime.now()
# rd = ReportDatabase()
# prices = broker.getPriceData("F", datetime(2018, 8, 9), datetime(2022, 8, 24))
# data = prices.toSimpleDict()
# with open("DIG.json", "w") as f:
#   json.dump(data, f)
# entry = rd.generateEntry(prices)
# print(entry)
# quit()

asys = ActorSystem("multiprocQueueBase")
assets = broker.getAllAssets()
asset_amount = len(assets)
#assets2 = broker2.getAllAssets(),
group_amount = 5
amount = list(zip(*[iter(assets)]*(len(assets)//group_amount)))


accounts = [account_info1, account_info2, account_info3, account_info4, account_info5]
accounts = accounts + accounts

def killed(*args):
  print("SHUTTING DOWN")
  asys.shutdown()


signal.signal(signal.SIGINT, killed)
signal.signal(signal.SIGTERM, killed)
signal.signal(signal.SIGABRT, killed)


def main():
  channel = Chan()
  can_log = True
  start_date = datetime(2019, 1, 30)
  end_date = datetime(2023,2,1)
  broker_actors = []
  task_manager = asys.createActor(TaskManagerActor)
  asys.ask(task_manager, SetupMessage({}, log=can_log))
  for i in range(group_amount):
    asset_group = amount[i]
    broker_actor = asys.createActor(BrokerActor)
    broker_actors.append(broker_actor)
    save_price_actor = asys.createActor(SavePriceActor)

    broker_setup = {
      "name": f"Broker {i}",
      "account_info": accounts[i],
      "save_price_actor": save_price_actor,
      "channel": channel
    }
    setup_message = SetupMessage(broker_setup, log=can_log)
    asys.ask(broker_actor, setup_message)
    asys.ask(save_price_actor, SetupMessage({"name": f"Save Price Actor {i}", "task_manager": task_manager}, log=can_log))


  for i in range(group_amount):
    asset_group = amount[i]
    broker_actor = broker_actors[i]
    get_message = GetPriceMessage(asset_group, start_date, end_date)
    asys.tell(broker_actor, get_message)

  while True: pass

if __name__ == "__main__":
  main()