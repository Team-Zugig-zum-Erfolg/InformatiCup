class Passenger:
  def __init__(self, id_passenger, start_station, end_station, group_size, target_round):
    self.id = id_passenger
    self.start_station = start_station
    self.end_station = end_station
    self.group_size = group_size
    self.target_round = target_round
  def getId(self):
    return passenger.id
  def setId(passenger,id_passenger):
    if type(id_passenger) != int and not isnumeric(id_passenger):
      return False
    self.id = id_passenger
  def getStartStation(self):
    return self.start_station
  def setStartStation(self,start_station):
    if type(start_station) != str:
      return False
    self.start_station = start_station
    return True
  def getEndStation(self):
    return self.end_station
  def setEndStation(self,end):
    if type(end) != list or len(end) != 2:
      return False
    self.end_station = end
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
  
