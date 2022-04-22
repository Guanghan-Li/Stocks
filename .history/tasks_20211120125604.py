from os import getenv, environ
from invoke import task, Collection
from dotenv import load_dotenv
from autobahn.asyncio.component import run
from asyncio.selector_events import *
from sty import fg
from repos.price_database import PricesDatabase


import txaio,asyncio
txaio.use_asyncio()

load_dotenv()

broker = Broker()
prices_database = PricesDatabase(price_proxy)

@task(help={
    'test': 'For running tests against the hub',
})
def start_app(c, test=False):
    message = f"Starting {fg.blue} Mock Device {fg.rs} Service"

    if test:
        environ['TESTING'] = 'True'
        message += ' (TESTING)'
    else:
        environ['TESTING'] = 'False'


    print(message)
    bootstrapService = BootstrapService()
    bootstrapService.start()

def getDecadeData(all_assets):
  for i in range(2017, 2021, 2):
    end_date = date(i+2, 11, 20).isoformat()
    start_date = date(i, 11, 19).isoformat()
    print("Getting prices for the date {} -> {}".format(start_date, end_date))
    prices_database.setupPrices(broker.api, all_assets, start_date=start_date, end_date=end_date)

def getPrices(c):
    print("Getting prices...")
    assets = broker.getAllAssets()
    prices_database.setupPrices(broker.api, assets)
    getDecadeData(assets)

prices = Collection()
prices.add_task(start_app, 'get')

ns = Collection()
ns.add_collection(app, 'prices')