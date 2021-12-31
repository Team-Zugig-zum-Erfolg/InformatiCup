from abfahrt.classes.Station import Station

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
  
  def to_list(self):
    """ """
    return [self.id, self.start.id, self.end.id, self.length, self.capacity]

  def to_str_input(self):
    """this method is used for input, generate information of one line"""
    output = " ".join([self.get_id_str(), self.start.get_id_str(), self.end.get_id_str() ,str(self.length),str(self.capacity)])
    return output

  def get_id_str(self)->str:
    """


    :rtype: str

    """
    out = "L" + str(self.id)
    return out
    
  def get_id(self):
    """ """
    return self.id
  
  def set_id(self,id_line:str):
    """

    :param id_line: 
    :type id_line: str

    """
    if type(id_line) != str:
      return False
    self.id = id_line
    return True
  
  def get_capacity(self):
    """ """
    return self.capacity
  
  def set_capacity(self,capacity:int):
    """

    :param capacity: 
    :type capacity: int

    """
    if type(capacity) != int:
      return False
    self.capacity = capacity
    return True
  
  def get_start(self):
    """ """
    return self.start
  
  def set_start(self,start:Station):
    """

    :param start: 
    :type start: Station

    """
    if (isinstance(start,Station)==False):
      return False
    self.start = start
    return True

  def get_end(self):
    """ """
    return self.end
  
  def set_end(self,end:Station):
    """

    :param end: 
    :type end: Station

    """
    if (isinstance(end,Station)==False):
      return False
    self.end = end
    return True
  
  def get_length(self):
    """ """
    return self.length
  
  def set_length(self,length:float):
    """

    :param length: 
    :type length: float

    """
    if type(length) != float:
      return False
    self.length = length
    return True

  def __repr__(self):
    # output = " ".join([self.get_id(),str(self.get_end()[0]),str(self.get_end()[1]),str(self.get_length()),str(self.get_capacity())])
    out = self.to_str_input()
    return out

  def __eq__(self, other):
    if (isinstance(other, Station)):
      return self.id == other.id and self.capacity == other.capacity and self.length == other.length and self.start == other.start and self.end == other.end
    return False


