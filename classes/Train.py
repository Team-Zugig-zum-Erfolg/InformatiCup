class Train:
  def __init__(self, id_train, capacity, start_station, speed):
    self.id = id_train
    self.capacity = capacity
    self.start_station = start_station
    self.speed = speed
    
  def get_id(self):
    return self.id
  
  def set_id(self,id_train):
    if type(id_train) != str:
      return False
    self.id = id_train
    return True
  
  def set_start_station(self,start_station):
    if type(start_station) != str:
      return False
    self.start_station = start_station
    return True
  
  def get_start_station(self):
    return self.start_station
  
  def set_speed(self,speed):
    if type(speed) != float:
      return False
    self.speed = speed
    return True
  
  def get_speed(self):
    return self.speed
  
  def set_capacity(self,capacity):
    if type(capacity) != int:
      return False
    self.capacity = capacity
    return True
  
  def get_capacity(self):
    return self.capacity
  
  def to_str(self):
      output = " ".join([self.get_id(),self.get_start_station(),str(self.get_capacity()),str(self.get_speed())])
      return output


