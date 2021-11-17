class Line:
  
 def __init__(line, id_line, end, capacity, length):
    line.id = id_line
    line.end = end
    line.capacity = capacity
    line.length = length
 
 def getId(line):
    return line.id
 
 def setId(line,id_line):
    if type(id_line) != int and not isnumeric(id_line):
        return False
    line.id = id_line
 
 def getCapacity(line):
    return line.capacity
 
 def setCapacity(line,capacity):
    if type(capacity) != int and not isnumeric(capacity):
        return False
    line.capacity = capacity
    return True
 
 def getEnd(line):
    return line.end
 
 def setEnd(line,end):
    if type(end) != list or len(end) != 2:
        return False
    line.end = end
    return True    
 
 def getLength(line):
    return line.length
 
 def setLength(line,length):
    if type(length) != int and not isnumeric(length):
        return False
    line.length = length
    return True

 def __repr__(self): 
    return( '' + self.id_line + ',' + self.end + ',' + self.capacity + ',' + str(self.length) + '')
 
  
