class Passenger:
  def __init__(self, id_passenger, start_station, target_station, group_size, target_round):
    self.id = id_passenger
    self.start_station = start_station
    self.target_station = target_station
    self.group_size = group_size
    self.target_round = target_round
  def getId(self):
    return passenger.id
  def setId(passenger,id_passenger):
    if type(id_passenger) != str:
      return False
    self.id = id_passenger
    return True
  def getStartStation(self):
    return self.capacity
  def setStartStation(self,start_station):
    if type(start_station) != str:
      return False
    self.start_station = start_station
    return True
  def getTargetStation(self):
    return self.end
  def setTargetStation(self,end):
    if type(end) != list or len(end) != 2:
      return False
    self.end = end
    return True    
  def getGroupSize(self):
    return self.group_size
  def setGroupSize(self,size):
    if type(size) != int and not isnumeric(size):
      return False
    self.group_size = size
    return True
  def setTargetRound(self,target_round):
    if type(target_round) != int and not isnumeric(target_round):
      return False
    self.target_round = target_round
    return True
  def getTargetRound(self):
    return self.target_round
  
