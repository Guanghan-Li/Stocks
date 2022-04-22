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
    pass

prices = Collection()
prices.add_task(start_app, 'get')

ns = Collection()
ns.add_collection(prices, 'prices')