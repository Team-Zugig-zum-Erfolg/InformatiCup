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
    if type(capacity) != int and not isnumeric(capacity):
        return False
    self.capacity = capacity
    return True
    
def __repr__(self): 
#    return str(self.id_passenger, self.start_station, self.end_station, self.group_size, target_round)
    return( '' + self.name + ',' + self.capacity + '')
 
