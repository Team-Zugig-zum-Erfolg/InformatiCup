class Passenger:
  def __init__(self, id_passenger, start_station, end_station, group_size, target_round):
    self.id = id_passenger
    self.start_station = start_station
    self.end_station = target_station
    self.group_size = group_size
    self.target_round = target_round
    
  def get_id(self):
    return passenger.id
  
  def set_id(passenger,id_passenger):
    if type(id_passenger) != str:
      return False
    self.id = id_passenger
    return True
    
  def get_start_station(self):
    return self.start_station
  
  def set_start_station(self,start_station):
    if type(start_station) != str:
      return False
    self.start_station = start_station
    return True
  
  def get_end_station(self):
    return self.end_station
  
  def set_end_station(self,end):
    if type(end) != list or len(end) != 2:
      return False
    self.end_station = end
    return True
  
  def get_group_size(self):
    return self.group_size
  
  def set_group_size(self,size):
    if type(size) != int and not isnumeric(size):
      return False
    self.group_size = size
    return True
  
  def set_target_round(self,target_round):
    if type(target_round) != int and not isnumeric(target_round):
      return False
    self.target_round = target_round
    return True
  
  def get_target_round(self):
    return self.target_round
  
  
