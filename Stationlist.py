from classes import Station
from classes.TrainInStation import TrainInStation
import sys

from Linelist import Linelist
from Input import Input
from Groups import Groups
from Result import Result

TRAIN_NOT_IN_STATION = []
T_ID = 0
T_START_STATION = 1
T_SPEED = 2
T_CAPACITY = 3

S_ID = 0
S_CAPACITY = 1


class Stationlist:
    stations = []  # the stations with capacities

    def __init__(self, stationlist, trainlist):
        global TRAIN_NOT_IN_STATION
        station_id = 1
        self.stations.append([])
        for station in stationlist:
            self.stations.append([])
            for i in range(0, station[S_CAPACITY]):
                self.stations[station_id].append([])
            station_id = station_id + 1
        for train in trainlist:
            train_in_station = TrainInStation(0, 1, train, None, train.start_station.id)
            if train.start_station.id != -1:
                available, earliest_leave_time = self.compare_free_place(train_in_station)
                if available:
                    self.add_new_train_in_station(train_in_station, None, 0, 0)
                else:
                    train_in_station.passenger_out_train_time = earliest_leave_time
                    train_in_station.passenger_in_train_time = earliest_leave_time + 1
                    self.add_new_train_in_station(train_in_station, train.start_station.id, 0, 0)
            else:
                TRAIN_NOT_IN_STATION.append(train_in_station)
                TRAIN_NOT_IN_STATION.sort(key=lambda x: x.train.capacity, reverse=False)
        print(TRAIN_NOT_IN_STATION)

    @staticmethod
    def _capacity_is_full(capacity, train_in_station: TrainInStation):

        for _train_in_station in capacity:
            if _train_in_station.leave_time == None and _train_in_station.passenger_out_train_time <= train_in_station.passenger_out_train_time + 1:
                return True
        return False
    
    def compare_free_place(self, train_in_station: TrainInStation):
        # train, in_station_time, station_number
        earliest_leave_time = -1
        station_capacities = self.stations[train_in_station.station_id]
        time_change = None
        ends = []
        for capacity in station_capacities:
            if len(capacity) == 0:
                return [True, -1]
            if Stationlist._capacity_is_full(capacity,train_in_station):
                continue
            last_train_in_station = len(capacity) - 1
            if capacity[0].passenger_out_train_time > train_in_station.passenger_in_train_time:
                print("erst")
                return [True, -1]
            for i in range(last_train_in_station):
                # print(train_in_station.passenger_out_train_time)
                time_change = earliest_leave_time
                leave_time = Stationlist.train_leave_time(capacity[i])
                if Stationlist._train_in_station_is_free(leave_time, capacity[i + 1],
                                                         train_in_station.passenger_out_train_time):
                    return [True, -1]
                elif train_in_station.passenger_out_train_time <= leave_time:
                    earliest_leave_time = Stationlist._train_in_station_pos(capacity[i], capacity[i + 1],
                                                                            earliest_leave_time)
                    if time_change != earliest_leave_time:
                        time_change = None
                        print("rime none")
                    break

            leave_time = Stationlist.train_leave_time(capacity[last_train_in_station])
            ends.append(leave_time + 1)
            print("ends append")
            if leave_time < train_in_station.passenger_out_train_time:
                return [True, -1]
        if time_change is not None:
            print(ends)
            print("ends")
            cpa_end = ends[0]
            for end in ends:
                if cpa_end > end:
                    cpa_end = end
            earliest_leave_time = cpa_end
            print(earliest_leave_time)
        print("compare delay time" + str(earliest_leave_time))
        return [False, earliest_leave_time]

    @staticmethod
    def _train_in_station_is_free(front_train_leave_time, back_train_in_station: TrainInStation,
                                  in_station_time):
        # train_in_station[] = [out, in, train_Id, leave]
        return front_train_leave_time < in_station_time and \
               back_train_in_station.passenger_out_train_time > (in_station_time + 1)

    @staticmethod
    def _train_in_station_pos(front_train_in_station: TrainInStation, back_train_in_station: TrainInStation,
                              earliest_leave_time):
        distance_s_e = 1
        if front_train_in_station.leave_time is not None:
            leave_time = front_train_in_station.leave_time
        else:
            leave_time = front_train_in_station.passenger_in_train_time

        distance_between_trains = back_train_in_station.passenger_out_train_time - leave_time
        if distance_s_e + 2 <= distance_between_trains:
            earliest_leave_time = leave_time + 1
        return earliest_leave_time

    def add_new_train_in_station(self, train_in_station: TrainInStation, result, start_time, start_station, ignore_full_station=False):
        global TRAIN_NOT_IN_STATION
        enable, delay_time = self.compare_free_place(train_in_station)
        print("compare add " + str(enable))
        if not enable:
            if delay_time != -1:
                return enable
            elif ignore_full_station == False:
                return enable
        if result is not None:
            i = 0
            for _train_in_station in TRAIN_NOT_IN_STATION:
                if _train_in_station.train.id == train_in_station.train.id:
                    result.save_train_start(train_in_station.train.id, start_time,
                                            start_station.id)
                    TRAIN_NOT_IN_STATION.pop(i)
                    self.add_train_leave_time(train_in_station.train, start_time + 1, train_in_station.station_id,
                                              result)
                    break
                i += 1
        capacity_pos = 0
        finish = 0
        for capacity in self.stations[train_in_station.station_id]:
            if Stationlist._capacity_is_full(capacity,train_in_station) and ignore_full_station == True:
                capacity.append(train_in_station)
                capacity.sort(key=lambda x: x.passenger_out_train_time)
                return True
            if len(capacity) == 0 or capacity[0].passenger_out_train_time > train_in_station.passenger_in_train_time:
                capacity.append(train_in_station)
                capacity.sort(key=lambda x: x.passenger_out_train_time)
                return True
            last_train_in_station = len(capacity) - 1
            for i in range(last_train_in_station):
                leave_time = Stationlist.train_leave_time(capacity[i])
                if Stationlist._train_in_station_is_free(leave_time, capacity[i + 1],
                                                              train_in_station.passenger_out_train_time):
                    finish = 1
                    break
            leave_time = Stationlist.train_leave_time(capacity[last_train_in_station])
            if leave_time < train_in_station.passenger_out_train_time:
                finish = 1
            if finish == 1:
                break
            capacity_pos += 1
        if enable:
            self.stations[train_in_station.station_id][capacity_pos].append(train_in_station)
            self.stations[train_in_station.station_id][capacity_pos].sort(key=lambda x: x.passenger_out_train_time)
            return True

    def add_train_leave_time(self, train, leave_time, station_number, result):

        capacity_number = 0
        found = 0
        for capacity in self.stations[station_number]:
            t = 0
            for train_in_station in capacity:
                if train_in_station.train == train and train_in_station.leave_time is None:
                    train_in_station.leave_time = leave_time
                    return True
                t = t + 1
            capacity_number = capacity_number + 1

        self.add_new_train_in_station(TrainInStation(0, leave_time, train, leave_time, station_number), result, 0, 0)
        return True

    def read_trains_from_station(self, station_number):
        trains = []
        start_times = []
        train_not_in_station_start_time = sys.maxsize
        global TRAIN_NOT_IN_STATION
        for capacity in self.stations[station_number]:
            if len(capacity) > 0:
                for i in range(len(capacity)):
                    train_in_station = capacity[i]
                    if train_in_station.leave_time is None:
                        trains.append(train_in_station.train)
                        start_times.append(train_in_station.passenger_out_train_time)
                    if i + 1 == len(capacity):
                        if train_not_in_station_start_time > train_in_station.passenger_in_train_time + 1:
                            train_not_in_station_start_time = train_in_station.passenger_in_train_time + 1
            else:
                train_not_in_station_start_time = 0
        for train_not_in_station in TRAIN_NOT_IN_STATION:
            #check if the station is at least to the time train_not_in_station_start_time for one train free
            #only then return the train
            train_not_in_station.passenger_out_train_time = train_not_in_station_start_time
            train_not_in_station.passenger_in_train_time = train_not_in_station_start_time + 1
            trains.append(train_not_in_station.train)
            start_times.append(train_not_in_station.passenger_out_train_time)
        return start_times, trains, Station(station_number, len(self.stations[station_number]))

    @staticmethod
    def train_leave_time(train_in_station: TrainInStation):
        if train_in_station.leave_time is None:
            return train_in_station.passenger_in_train_time
        else:
            return train_in_station.leave_time

    def print_out(self):
        i = 0
        for capacity in self.stations:
            print("station " + str(i))
            print(capacity)
            i += 1
        if TRAIN_NOT_IN_STATION != None:
            print(TRAIN_NOT_IN_STATION)

