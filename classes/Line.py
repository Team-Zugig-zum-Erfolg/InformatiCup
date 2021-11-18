from classes.Station import Station

class Line:
  # Strecken: str(ID) str(Anfang) str(Ende) dec(Länge) int(Kapazität)
  # L1 S1 S2 1 3
  id:int = 0
  start:Station = None
  end:Station = None
  capacity:float = 0.0
  length:int = 0

  def __init__(self, id:int,start:Station, end:Station, length:float, capacity:int):
    ''' a constructor with start'''
    self.id = id # int
    self.start = start
    self.end = end
    self.capacity = capacity
    self.length = length
  
  def to_str_input(self):
    '''this method is used for input, generate information of one line'''
    output = " ".join([self.get_id_str(), self.start.get_id_str(), self.end.get_id_str() ,str(self.length),str(self.capacity)])
    return output

  def get_id_str(self)->str:
    ''' return the id of line with L, like "L1" '''
    out = "L" + str(self.id)
    return out
    

  def get_id(self):
    return self.id
  
  def set_id(self,id_line:str):
    self.id = id_line
    return True
  
  def get_capacity(self):
    return self.capacity
  
  def set_capacity(self,capacity:int):
    self.capacity = capacity
    return True
  
  def get_end(self):
    return self.end
  
  def set_end(self,end:Station):
    self.end = end
    return True
  
  def get_length(self):
    return self.length
  
  def set_length(self,length:float):
    self.length = length
    return True


  def __repr__(self):
      # output = " ".join([self.get_id(),str(self.get_end()[0]),str(self.get_end()[1]),str(self.get_length()),str(self.get_capacity())])
      out = self.to_str_input()
      return out


