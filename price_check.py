from src.stock.repos.report_database import ReportDatabase, Entry
from src.stock.broker import Broker
from datetime import datetime
import asyncio
from dataclasses import dataclass

@dataclass
class Results:
  good=[]
  bad=[]

#1
account_info1 = {
      "public_key": 'PK22ZH3C6B3Z2JB1JSDC',
      "private_key": 'ihZzYfEPD94xIVzJANzUKpghdg1Y4Z2uCQO9Tn2w',
      "api_link": 'https://paper-api.alpaca.markets'
}

async def get_profit(broker: Broker, entry: Entry, date):
  prices = await broker.getPrices(entry.stock, date, date)
  profit = prices.prices[0].close - entry.open_price
  return (entry.stock, profit)

def sort_momentum2y(entry: Entry) -> float:
  return entry[0].prev_momentum

async def getResults(rd: ReportDatabase, all_stocks):
  now = datetime.now()
  date = datetime(now.year, now.month, now.day-1)
  broker = Broker(account_info1)
  results = {
    "good": [],
    "bad": []
  }
  tasks = []
  for stock in all_stocks:
    entries = rd.getMOstRecent(stock)
    entry: Entry = entries[0]
    if entry.rsi28 >= 35 and entry.rsi14 >=30:
      print("Task for ", entry.stock)
      res = await get_profit(broker, entry, date)
      print(res)
      #tasks.append(task)
  
  # res = await asyncio.gather(*tasks)
  # for i in res:
  #   print(res)

      
  return results

async def main():
  rd = ReportDatabase(log=False)
  all_stocks = rd.database.get_tables()
  await getResults(rd, all_stocks[:2])

asyncio.run(main())
  