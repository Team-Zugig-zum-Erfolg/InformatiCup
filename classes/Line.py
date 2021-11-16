class Line:
  def __init__(self, id_line, end, capacity, length):
    self.id = id_line
    self.end = end
    self.capacity = capacity
    self.length = length
    
  def get_id(self):
    return self.id
  
  def set_id(self,id_line):
    if type(id_line) != str:
      return False
    self.id = id_line
    return True
  
  def get_capacity(self):
    return self.capacity
  
  def set_capacity(self,capacity):
    if type(capacity) != int:
      return False
    self.capacity = capacity
    return True
  
  def get_end(self):
    return self.end
  
  def set_end(self,end):
    if type(end) != list or len(end) != 2:
      return False
    self.end = end
    return True
  
  def get_length(self):
    return self.length
  
  def set_length(self,length):
    if type(length) != float and type(length) != int:
      return False
    self.length = length
    return True

  def to_str(self):
      output = " ".join([self.get_id(),str(self.get_end()[0]),str(self.get_end()[1]),str(self.get_length()),str(self.get_capacity())])
      return output
    
  def __repr__(self):
      output = " ".join([self.get_id(),str(self.get_end()[0]),str(self.get_end()[1]),str(self.get_length()),str(self.get_capacity())])
      return output


