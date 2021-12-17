from autobahn.asyncio.component import Component, run, Session
from asyncio import sleep
import os
import argparse
import six
from repos.price_database import PricesDatabase
from repos.report_database import ReportDatabase
from repos.price_model import *
from repos.report_model import *
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta

url = os.environ.get('CBURL', u'ws://localhost:8080/ws')
realmv = os.environ.get('CBREALM', u'realm1')
print(url, realmv)
component = Component(transports=url, realm=realmv)
prices_database = PricesDatabase(price_proxy)
reports_database = ReportDatabase(report_proxy, prices_database)

def prepareData(prices):
    price_data = []
    for price in prices:
        new_price = {
            'h': price['high'],
            'l': price['low']
        }
        price_data.append(new_price)
    return price_data

async def updateReport(session, current_date, stocks):
    for stock in stocks:
        # if reports_database.filledPNF(current_date, stock):
        #     continue
        prices = prices_database.getTwoYearPrices(stock, current_date)
        price_data = prepareData(prices)
        if len(price_data) > 500:
            result = await session.call('my.func', stock, price_data)
            column = result['column']
            trend = result['trend']
            if column == 'UP' and trend == 'UP':
                reports_database.updatePnf(current_date, stock, column, trend)
                print("Updated " + stock)

@component.on_join
async def joined(session: Session, details):
    current_date = datetime(2019, 11, 20)

    print("session ready")
    stocks = prices_database.getAllStocks()
    for i in range(104):
        print(current_date.isoformat())
        await updateReport(session, current_date, stocks)
        current_date += relativedelta(weeks=1)
        
    
    print("DONE")
    

if __name__ == "__main__":
    run([component])