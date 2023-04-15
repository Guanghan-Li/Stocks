from src.stock.values.task import Task


class Tasks:
    def __init__(self, tasks: list[Task]):
        self.tasks: list[Task] = tasks

    def getById(self, task_id):
        for task in self.tasks:
            if task.task_id == task_id:
                return task

        return None

    def getByAsset(self, asset):
        for task in self.tasks:
            if task.data == asset:
                return task

        return None

    def percentDone(self):
        amount_done = 0
        for task in self.tasks:
            if task.done:
                amount_done += 1

        return round(amount_done / len(self.tasks) * 100, 2)

    def join(self, other_tasks: "Tasks") -> "Tasks":
        return Tasks(self.tasks + other_tasks.tasks)
