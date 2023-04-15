from thespian.actors import *
from src.stock.actors.broker_actor import BrokerActor
from src.stock.actors.save_price import SavePriceActor
from src.stock.actors.messages.setup_message import SetupMessage

asys = ActorSystem("multiprocQueueBase")
broker_actor = asys.createActor(BrokerActor)
save_price_actor = asys.createActor(SavePriceActor)
info = {"save_price_actor": save_price_actor, "gen_report_actor": 1, "name": "Hello"}

asys.tell(broker_actor, SetupMessage(info))
