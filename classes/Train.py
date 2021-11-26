from typing import List
from classes.Station import Station
from classes.Line import Line

class Train:
  # Züge: str(ID) str(Startbahnhof)/* dec(Geschwindigkeit) int(Kapazität)

  id:int = 0
  start_station:Station = None
  speed:float = 0.0
  capacity:int = 0
  history:List[str] = []

  def __init__(self, id:int, start_station:Station, speed:float, capacity:int):
    '''if start_station is *, input value of start_station could be None '''
    self.id = id
    self.start_station = start_station
    self.speed = speed
    self.capacity = capacity

  def to_list(self):
    return [self.id, self.start_station.get_id(), self.speed, self.capacity]

  def to_str_input(self)->str:
    if self.start_station.id < 0:
      output = " ".join([self.get_id_str(), "*", str(self.speed), str(self.capacity)])
    else:
      output = " ".join([self.get_id_str(), self.start_station.get_id_str(), str(self.speed), str(self.capacity)])
    return output

  def to_str_output(self)->str:
    output = "\n".join(self.history)
    return output

  def get_id_str(self)->str:
    ''' get id with T in a string '''
    out = "T" + str(self.id)
    return out
  
  def add_start(self, time:int, station:Station):
    out = str(time) + " " + "Start" + " " + station.get_id_str()
    self.history.append(out)
  
  def add_depart(self, time:int, line:Line):
    out = str(time) + " " + "Depart" + " " + line.get_id_str()
    self.history.append(out)

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

  def __repr__(self):
      output = " ".join([self.get_id(),self.get_start_station(),str(self.get_capacity()),str(self.get_speed())])
      return output


