class Passenger:
  def __init__(self, id_passenger, start_station, end_station, group_size, target_round):
    self.id_passenger = id_passenger
    self.start_station = start_station
    self.end_station = end_station
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
   
  def __repr__(self): 
#    return str(self.id_passenger, self.start_station, self.end_station, self.group_size, target_round)
    return( '' + self.id_passenger + ',' + self.start_station + ',' + self.end_station + ',' + str(self.group_size) + ',' + str(self.target_round) + '')
    






#passengers = ['P1 S2 S3 3 3','P2 S2 S1 10 5','P2 S2 S1 10 9','P2 S2 S1 8 9']
#pasag = []
#print(passengers)


#for i in range(len(passengers)):
 #   pasag = passengers[i].split(" ")
 #   print(pasag)
  #  pasag[-1]
    
    
    
    
    
def partition(array, start, end, compare_func):
    pivot = array[start]
    low = start + 1
    high = end

    while True:
        while low <= high and compare_func(array[high], pivot):
            high = high - 1

        while low <= high and not compare_func(array[low], pivot):
            low = low + 1

        if low <= high:
            array[low], array[high] = array[high], array[low]
        else:
            break

    array[start], array[high] = array[high], array[start]

    return high
    
    
    
    
def quick_sort(array, start, end, compare_func):
    if start >= end:
        return

    p = partition(array, start, end, compare_func)
    quick_sort(array, start, p-1, compare_func)
    quick_sort(array, p+1, end, compare_func)
    


passenger = [Passenger("P1", "S2", "S3", 3, 3), 
       Passenger("P2", "S2", "S1", 10, 9), 
       Passenger("P2", "S2", "S1", 10, 5), 
       Passenger("P2", "S2", "S1", 10, 7), 
       Passenger("P2", "S2", "S1", 10, 2)] 


quick_sort(passenger, 0, len(passenger) - 1, lambda x, y: x.target_round > y.target_round)


#print(sorted(passenger, key=lambda x: x.target_round)) 


for Passenger in passenger:
    print(Passenger) 
    