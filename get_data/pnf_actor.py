from pykka import ThreadingActor
import asyncio, queue, threading, os
from autobahn.asyncio.component import Component, run

class PNFActor(ThreadingActor):
  def __init__(self, name):
    super().__init__()
    self.name = name

  async def onJoin(self, session, details):
    print("JOINED WAMP")
    self.session = session
    message = {"stop": False}

    while not message["stop"]:
      message: dict = self.o_queue.get()
      message.setdefault("stop", False)
      if message["action"] == "update":
        price_data = message["prices"]
        stock = message["stock"]

        result = await self.session.call('my.func', stock, price_data)
        column = result['column']
        trend = result['trend']
        i_message = {"action": "pnf", "trend": trend, "column": column}
        self.i_queue.put(i_message)

  def updateReport(self, stock, prices):
    self.o_queue.put({"action": "update", "stock": stock, "prices": prices}, block=True)
    result = self.i_queue.get()
    trend, column = result["trend"], result["column"]
    print(trend, column, stock)
    return (trend, column)

  def on_start(self):
    print("Starting", self.name)
    self.loop = asyncio.new_event_loop()
    asyncio.set_event_loop(self.loop)
    print("HELLO FROM HERE")
    self.o_queue = queue.Queue()
    self.i_queue = queue.Queue()
    thread = threading.Thread(target=self.runComp, daemon=True)
    thread.start()

  def runComp(self):
    print("Run comp")
    self.loop2 = asyncio.new_event_loop()
    asyncio.set_event_loop(self.loop2)
    url = os.environ.get('CBURL', u'ws://localhost:8080/ws')
    realmv = os.environ.get('CBREALM', u'realm1')
    self.component = Component(transports=url, realm=realmv)
    self.component.on("join", self.onJoin)
    #self.component.start(self.loop)
    print("This is here")
    #self.loop.run_forever()
    run([self.component])
  
  def foo(self):
    print("Foo")
    return 1

  def on_stop(self):
    self.component.stop()
    self.loop.stop()

  def on_failure(self, exception_type, exception_value: BaseException, traceback) -> None:
      print("THIS DIED")