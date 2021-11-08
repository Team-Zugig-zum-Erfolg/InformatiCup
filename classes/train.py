class Train:
  def __init__(train, id_train, capacity, start_station, depature_time, speed):
    train.id = id_train
    train.capacity = capacity
    train.start_station = start_station
    train.depature_time = depature_time
    train.speed = speed
  def getId(train):
    return train.id_train
  def setId(train,id_train):
    if type(id_train) != str:
      return False
    train.id_train = id_train
    return True
  def setStartStation(train,start_station):
    train.start_station = start_station
  def getStartStation(train):
    return train.start_station
      
  
