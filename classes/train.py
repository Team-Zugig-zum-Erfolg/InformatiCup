class Train:
 
 def __init__(self, id_train, capacity, start_station, speed):
    self.id = id_train
    self.capacity = capacity
    self.start_station = start_station
    self.speed = speed
 
 def getId(self):
    return self.id
 
 def setId(self,id_train):
    self.id = id_train
 
 def setStartStation(self,start_station):
    self.start_station = start_station
 
 def getStartStation(self):
    return self.start_station
 
 def setSpeed(self,speed):
    self.speed = speed
 
 def getSpeed(self):
    return self.speed
 
 def setCapacity(self,capacity):
    self.capacity = capacity
 
 def getCapacity(self):
    return self.capacity
 
 def to_str(self):
    output = " ".join([self.getId(),self.getStartStation(),str(self.getCapacity()),str(self.getSpeed())])
    return output

# def __repr__(self): 
#    return str(self.id_passenger, self.start_station, self.end_station, self.group_size, target_round)
#    return( '' + self.id_train + ',' + self.start_station + ',' + self.capacity + ',' + str(self.speed) + '')
 
