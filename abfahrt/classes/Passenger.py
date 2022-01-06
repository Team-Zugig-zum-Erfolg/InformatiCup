from typing import List
# This module provides runtime support for type hints. The most fundamental support consists of the types Any, Union, Callable, TypeVar, and Generic. For a full specification, please see PEP 484. For a simplified introduction to type hints, see PEP 483. (https://docs.python.org/3/library/typing.html)

from abfahrt.classes.Station import Station

class Passenger:
  # Passagiere: str(ID) str(Startbahnhof) str(Zielbahnhof) int(Gruppengröße) int(Ankunftszeit)

  id:int = 0
  start_station:Station = None
  end_station:Station = None
  group_size:int = 0
  target_time:int = 0

  action_board_time: int = 0
  action_arrive_time: int = 0
  action_train: str = ""

  history:List[str] = []

  def __init__(self, id:int, start_station:Station, end_station:Station, group_size:int, target_time:int):
    self.id = id
    self.start_station = start_station
    self.end_station = end_station
    self.group_size = group_size
    self.target_time = target_time
    self.history = []

  def to_list(self):
    return [self.id, self.start_station.id, self.end_station.id, self.group_size, self.target_time]

  def to_str_input(self)->str:
    output = " ".join([self.get_id_str(), self.start_station.get_id_str(), self.end_station.get_id_str(), str(self.group_size), str(self.target_time)])
    return output

  def to_str_output(self)->str:
    # return "[Passenger:P" + str(self.ID) + "]\n" + str(self.board_time) + " Board " + self.train + "\n" + str(self.arrive_time)+ " Detrain\n"
    output = "\n".join(self.history)
    return output
  
  def add_board(self, time:int, train_id:int):
    out = str(time) + " " + "Board" + " T" + str(train_id)
    # print(f"passenger [{self.id}] add board",out)
    self.history.append(out)

  def add_detrain(self, time:int):
    out = str(time) + " " + "Detrain"
    # print(f"passenger [{self.id}] add detrain",out)
    self.history.append(out)

  def merge(self, passenger):
    self.history += passenger.history

  def get_id_str(self)->str:
    ''' get id with P in a string '''
    out = "P" + str(self.id)
    return out
    
  def get_id(self):
    return self.id
  
  def set_id(self,id_passenger:int):
    if type(id_passenger) != int:
      return False
    self.id = id_passenger
    return True
    
  def get_start_station(self):
    return self.start_station
  
  def set_start_station(self,start_station:Station):
    if (isinstance(start_station, Station) == False):
      return False
    self.start_station = start_station
    return True
  
  def get_end_station(self):
    return self.end_station
  
  def set_end_station(self,end_station:Station):
    if (isinstance(end_station, Station) == False):
      return False
    self.end_station = end_station
    return True
  
  def get_group_size(self):
    return self.group_size
  
  def set_group_size(self,size):
    if type(size) != int:
      return False
    self.group_size = size
    return True
  
  def set_target_round(self, target_round):
    if type(target_round) != int:
      return False
    self.target_time = target_round
    return True

  def get_target_round(self):
    return self.target_time
  
  def __repr__(self):
    output = " ".join([self.get_id_str(),self.get_start_station().get_id_str(),self.get_end_station().get_id_str(),str(self.get_group_size()),str(self.get_target_round())])
    return output
  
  def __eq__(self, other):
    if (isinstance(other, Station)):
      return self.id == other.id and self.group_size == other.group_size and self.start_station == other.start_station and self.end_station == other.end_station and self.target_time == other.target_time
    return False
  
  
