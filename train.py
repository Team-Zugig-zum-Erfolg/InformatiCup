class Train:
  def __init__(train, id_train, capacity, start_station, depature_time, speed):
    train.id_train = id_train
    train.capacity = capacity
    train.start_station = start_station
    train.depature_time = depature_time
    train.speed = speed
  def getID(train):
    return train.id_train
