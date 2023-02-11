from src.stock.repos.report_database import ReportDatabase, Entry
from src.stock.broker import Broker
from datetime import datetime
import asyncio
from dataclasses import dataclass
from itertools import islice
from prettytable import PrettyTable
from dateutil.relativedelta import relativedelta

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
  if prices.prices:
    profit = prices.prices[0].close - entry.open_price
    return (entry.stock, profit)
  
  return (entry.stock, None)

def sort_momentum2y(entry: Entry) -> float:
  return entry[0].prev_momentum

def chunk(arr_range, arr_size):
    arr_range = iter(arr_range)
    return iter(lambda: tuple(islice(arr_range, arr_size)), ())

async def getResults(rd: ReportDatabase, all_stocks):
  now = datetime.now()
  date = datetime(now.year, now.month, now.day)
  date = date - relativedelta(days=1)
  broker = Broker(account_info1)
  results = {
    "good": [],
    "bad": []
  }
  task_groups = []
  groups = chunk(all_stocks, 50)
  stock_amount = len(all_stocks)
  for group in list(groups)[:5]:
    tasks = []
    for stock in group:
      entries = rd.getMOstRecent(stock)
      entry: Entry = entries[0]
      if entry.rsi28 >= 35 and entry.rsi14 >=30:
        task = asyncio.ensure_future(get_profit(broker, entry, date))
        #res = await get_profit(broker, entry, date)
        tasks.append(task)
    if tasks:
      print("Getting results")
      res = await asyncio.gather(*tasks)
      stock_amount -= 50
      print("Got results -> stocks left:", stock_amount)
      for profit in res:
        if profit[1] is None:
          continue
        if profit[1] < 0:
          results["bad"].append(profit)
        else:
          results["good"].append(profit)
      
  return results

def toCsv(headers, rows, file_name):
  output = ",".join(headers) + "\n"
  for row in rows:
    data = ",".join([str(d) for d in row])
    output += data + "\n"
  
  with open(f"{file_name}.csv", "w") as f:
    f.write(output)

async def main():
  headers = [
    "Date","Stock", "Close Price", "Open Price",
    "2Y Momentum", "1Y Momentum", "Accel", 
    "RSI14", "RSI28", "Column", "Trend", "Profit"
  ]
  rd = ReportDatabase(log=False)
  all_stocks = rd.database.get_tables()
  results = await getResults(rd, all_stocks)
  results['good'].sort(key=lambda x: x[1], reverse=True)
  results['bad'].sort(key=lambda x: x[1])
  good = PrettyTable(headers)
  for stock, profit in results["good"][:10]:
    entry = rd.getMOstRecent(stock)[0]
    row = entry.to_list() + [round(profit, 3)]
    good.add_row(row)

  print(good)
  print()
  bad = PrettyTable(headers)
  for stock, profit in results["bad"][:10]:
    entry = rd.getMOstRecent(stock)[0]
    row = entry.to_list() + [round(profit, 3)]
    bad.add_row(row)

  print(bad)

  toCsv(headers, good.rows, "good")
  toCsv(headers, bad.rows, "bad")

asyncio.run(main())
  