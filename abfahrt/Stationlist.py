from abfahrt.classes.Station import Station
from abfahrt.classes.TrainInStation import TrainInStation
import sys

from abfahrt.Result import Result

TRAIN_NOT_IN_STATION = []
T_ID = 0
T_START_STATION = 1
T_SPEED = 2
T_CAPACITY = 3

S_ID = 0
S_CAPACITY = 1


class Stationlist:
    """ """
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
            train_in_station = TrainInStation(
                0, 1, train, None, train.start_station.id)
            if train.start_station.id != -1:
                available, earliest_leave_time = self.compare_free_place(
                    train_in_station)
                if available:
                    self.add_new_train_in_station(train_in_station, None)
                else:
                    raise ValueError(
                        "Error: Too many trains in station at beginning!")
            else:
                TRAIN_NOT_IN_STATION.append(train_in_station)
                TRAIN_NOT_IN_STATION.sort(
                    key=lambda x: x.train.capacity, reverse=False)

    @staticmethod
    def _capacity_is_full(capacity):
        """

        :param capacity: 

        """

        for _train_in_station in capacity:
            # and _train_in_station.arrive_train_time <= train_in_station.arrive_train_time + 1:
            if _train_in_station.leave_time == None:
                return True
        return False

    def compare_free_place(self, train_in_station: TrainInStation):
        """

        :param train_in_station: 
        :type train_in_station: TrainInStation

        """
        station_capacities = self.stations[train_in_station.station_id]
        capacity_minimal_times = []

        # if at least one capacity is free
        for capacity in station_capacities:
            if len(capacity) == 0:
                return [True, -1]

        if train_in_station.leave_time == None:
            for capacity in station_capacities:
                if Stationlist._capacity_is_full(capacity):
                    continue
                elif train_in_station.arrive_train_time <= capacity[len(capacity)-1].leave_time:
                    capacity_minimal_times.append(
                        capacity[len(capacity)-1].leave_time+1)
                else:
                    return [True, -1]

            if len(capacity_minimal_times) > 0:
                return [False, min(capacity_minimal_times)]
            else:
                return [False, -1]

        else:
            # first train of capacity arrives after the current train wants to leave again
            if train_in_station.leave_time < capacity[0].arrive_train_time:
                return [True, -1]

            for capacity in station_capacities:
                skip_capacity = 0
                for i in range(len(capacity)-1):
                    if capacity[i].leave_time == None:
                        skip_capacity = 1
                        break

                    if Stationlist._train_in_station_is_free(capacity[i].leave_time, capacity[i + 1], train_in_station.arrive_train_time, train_in_station.leave_time):
                        return [True, -1]

                    elif (capacity[i+1].arrive_train_time - capacity[i].leave_time)-1 > (train_in_station.leave_time-train_in_station.arrive_train_time) and capacity[i].leave_time >= train_in_station.arrive_train_time:
                        capacity_minimal_times.append(
                            capacity[i].leave_time + 1)
                        skip_capacity = 1
                        break

                if skip_capacity == 1:
                    continue

                if capacity[len(capacity)-1].leave_time != None:
                    if capacity[len(capacity)-1].leave_time < train_in_station.arrive_train_time:
                        return [True, -1]
                    else:
                        capacity_minimal_times.append(
                            capacity[len(capacity)-1].leave_time+1)

            if len(capacity_minimal_times) > 0:
                return [False, min(capacity_minimal_times)]
            else:
                return [False, -1]

    @staticmethod
    def _train_in_station_is_free(front_train_leave_time, back_train_in_station: TrainInStation,
                                  in_station_time, leave_station_time):
        """

        :param front_train_leave_time: 
        :param back_train_in_station: 
        :type back_train_in_station: TrainInStation
        :param in_station_time: 
        :param leave_station_time: 

        """
        # train_in_station[] = [out, in, train_Id, leave]
        if front_train_leave_time == None:
            return False

        return front_train_leave_time < in_station_time and back_train_in_station.arrive_train_time > leave_station_time

    @staticmethod
    def _train_in_station_pos(front_train_in_station: TrainInStation, back_train_in_station: TrainInStation,
                              earliest_leave_time):
        """

        :param front_train_in_station: 
        :type front_train_in_station: TrainInStation
        :param back_train_in_station: 
        :type back_train_in_station: TrainInStation
        :param earliest_leave_time: 

        """
        distance_s_e = 1
        if front_train_in_station.leave_time is not None:
            leave_time = front_train_in_station.leave_time
        else:
            leave_time = front_train_in_station.passenger_in_train_time

        distance_between_trains = back_train_in_station.arrive_train_time - leave_time
        if distance_s_e + 2 <= distance_between_trains:
            earliest_leave_time = leave_time + 1
        return earliest_leave_time

    @staticmethod
    def _train_in_capacity(capacity, train):
        """

        :param capacity: 
        :param train: 

        """
        if not train:
            return False
        for train_in_station in capacity:
            if train_in_station.train == train and train_in_station.leave_time == None:
                return True
        return False

    def add_new_train_in_station(self, train_in_station: TrainInStation, result, train_to_replace=False):
        """

        :param train_in_station: 
        :type train_in_station: TrainInStation
        :param result: 
        :param train_to_replace:  (Default value = False)

        """
        global TRAIN_NOT_IN_STATION
        enable, delay_time = self.compare_free_place(train_in_station)
        if not enable:
            if delay_time != -1:
                return False
            elif not train_to_replace:
                return False
        if result is not None:
            i = 0
            for _train_in_station in TRAIN_NOT_IN_STATION:
                if _train_in_station.train == train_in_station.train:
                    result.save_train_start(
                        train_in_station.train.id, 0, train_in_station.station_id)
                    TRAIN_NOT_IN_STATION.pop(i)
                    #self.add_train_leave_time(train_in_station.train, start_time + 1, train_in_station.station_id,result)
                    break
                i += 1
        capacity_pos = 0
        finish = 0
        inserted = 0
        for capacity in self.stations[train_in_station.station_id]:
            if Stationlist._capacity_is_full(capacity) and Stationlist._train_in_capacity(capacity, train_to_replace):
                capacity.append(train_in_station)
                capacity.sort(key=lambda x: x.arrive_train_time)
                inserted = 1
                return True
            elif Stationlist._capacity_is_full(capacity) and train_in_station.leave_time == None:
                capacity_pos += 1
                continue
            if len(capacity) == 0 or capacity[0].arrive_train_time > train_in_station.passenger_in_train_time:
                capacity.append(train_in_station)
                capacity.sort(key=lambda x: x.arrive_train_time)
                return True
            last_train_in_station = len(capacity) - 1
            for i in range(last_train_in_station):
                leave_time = capacity[i].leave_time
                if train_in_station.leave_time != None and Stationlist._train_in_station_is_free(leave_time, capacity[i + 1],
                                                                                                 train_in_station.arrive_train_time, train_in_station.leave_time):
                    finish = 1
                    break
            leave_time = capacity[last_train_in_station].leave_time
            if leave_time == None:
                pass
            elif leave_time < train_in_station.arrive_train_time:
                finish = 1

            if finish == 1:
                break
            capacity_pos += 1
        if train_to_replace and inserted == 0:
            i = 0
            for capacity in self.stations[train_in_station.station_id]:
                if Stationlist._capacity_is_full(capacity):
                    i = i+1
                else:
                    self.stations[train_in_station.station_id][i].append(
                        train_in_station)
                    self.stations[train_in_station.station_id][i].sort(
                        key=lambda x: x.arrive_train_time)
                    break
        if enable:
            self.stations[train_in_station.station_id][capacity_pos].append(
                train_in_station)
            self.stations[train_in_station.station_id][capacity_pos].sort(
                key=lambda x: x.arrive_train_time)
            return True

    def add_train_leave_time(self, train, leave_time, station_number, result):
        """

        :param train: 
        :param leave_time: 
        :param station_number: 
        :param result: 

        """

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
        for train_not_in_station in TRAIN_NOT_IN_STATION:
            if train == train_not_in_station.train:
                self.add_new_train_in_station(TrainInStation(
                    0, 1, train, leave_time, station_number), result)
        return True

    def read_trains_from_station(self, station_number, also_not_in_station_trains=True):
        """

        :param station_number: 
        :param also_not_in_station_trains:  (Default value = True)

        """
        trains = []
        start_times = []
        one_empty_capacity = 0
        train_not_in_station_start_time = sys.maxsize
        global TRAIN_NOT_IN_STATION
        for capacity in self.stations[station_number]:
            if len(capacity) > 0:
                for i in range(len(capacity)):
                    train_in_station = capacity[i]
                    if train_in_station.leave_time is None:
                        trains.append(train_in_station.train)
                        start_times.append(train_in_station.arrive_train_time)
                    if i + 1 == len(capacity):
                        if train_not_in_station_start_time > train_in_station.passenger_in_train_time + 1:
                            train_not_in_station_start_time = train_in_station.passenger_in_train_time + 1
            else:
                one_empty_capacity = 1

        if also_not_in_station_trains:
            for train_not_in_station in TRAIN_NOT_IN_STATION:
                # check if the station is at least to the time train_not_in_station_start_time for at least one train free
                # only then return the train
                if one_empty_capacity == 1:
                    train_not_in_station.arrive_train_time = 0
                    train_not_in_station.passenger_in_train_time = 1
                    trains.append(train_not_in_station.train)
                    start_times.append(0)

        return start_times, trains, Station(station_number, len(self.stations[station_number]))

    @staticmethod
    def train_leave_time(train_in_station: TrainInStation):
        """

        :param train_in_station: 
        :type train_in_station: TrainInStation

        """
        if train_in_station.leave_time is None:
            return train_in_station.passenger_in_train_time
        else:
            return train_in_station.leave_time
