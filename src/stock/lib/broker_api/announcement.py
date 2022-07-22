from pyparsing import anyOpenTag


class Announcement:
  def __init__(self, id, corporate_action_id, ca_type, ca_sub_type, initiating_symbol='', initiating_original_cusip='', target_symbol='', target_original_cusip='', ex_date='', record_date='', payable_date='', cash='', old_rate='', new_rate=''):
    self.id = id
    self.corporate_action_id = corporate_action_id
    self.ca_type = ca_type
    self.ca_sub_type = ca_sub_type
    self.initiating_symbol = initiating_symbol
    self.initiating_original_cusip = initiating_original_cusip
    self.target_symbol = target_symbol
    self.target_original_cusip = target_original_cusip
    self.ex_date = ex_date
    self.record_date = record_date
    self.payable_date = payable_date
    self.cash = cash
    self.old_rate = old_rate
    self.new_rate = new_rate

  def __str__(self):
    return f"Announcement ->  ca_type: {self.ca_type} | ca_sub_type: {self.ca_sub_type} | old_rate: {self.old_rate} | new_rate: {self.new_rate} | initiating_symbol: {self.initiating_symbol} | target_symbol: {self.target_symbol} | ex_date: {self.ex_date} | record_date: {self.record_date}"

  @staticmethod
  def fromJson(data):
    return Announcement(**data)