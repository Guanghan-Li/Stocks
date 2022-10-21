from asyncio import all_tasks
import thespian
from thespian.actors import *
from sty import fg
from src.stock.actors.messages import *
from src.stock.lib.log.log import Log
from src.stock.values.tasks import Tasks, Task

class TaskManagerActor(ActorTypeDispatcher):
  def __init__(self):
    super().__init__()
  
  def receiveMsg_SetupMessage(self, message: SetupMessage, sender):
    self.all_tasks: dict[str, Tasks] = {}
    self.log = Log(message.log)
    self.send(sender, 0)

  def receiveMsg_TaskCreate(self, message: TaskCreate, sender):
    return
    task: Task = message.task
    if not task.actor_name in self.all_tasks:
      self.all_tasks[task.actor_name] = Tasks([])
    
    actor_tasks: Tasks = self.all_tasks[task.actor_name]
    actor_tasks.tasks.append(task)

  def receiveMsg_TaskFinished(self, message: TaskFinishedMessage, sender):
    return
    actor_tasks: Tasks = self.all_tasks[message.actor_name]
    task = actor_tasks.getById(message.task_id)
    task.done = True
    task.started = False

  def receiveMsg_TaskSummary(self, message: TaskSummary, sender):
    all_tasks = Tasks([])
    breakdown_percents = {}
    for actor_name, tasks in self.all_tasks.items():
      all_tasks.join(tasks)
      if message.breakdown:
        breakdown_percents[actor_name] = tasks.percentDone()
    
    self.send(sender, {"percent": all_tasks.percentDone(), "breakdown": breakdown_percents})
    
