class Station:
  # station: str(ID), int capacity
  id:int = 0
  capacity:int = 0

  def __init__(self, id:int, capacity:int):
    self.id = id
    self.capacity = capacity
  
  def to_list(self):
    return [self.id, self.capacity]

  def to_str_input(self)->str:
    output = " ".join([self.get_id_str(),str(self.capacity)])
    return output


  def get_id_str(self)->str:
    out = "S" + str(self.id)
    return out

  def get_id(self):
    return self.id
  
  def set_id(self,id:int):
    self.name = id
    return True
  
  def get_capacity(self):
    return self.capacity
  
  def set_capacity(self,capacity:int):
    self.capacity = capacity
    return True
  

  def __repr__(self):
      output = " ".join([self.get_id_str(),str(self.get_capacity())])
      return output
    