'''
input_ = Input()
stations, lines, trains, passengers = input_.from_file("test/test-input-1.txt")

station_input_list = []
for s in stations:
    station_input_list.append(s.to_list())
line_input_list = []
for li in lines:
    line_input_list.append(li.to_list())
train_input_list = trains
result = Result()

# for t in trains:
# train_input_list.append(t.to_list())

linelist = Linelist(line_input_list)
stationlist = Stationlist(station_input_list, train_input_list)
stationlist.print_out()
print(train_input_list)
print(stationlist.stations)
enable = stationlist.add_new_train_in_station(TrainInStation(2, 3, trains[1], 5, 2), result, 0, 0)
enable = stationlist.add_new_train_in_station(TrainInStation(2, 3, trains[6], None, 2), result, 0, 0)
#enable, delay = stationlist.compare_free_place(TrainInStation(3, 4, trains[1], None, 1))
enable = stationlist.add_new_train_in_station(TrainInStation(3, 4, trains[3], 6, 2), result, 0, 0)
enable = stationlist.add_new_train_in_station(TrainInStation(4, 5, trains[3], None, 2), result, 0, 0)
#enable, delay = stationlist.compare_free_place(TrainInStation(7, 8, trains[5], None, 2))
enable = stationlist.add_new_train_in_station(TrainInStation(6, 7, trains[3], None, 2), result, 0, 0)
enable = stationlist.add_new_train_in_station(TrainInStation(6, 7, trains[3], None, 2), result, 0, 0)
#enable = stationlist.add_new_train_in_station(TrainInStation(delay, delay + 1, trains[3], None, 1), result, 0, 0)
enable, delay = stationlist.compare_free_place(TrainInStation(3, 4, trains[5], None, 2))
enable = stationlist.add_new_train_in_station(TrainInStation(delay, delay + 1, trains[3], None, 1), result, 0, 0)

enable, delay = stationlist.compare_free_place(TrainInStation(0, 1, trains[4], None, 2))


enable = stationlist.add_new_train_in_station(TrainInStation(0, 1, trains[3], None, 2), result, 0, 0)
print(enable)
enable, delay = stationlist.compare_free_place(TrainInStation(1, 2, trains[5], None, 2))
print(enable)
print(delay)
enable = stationlist.add_new_train_in_station(TrainInStation(delay, delay + 1, trains[8], None, 2), result, 0, 0)
stationlist.print_out()'''
