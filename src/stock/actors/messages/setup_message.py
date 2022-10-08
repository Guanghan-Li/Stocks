class SetupMessage:
  def __init__(self, info: dict, log=False):
    self.info: dict = info
    self.log = log