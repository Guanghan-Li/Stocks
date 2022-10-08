import asyncio, threading
from timeit import *
import os, math, subprocess, time
import mplfinance as mpf
from alpaca_trade_api.rest import *
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from pandas import DataFrame
from psycopg2 import Timestamp
from src.stock.broker import Broker
#import signal
from sty import fg
import txaio, signal

from stock.actors.messages import generate_report, save_report

txaio.use_asyncio()
from autobahn.asyncio.component import Component
from autobahn.asyncio.component import run
import queue, requests, pytz
from requests.auth import HTTPBasicAuth

from thespian.actors import *
from src.stock.actors.broker_actor import BrokerActor
from src.stock.values.prices import Prices, Price
from src.stock.actors.save_price import SavePriceActor
from src.stock.actors.generate_report import GenerateReportActor
from src.stock.actors.save_report import SaveReportActor
from src.stock.actors.task_manager import TaskManagerActor


from src.stock.actors.messages import *

from src.stock.values.tasks import Tasks, Task


#personal
account_info1 = {
      "public_key": 'PKG77R4EUWQ76WC12PI5',
      "private_key": 'YvNim9ia5ov4oJ7WHLv6ElPYQMcMTZMMTP3pLjtp',
      "api_link": 'https://paper-api.alpaca.markets'
}
#08
account_info2 = {
  "public_key": "PKAJ6YB539JWBMJT81Q8",
  "private_key": "clxZoMjA1rc7RFA42aFcbnAwggp95buT1bwGCHxe",
  "api_link": "https://paper-api.alpaca.markets"
}
#02
account_info3 = {
  "public_key": "PKZBZND7F6PH39SMHJPQ",
  "private_key": "2gENBEvKNSEss7zWkY8N290eIANnv32iUeuHPRFy",
  "api_link": "https://paper-api.alpaca.markets"
}
#03
account_info4 = {
  "public_key": "PKQMDMXG2T2FMQ8AZOY5",
  "private_key": "YVdUWYT7hTVPxpkuwDFi07i3Ib8E1AceHPZha46a",
  "api_link": "https://paper-api.alpaca.markets"
}

account_info5 = {
  "public_key": "PKP33J9QMA0IK97MBED5",
  "private_key": "D2cP3slrGwPm3MeAdQdar2MawUNmYMwaK1Wq99lv",
  "api_link": "https://paper-api.alpaca.markets"
}


# from src.stock.repos.announcement_database import AnnouncementDatabase, Announcement
# from src.stock.repos.report_database import ReportDatabase
# announce_db = AnnouncementDatabase()


broker = Broker(account_info1)


# prices = broker.getPriceData("DIG", datetime(2022, 8, 9), datetime(2022, 8, 24))
# weeks = prices.splitByWeek()
# print(len(weeks))

# for week in weeks:
#   print(week)
# quit()
asys = ActorSystem("multiprocQueueBase")
assets = broker.getAllAssets()
asset_amount = len(assets)
#assets2 = broker2.getAllAssets(),
amount = list(zip(*[iter(assets)]*(len(assets)//5)))


accounts = [account_info1, account_info2, account_info3, account_info4, account_info5]
accounts = accounts + accounts

def killed(*args):
  print("SHUTTING DOWN")
  asys.shutdown()


signal.signal(signal.SIGINT, killed)
signal.signal(signal.SIGTERM, killed)
signal.signal(signal.SIGABRT, killed)


def main():
  can_log = True
  start_date = datetime(2018, 7, 25)
  end_date = datetime(2022,7,26)
  broker_actors = []
  task_manager = asys.createActor(TaskManagerActor)
  asys.ask(task_manager, SetupMessage({}, log=can_log))
  for i in range(len(amount)):
    asset_group = amount[i]
    broker_actor = asys.createActor(BrokerActor)
    broker_actors.append(broker_actor)
    save_price_actor = asys.createActor(SavePriceActor)
    gen_report_actor = asys.createActor(GenerateReportActor)
    save_report_actor = asys.createActor(SaveReportActor)

    broker_setup = {
      "name": f"Broker {i}",
      "account_info": accounts[i],
      "save_price_actor": save_price_actor,
      "gen_report_actor": gen_report_actor,
      "task_manager": task_manager
    }
    setup_message = SetupMessage(broker_setup, log=can_log)
    asys.ask(broker_actor, setup_message)
    asys.ask(save_price_actor, SetupMessage({"name": f"Save Price Actor {i}", "task_manager": task_manager}, log=can_log))
    asys.ask(save_report_actor, SetupMessage({"name": f"Save Report Actor {i}", "task_manager": task_manager}, log=can_log))
    asys.ask(gen_report_actor, SetupMessage({"name": f"Gen Report Actor {i}", "save_report_actor": save_report_actor, "task_manager": task_manager}, log=can_log))


  for i in range(len(amount)):
    asset_group = amount[i]
    broker_actor = broker_actors[i]
    get_message = GetPriceMessage(asset_group, start_date, end_date)
    asys.tell(broker_actor, get_message)

  while True: pass

if __name__ == "__main__":
  main()