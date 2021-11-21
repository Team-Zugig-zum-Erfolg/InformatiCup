from classes.Line import Line
from classes.Station import Station

class Linelist:

    line_objects = []
    lines = []           #the lines with capacities
    
    
    def initial(self, linelist):
      
        line_number = 1
        self.lines.append([])
        self.line_objects.append([])
        for line in linelist:
            self.lines.append([])
            self.line_objects.append(Line(line[0],line[1],line[2],line[3],line[4]))
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

    def get_lines_from_station(self, station_number):
        lines_return = []
        for line_object in self.line_objects:
            if line_object.get_start_station().get_id() == station_number or line_object.get_end_station().get_id() == station_number:
                lines_return.append(line_object)
        return lines_return



