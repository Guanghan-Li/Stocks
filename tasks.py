from os import getenv, environ
from invoke import task, Collection
from dotenv import load_dotenv
from get_data import get_prices
import asyncio


import txaio, asyncio

txaio.use_asyncio()

load_dotenv()


@task(
    help={
        "test": "For running tests against the hub",
    }
)
def start_app(c, test=False):
    asyncio.run(get_prices.main())


prices = Collection()
prices.add_task(start_app, "get")

ns = Collection()
ns.add_collection(prices, "prices")
