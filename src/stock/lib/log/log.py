class Log:
  def __init__(self, can_log=False):
    self.can_log = can_log

  def info(self, *args):
    if self.can_log == True:
      print(*args)