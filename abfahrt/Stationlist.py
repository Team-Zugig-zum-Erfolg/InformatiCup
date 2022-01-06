import sys
from typing import List
from typing import Tuple
from abfahrt.classes.Train import Train
from abfahrt.classes.Station import Station
from abfahrt.classes.TrainInStation import TrainInStation
from abfahrt.Result import Result


T_ID = 0
T_START_STATION = 1
T_SPEED = 2
T_CAPACITY = 3

S_ID = 0
S_CAPACITY = 1


class Stationlist:

    def __init__(self, stations: List[Station], trainlist: List[Train], result: Result):
        self.stations = []  # the stations with capacities
        self.result = result
        self.trains_not_in_station = []
        stationlist = []
        for station in stations:
            stationlist.append(station.to_list())

        self.stations.append([])
        station_id = 1
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
                    print("INVALID INPUT: Too many trains in station at beginning!")
                    sys.exit(0)
            else:
                self.trains_not_in_station.append(train_in_station)
                self.trains_not_in_station.sort(
                    key=lambda x: x.train.capacity, reverse=False)

    @staticmethod
    def _capacity_is_full(capacity: List[TrainInStation]) -> bool:
        """
        Checks a capacity if there is a stopped train in it

        Args:
            capacity (List[TrainInStation]): capacity, so a list of TrainInStation objects

        Returns:
            bool: True, if the capacity is full, else False
        """
        for _train_in_station in capacity:
            if _train_in_station.leave_time == None:
                return True
        return False

    def compare_free_place(self, train_in_station: TrainInStation) -> Tuple[bool, int]:
        """
        Checks if a TrainInStation object can be inserted in the station

        Args:
            train_in_station (TrainInStation): the TrainInStation object

        Returns:
            Tuple[bool, int]: [True, -1] if station is free, [False, delay_time > 0] if station is free in delay time, [False, -1] if station is blocked
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

                    if Stationlist._train_in_station_is_free(capacity[i].leave_time, capacity[i + 1].arrive_train_time, train_in_station.arrive_train_time, train_in_station.leave_time):
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
    def _train_in_station_is_free(front_train_leave_time: int, back_train_in_station_arrive_time: int,
                                  in_station_time: int, leave_station_time: int) -> bool:
        """
        Checks if the station is free for a given time range between two other times of trains in the station

        Args:
            front_train_leave_time (int): leave_time of the first train
            back_train_in_station_arrive_time (int): arrive time of the second train
            in_station_time (int): time of the new train arriving at the station
            leave_station_time (int): time of the new train leaving the station

        Returns:
            bool: True, if station is free, else False
        """
        if front_train_leave_time == None:
            return False
        return front_train_leave_time < in_station_time and back_train_in_station_arrive_time > leave_station_time

    @staticmethod
    def _train_in_capacity(capacity: List[TrainInStation], train: Train) -> bool:
        """
        Checks if a train is in a specific capacity

        Args:
            capacity (List[TrainInStation]): capacity, so a list of TrainInStation objects
            train (Train): train to search in the capacity

        Returns:
            bool: True, if the train was found, else False
        """
        if not train:
            return False
        for train_in_station in capacity:
            if train_in_station.train == train and train_in_station.leave_time == None:
                return True
        return False

    def add_new_train_in_station(self, train_in_station: TrainInStation, train_to_replace=None) -> bool:
        """
        Inserts a new TrainInStation objects in the right/best fitting capacity of the station

        Args:
            train_in_station (TrainInStation): TrainInStation object to insert
            train_to_replace ([type], optional): train in the station which should replaced with the new train. Defaults to None.

        Returns:
            bool: True, if inserting was successful, else False
        """
        enable, delay_time = self.compare_free_place(train_in_station)
        if not enable:
            if delay_time != -1:
                return False
            elif not train_to_replace:
                return False
        if self.result:
            i = 0
            for _train_in_station in self.trains_not_in_station:
                if _train_in_station.train == train_in_station.train:
                    self.result.save_train_start(
                        train_in_station.train.id, 0, train_in_station.station_id)
                    self.trains_not_in_station.pop(i)
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
                if train_in_station.leave_time != None and Stationlist._train_in_station_is_free(leave_time, capacity[i + 1].arrive_train_time,
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

    def add_train_leave_time(self, train: Train, leave_time: int, station_number: int) -> bool:
        """
        Adds the leave time of a stopped train in a specific station

        Args:
            train (Train): train to add the leave time
            leave_time (int): the leave time
            station_number (int): the id/number of the station

        Returns:
            bool: True, if adding was successful, else False
        """
        capacity_number = 0
        for capacity in self.stations[station_number]:
            t = 0
            for train_in_station in capacity:
                if train_in_station.train == train and train_in_station.leave_time is None:
                    train_in_station.leave_time = leave_time
                    return True
                t = t + 1
            capacity_number = capacity_number + 1
        for train_not_in_station in self.trains_not_in_station:
            if train == train_not_in_station.train:
                self.add_new_train_in_station(TrainInStation(
                    0, 1, train, leave_time, station_number))
        return True

    def read_trains_from_station(self, station_number: int, also_not_in_station_trains=True) -> Tuple[List[int], List[Train], Station]:
        """
        Retrieves the stopped trains at a station and the possible start/leave times

        Args:
            station_number (int): the id/number of the station
            also_not_in_station_trains (bool, optional): True if also trains with no start station should be checked for starting at the station. Defaults to True.

        Returns:
            Tuple[List[int], List[Train], Station]: start time of the trains, trains in the station, the station as object
        """
        trains = []
        start_times = []
        one_empty_capacity = 0
        train_not_in_station_start_time = sys.maxsize
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
            for train_not_in_station in self.trains_not_in_station:
                # check if the station is at least to the time train_not_in_station_start_time for at least one train free
                # only then return the train
                if one_empty_capacity == 1:
                    train_not_in_station.arrive_train_time = 0
                    train_not_in_station.passenger_in_train_time = 1
                    trains.append(train_not_in_station.train)
                    start_times.append(0)

        return start_times, trains, Station(station_number, len(self.stations[station_number]))
