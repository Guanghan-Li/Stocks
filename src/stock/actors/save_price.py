import thespian
from thespian.actors import *
from sty import fg
from src.stock.repos.price_database import PricesDatabase, price_proxy
from src.stock.actors.messages import *
from src.stock.lib.log.log import Log
from src.stock.values.tasks import Tasks, Task
from datetime import datetime


class SavePriceActor(ActorTypeDispatcher):
    def __init__(self):
        super().__init__()
        self.running_task = False

    def receiveMsg_SetupMessage(self, message: SetupMessage, sender):
        self.name = message.info["name"]
        self.log = Log(message.log)
        self.log.info("SavePriceActor Got Setup message", self.name)
        self.prices_database = PricesDatabase(price_proxy, "Data/prices.db")
        self.task_manager = message.info.get("task_manager", None)
        self.send(sender, 0)

    def receiveMsg_SavePriceMessage(self, message: SavePriceMessage, sender):
        start = datetime.now()
        self.log.info(f"{fg.li_red}START savePrice{fg.rs} {self.name} {message.asset}")
        task = Task.create(self.name, message.asset)
        # self.send(self.task_manager, task.toCreateMessage())
        self.prices_database.setupPrices(message.data)

        end = datetime.now()
        time_spent = (end - start).microseconds * 0.001
        self.log.info(
            f"{fg.li_red}END savePrice{fg.rs} {self.name} {message.asset} | took {time_spent}"
        )
        # self.send(self.task_manager, task.toFinishedMessage())

    def receiveMsg_TaskFinishedMessage(self, message: TaskFinishedMessage, sender):
        self.send(sender, self.running_task)
