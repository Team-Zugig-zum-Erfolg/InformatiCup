from classes.TrainInLine import TrainInLine


class Linelist:
    lines = []  # the lines with capacities
    START = 0
    END = 1
    TRAIN = 2

    def initial(self, linelist):

        line_number = 1
        self.lines.append([])
        for line in linelist:
            self.lines.append([])
            for i in range(0, line[4]):
                self.lines[line_number].append([])
            line_number = line_number + 1
        return True

    def compare_free(self, train_in_line: TrainInLine):

        earliest_leave_time = -1
        line_capacities = self.lines[train_in_line.line_id]
        for capacity in line_capacities:
            not_free = 0
            for train_in_line in capacity:
                if Linelist._train_in_line_is_full(train_in_line, train_in_line.start, train_in_line.end):
                    not_free = 1
                    if earliest_leave_time == -1:
                        earliest_leave_time = train_in_line.end
                    elif earliest_leave_time > train_in_line.end:
                        earliest_leave_time = train_in_line.end
            if not_free == 0:
                return [True, -1]

        time_change = None
        ends = []

        for capacity in line_capacities:
            for train_pos in range(len(capacity) - 1):
                time_change = earliest_leave_time
                earliest_leave_time = Linelist._train_in_line_pos(capacity[train_pos], capacity[train_pos + 1],
                                                                  train_in_line.start, train_in_line.end,
                                                                  earliest_leave_time)
                if time_change != earliest_leave_time:
                    time_change = None
                    break
                elif train_pos == len(capacity) - 2:
                    ends.append(capacity[train_pos + 1][1] + 1)
            if time_change != earliest_leave_time:
                break
        if time_change != None:
            cpa_end = ends[0]
            for end in ends:
                if cpa_end > end:
                    cpa_end = end
            earliest_leave_time = cpa_end

        return [False, earliest_leave_time]

    @staticmethod
    def _train_in_line_is_full(train_in_line, start, end):
        return ((train_in_line.end >= start >= train_in_line.start) or
                (train_in_line.start <= end <= train_in_line.end))

    @staticmethod
    def _train_in_line_pos(front_train_in_line: TrainInLine, back_train_in_line: TrainInLine, start, end,
                           earliest_leave_time):
        distance_s_e = end - start
        distance_between_trains = back_train_in_line.start - front_train_in_line.end
        if distance_s_e + 2 <= distance_between_trains:
            earliest_leave_time = front_train_in_line.end + 1
        return earliest_leave_time

    def add_new_train_in_line(self, train_in_line: TrainInLine):

        capacity_number = 0
        for capacity in self.lines[train_in_line.line_id]:
            free = 1
            for train_in_line_add in capacity:
                if self._train_in_line_is_full(train_in_line_add, train_in_line.start, train_in_line.end):
                    free = 0
                    break
            if free == 1:
                self.lines[train_in_line.line_id][capacity_number].append(
                    [train_in_line.start, train_in_line.end, train_in_line.train])
                self.lines[train_in_line.line_id][capacity_number].sort(key=lambda x: x[0])
                print(self.lines[train_in_line.line_id][capacity_number])
                return True
            capacity_number = capacity_number + 1
        return False

    def read_trains_from_line(self, line_number):
        trains = []
        for capacity in self.lines[line_number]:
            for train_in_line in capacity:
                if train_in_line[self.TRAIN] not in trains:
                    trains.append(train_in_line[self.TRAIN])
        return trains




'''linelist.initial([[1, 3, 4, 12.2, 1], [2, 1, 2, 4.2, 2], [3, 3, 2, 4.2, 2], [4, 4, 2, 4.2, 2]])

linelist.add_new_train_in_line(1 , 7, 9, 1)
linelist.add_new_train_in_line(2 , 1, 2, 1)

linelist.add_new_train_in_line(1 , 7, 9, 2)
linelist.add_new_train_in_line(2 , 1, 2, 2)
linelist.add_new_train_in_line(2 , 1, 2, 2)
linelist.add_new_train_in_line(2 , 8, 9, 2)

print(linelist.add_new_train_in_line(2, 10, 12, 1))

print(linelist.compare_free(1, 2, 6, 2)) # Falsch delay_time
print(linelist.compare_free(1, 4, 6, 1))
print(linelist.compare_free(1, 2, 6, 1))
print(linelist.compare_free(1, 3, 6, 2))
linelist.add_new_train_in_line(1 , 2, 6, 1)
#linelist.add_new_train_in_line(1 , 13, 15, 1)
print(linelist.read_trains_from_line(1))
print(linelist.lines[1])
print(linelist.lines[2])'''
