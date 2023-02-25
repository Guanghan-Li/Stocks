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
import signal

from stock.actors.messages import generate_report, save_report

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

from src.stock.repos.price_database import PricesDatabase

actor_amount = 7
price_database = PricesDatabase()
asys = ActorSystem("multiprocQueueBase")
assets = price_database.database.get_tables()
asset_amount = len(assets)
amount = list(zip(*[iter(assets)]*(len(assets)//actor_amount)))


def killed(*args):
  print("SHUTTING DOWN")
  asys.shutdown()
  quit()


signal.signal(signal.SIGINT, killed)
signal.signal(signal.SIGTERM, killed)
signal.signal(signal.SIGABRT, killed)


def main():
  can_log = True
  report_actors = []
  task_manager = asys.createActor(TaskManagerActor)
  asys.ask(task_manager, SetupMessage({}, log=can_log))
  for i in range(actor_amount):
    asset_group = amount[i]
    gen_report_actor = asys.createActor(GenerateReportActor)
    save_report_actor = asys.createActor(SaveReportActor)

    asys.ask(save_report_actor, SetupMessage({"name": f"Save Report Actor {i}", "task_manager": task_manager}, log=can_log))
    asys.ask(gen_report_actor, SetupMessage({"name": f"Gen Report Actor {i}", "save_report_actor": save_report_actor, "task_manager": task_manager}, log=can_log))
    report_actors.append(gen_report_actor)

  for i in range(actor_amount):
    asset_group = amount[i]
    gen_report_actor = report_actors[i]
    message = GetAllAssetsMessage(asset_group, None)
    asys.tell(gen_report_actor, message)

  while True: pass

if __name__ == "__main__":
  main()