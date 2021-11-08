class Station:
  def __init__(self, name, capacity):
    self.name = name
    self.capacity = capacity
  def getName(self):
    return self.name
  def setName(self,name):
    if type(name) != str:
      return False
    self.name = name
    return True
  def getCapacity(self):
    return self.capacity
  def setCapacity(self,capacity):
    if type(capacity) != int or not isnumeric(capacity):
      return False
    self.capacity = capacity
    return True
