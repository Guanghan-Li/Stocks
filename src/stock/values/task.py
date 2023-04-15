import uuid
from src.stock.actors.messages.task_create import TaskCreate
from src.stock.actors.messages.task_finished import TaskFinishedMessage


class Task:
    def __init__(self, task_id, actor_name, data):
        self.task_id = task_id
        self.actor_name = actor_name
        self.data = data

        self.done = False
        self.started = True

    @staticmethod
    def create(actor_name, data):
        task_id = str(uuid.uuid4())
        return Task(task_id, actor_name, data)

    def toCreateMessage(self) -> TaskCreate:
        return TaskCreate(self)

    def toFinishedMessage(self) -> TaskFinishedMessage:
        return TaskFinishedMessage(self.task_id, self.actor_name)
