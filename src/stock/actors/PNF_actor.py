import thespian
from thespian.actors import *
from sty import fg

class PNFActor(ActorTypeDispatcher):
  def __init__(self, name):
    super().__init__()
    self.name = name

  def receiveMsg_SetupMessage(self, message, sender):
    pass

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

        print("CALL START")
        result = await self.session.call('my.func', stock, price_data)
        print("CALL END")
        column = result['column']
        trend = result['trend']
        i_message = {"action": "pnf", "trend": trend, "column": column}
        self.i_queue.put(i_message)