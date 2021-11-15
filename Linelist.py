from classes import Line

class Linelist:

    line_objects = []    #the line objects of type class Station
    lines = []           #the lines with capacities
    
    
    def initial(self, linelist):
        
        self.line_objects = linelist
        for line in linelist:
            self.lines.append([])
        return True    
   
    def compare_free(self, train, in_line_time, line_number):

        trains_in_line = 0
        earliest_leave_time = -1
        line_capacities = self.lines[line_number]
        if len(line_capacities) < self.line_objects[line_number].get_capacity():
            return [True,-1]
        for train_in_line in line_capacities:
                if train_in_line[0] <= in_line_time and (train_in_line[1] >= in_line_time):
                    if earliest_leave_time > train_in_line[1] or earliest_leave_time == -1:
                        earliest_leave_time = train_in_line[1]
                    trains_in_line = trains_in_line + 1
                if trains_in_line == self.line_objects[line_number].get_capacity():
                    return [False,earliest_leave_time]
        return [True,-1]
    
    def add_new_train_in_line(self, train, start, end, line_number):

        self.lines[line_number].append([start,end,train])
        return True

    def read_trains_from_line(self, line_number):
        
        trains = []
        for train_in_line in self.lines[line_number]:
            if train_in_line[2] not in trains:
                trains.append(train_in_line[2])
        return trains


line1 = Line("L1",["S1","S2"],2,10)
line2 = Line("L2",["S1","S2"],2,10)

linelist = Linelist()


linelist.initial([line1,line2])

linelist.add_new_train_in_line("T1",1,12,0)
linelist.add_new_train_in_line("T2",1,12,0)
print(linelist.compare_free("T1",6,0))
print(linelist.read_trains_from_line(0))




