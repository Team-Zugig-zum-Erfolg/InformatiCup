class Station:
  def __init__(self, name, capacity):
    self.name = name
    self.capacity = capacity
  def get_name(self):
    return self.name
  def set_name(self,name):
    if type(name) != str:
      return False
    self.name = name
    return True
  def get_capacity(self):
    return self.capacity
  def set_capacity(self,capacity):
    if type(capacity) != int and not isnumeric(capacity):
      return False
    self.capacity = capacity
    return True
  def to_str(self):
      output = " ".join([self.get_name(),str(self.get_capacity())])
      return output
