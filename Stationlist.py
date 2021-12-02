from classes import Station
from classes.TrainInStation import TrainInStation
import sys

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
                    self.add_new_train_in_station(train_in_station, None)
                else:
                    train_in_station.passenger_out_train_time = earliest_leave_time
                    train_in_station.passenger_in_train_time = earliest_leave_time + 1
                    self.add_new_train_in_station(train_in_station, train.start_station.id)
            else:
                TRAIN_NOT_IN_STATION.append(train_in_station)
                TRAIN_NOT_IN_STATION.sort(key=lambda x: x.train.capacity, reverse=False)

    def compare_free_place(self, train_in_station: TrainInStation):
        # train, in_station_time, station_number
        earliest_leave_time = -1
        station_capacities = self.stations[train_in_station.station_id]
        for capacity in station_capacities:
            not_free = 0
            for _train_in_station in capacity:
                print(train_in_station.passenger_out_train_time)
                if _train_in_station.leave_time == None and train_in_station.passenger_out_train_time >= _train_in_station.passenger_out_train_time+1:
                    earliest_leave_time = -1
                    not_free = 1
                    break
                if Stationlist._train_in_station_is_full(_train_in_station, train_in_station.passenger_out_train_time):
                    if _train_in_station.leave_time is not None:
                        leave_time = _train_in_station.leave_time
                    else:
                        leave_time = _train_in_station.passenger_in_train_time
                    if earliest_leave_time == -1:
                        earliest_leave_time = leave_time
                    elif earliest_leave_time > leave_time:
                        earliest_leave_time = leave_time
                    not_free = 1
                    break
            if not_free == 0:
                return [True, -1]

        return [False, earliest_leave_time]

        time_change = None
        ends = []
        for capacity in station_capacities:
            for train_pos in range(len(capacity) - 1):
                time_change = earliest_leave_time
                if train_pos.leave_time is not None:
                    leave_time = train_pos.leave_time
                else:
                    leave_time = train_pos.passenger_in_train_time
                if leave_time < train_in_station.passenger_out_train_time:
                    earliest_leave_time = Stationlist._train_in_station_pos(capacity[train_pos], capacity[train_pos + 1]
                                                                            , earliest_leave_time)
                if time_change != earliest_leave_time:
                    time_change = None
                    break
                elif train_pos == len(capacity) - 2:
                    ends.append(capacity[train_pos + 1][1] + 1)
            if time_change != earliest_leave_time:
                break
        if time_change is not None:
            cpa_end = ends[0]
            for end in ends:
                if cpa_end > end:
                    cpa_end = end
            earliest_leave_time = cpa_end
        return [False, earliest_leave_time]

    @staticmethod
    def _train_in_station_is_full(train_in_station, in_station_time):
        # train_in_station[] = [out, in, train_Id, leave]
        if train_in_station.leave_time is not None:
            return train_in_station.passenger_out_train_time <= in_station_time <= train_in_station.leave_time
        else:
            return train_in_station.passenger_out_train_time <= in_station_time <= train_in_station.passenger_in_train_time

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

    def add_new_train_in_station(self, train_in_station: TrainInStation, result):
        global TRAIN_NOT_IN_STATION
        if result is not None:
            for _train_in_station in TRAIN_NOT_IN_STATION:
                if _train_in_station.train == train_in_station.train:
                    result.save_train_start(train_in_station.train.id, 0, train_in_station.station_id)
          
            for i in range(len(TRAIN_NOT_IN_STATION)):
                if train_in_station.train.id == TRAIN_NOT_IN_STATION[i].train.id:
                    TRAIN_NOT_IN_STATION.pop(i)
                    break
        

        capacity_number = 0
        for capacity in self.stations[train_in_station.station_id]:
            free = 1
            for _train_in_station in capacity:
                if Stationlist._train_in_station_is_full(_train_in_station, train_in_station.passenger_out_train_time) or (_train_in_station.leave_time == None and _train_in_station.passenger_out_train_time+1 < train_in_station.passenger_out_train_time):
                    free = 0
                    break
            if free == 1:
                self.stations[train_in_station.station_id][capacity_number].append(train_in_station)
                self.stations[train_in_station.station_id][capacity_number].sort(
                    key=lambda x: x.passenger_out_train_time)
                return True
            capacity_number = capacity_number + 1
        return False

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
        print("idhhw"+str(station_number))            
        self.add_new_train_in_station(TrainInStation(0,leave_time,train,leave_time,station_number),result)
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
            train_not_in_station.passenger_out_train_time = train_not_in_station_start_time
            train_not_in_station.passenger_in_train_time = train_not_in_station_start_time + 1
            trains.append(train_not_in_station.train)
            start_times.append(train_not_in_station.passenger_out_train_time)
        return start_times, trains, Station(station_number,len(self.stations[station_number]))





                            
