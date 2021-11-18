from classes import Line

class Linelist:


    lines = []           #the lines with capacities
    
    
    def initial(self, linelist):
      
        line_number = 1
        self.lines.append([])
        for line in linelist:
            self.lines.append([])
            for i in range(0,line[4]):
                self.lines[line_number].append([])
            line_number = line_number + 1
        return True    
   
    def compare_free(self, train, start, end, line_number):

        earliest_leave_time = -1
        line_capacities = self.lines[line_number]
        for capacity in line_capacities:
            not_free = 0
            for train_in_line in capacity:  
                if self._train_in_line_is_full(train_in_line,start,end):
                    not_free = 1
                    if earliest_leave_time == -1:
                        earliest_leave_time = train_in_line[1]
                    elif earliest_leave_time > train_in_line[1]:
                        earliest_leave_time = train_in_line[1]
            if not_free == 0:
                return [True,-1]
            
        return [False,earliest_leave_time]

    def _train_in_line_is_full(self,train_in_line,start,end):
        return ((train_in_line[1] >= start and train_in_line[0] <= start) or (train_in_line[0] <= end and train_in_line[1] >= end))

    
    def add_new_train_in_line(self, train, start, end, line_number):

        capacity_number = 0
        for capacity in self.lines[line_number]:
            free = 1
            for train_in_line in capacity:
                if self._train_in_line_is_full(train_in_line,start,end):
                    free = 0
                    break
            if free == 1:
                self.lines[line_number][capacity_number].append([start,end,train])
                self.lines[line_number][capacity_number].sort(key=lambda x: x[0])
                print(self.lines[line_number][capacity_number])
                return True
            capacity_number = capacity_number + 1
        return False

    def read_trains_from_line(self, line_number):
        trains = []
        for capacity in self.lines[line_number]:
            for train_in_line in capacity:
                if train_in_line[2] not in trains:
                    trains.append(train_in_line[2])
        return trains


linelist = Linelist()


linelist.initial([[1, 3, 4, 12.2, 1], [2, 1, 2, 4.2, 2], [3, 3, 2, 4.2, 2], [4, 4, 2, 4.2, 2]])

linelist.add_new_train_in_line(1 , 7, 9, 1)
linelist.add_new_train_in_line(2 , 1, 2, 1)

linelist.add_new_train_in_line(1 , 7, 9, 2)
linelist.add_new_train_in_line(2 , 1, 2, 2)
linelist.add_new_train_in_line(2 , 1, 4, 2)
linelist.add_new_train_in_line(2 , 5, 8, 2)

print(linelist.add_new_train_in_line(2, 10, 12, 1))

print(linelist.compare_free(1, 2, 6, 1)) # Falsch delay_time
print(linelist.compare_free(1, 4, 6, 1))
linelist.add_new_train_in_line(1 , 2, 6, 1)
print(linelist.read_trains_from_line(1))
print(linelist.lines[1])
print(linelist.lines[2])


