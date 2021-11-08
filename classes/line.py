class Line:
  def __init__(line, id_line, end, capacity, length):
    line.id = id_line
    line.end = end
    line.capacity = capacity
    line.length = length
  def getId(line):
    return line.id
  def setId(line,id_line):
    if type(id_line) != str:
      return False
    line.id = id_line
  def getCapacity(line):
    return line.capacity
  def setCapacity(line,capacity):
    if type(capacity) != int and not isnumeric(capacity):
      return False
    line.capacity = capacity
    return True
  def getEnd(line,index=-1):
    if type(index) != int:
      return False
    if index == -1:
      return line.end
    elif index in [0,1]:
      return line.end[index]
    return False
  def setEnd(line,end,index=-1):
    if type(end) == list:
        if len(end)!=2 or index!=-1:
          return False
        line.end = end
        return True
    elif type(end) == str:
      if type(index) != int or index not in [0,1]:
        return False
      line.end[index] = end
      return True   
    return False   
  def getLength(line):
    return line.length
  def setLength(line,length):
    if type(length) != int and not isnumeric(length):
      return False
    line.length = length
    return True
  def to_str(line):
    output = ' '.join([line.getId(),line.getEnd(0),line.getEnd(1),str(line.getLength()),str(line.getCapacity())])
    print(output)

  
