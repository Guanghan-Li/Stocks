import txaio, asyncio, pykka

txaio.use_asyncio()

from get_data import *
from broker import Broker

# personal
account_info1 = {
    "public_key": "PKG77R4EUWQ76WC12PI5",
    "private_key": "YvNim9ia5ov4oJ7WHLv6ElPYQMcMTZMMTP3pLjtp",
    "api_link": "https://paper-api.alpaca.markets",
}
# 08
account_info2 = {
    "public_key": "PKAJ6YB539JWBMJT81Q8",
    "private_key": "clxZoMjA1rc7RFA42aFcbnAwggp95buT1bwGCHxe",
    "api_link": "https://paper-api.alpaca.markets",
}
# 02
account_info3 = {
    "public_key": "PKZBZND7F6PH39SMHJPQ",
    "private_key": "2gENBEvKNSEss7zWkY8N290eIANnv32iUeuHPRFy",
    "api_link": "https://paper-api.alpaca.markets",
}
# 03
account_info4 = {
    "public_key": "PKQMDMXG2T2FMQ8AZOY5",
    "private_key": "YVdUWYT7hTVPxpkuwDFi07i3Ib8E1AceHPZha46a",
    "api_link": "https://paper-api.alpaca.markets",
}

account_info5 = {
    "public_key": "PKP33J9QMA0IK97MBED5",
    "private_key": "D2cP3slrGwPm3MeAdQdar2MawUNmYMwaK1Wq99lv",
    "api_link": "https://paper-api.alpaca.markets",
}


broker = Broker(account_info1)
broker2 = Broker(account_info2)
broker3 = Broker(account_info3)
broker4 = Broker(account_info4)
broker5 = Broker(account_info5)

count = 0

assets = broker.getAllAssets()
asset_amount = len(assets)
# assets2 = broker2.getAllAssets()
amount = list(zip(*[iter(assets)] * (len(assets) // 10)))

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

brokers = [broker, broker2, broker3, broker4, broker5]


def killed(sig, frame):
    pykka.ActorRegistry.stop_all(timeout=2.0)


# signal.signal(signal.SIGINT, killed)
# signal.signal(signal.SIGTERM, killed)
# signal.signal(signal.SIGABRT, killed)


async def foo(session):
    print("HELLO")


async def main():
    tasks = []

    for i in range(10):
        SavePriceActor.use_deamon_thread = True
        BrokerActor.use_deamon_thread = True
        GenerateReportActor.use_deamon_thread = True
        ReportSaveActor.use_deamon_thread = True
        save_price = SavePriceActor.start(f"Save Price {i}").proxy()

        save_report = ReportSaveActor.start(f"Save Report {i}").proxy()
        gen_report_actor = GenerateReportActor.start(
            f"GenReport {i}", save_report
        ).proxy()
        broker_actor = BrokerActor.start(
            f"Broker {i}", save_price, gen_report_actor
        ).proxy()
        tasks.append(broker_actor.getPrices(amount[i], brokers[i // 2]).get())

    await asyncio.wait(tasks)


# thread2 = threading.Thread(target=main)
# thread2.setDaemon(True)
# thread2.start()
asyncio.run(main())
# main()
# prices_database.setupPrices(broker.api, assets)
