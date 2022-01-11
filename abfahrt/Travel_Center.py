"""
    This is Travel_Center for managing travels and routes
"""
import math
# This module provides access to the mathematical functions defined by the C standard. (https://docs.python.org/3/library/math.html)
import sys
# This module provides access to some variables used or maintained by the interpreter and to functions that interact strongly with the interpreter. (https://docs.python.org/3/library/sys.html)
from typing import List
# This module provides runtime support for type hints. The most fundamental support consists of the types Any, Union, Callable, TypeVar, and Generic. For a full specification, please see PEP 484. For a simplified introduction to type hints, see PEP 483. (https://docs.python.org/3/library/typing.html)
from typing import Tuple
# These can be used as types in annotations using [], each having a unique syntax. (https://docs.python.org/3/library/typing.html)

from decimal import Decimal

from abfahrt.Groups import Groups
from abfahrt.classes.Passenger import Passenger
from abfahrt.classes.Line import Line
from abfahrt.classes.Train import Train
from abfahrt.Stationlist import Stationlist
from abfahrt.Linelist import Linelist
from abfahrt.classes.Travel import Travel
from abfahrt.classes.TrainInLine import TrainInLine
from abfahrt.classes.TrainInStation import TrainInStation
from abfahrt.classes.Station import Station
from abfahrt.Plan import Plan
from abfahrt.Result import Result

L_ID = 0
L_S_ID_START = 1
L_S_ID_END = 2
L_LEN = 3
L_CAPACITY = 4

S_ID = 0
S_CAPACITY = 1

T_ID = 0
T_S_ID = 1
T_SPEED = 2
T_CAPACITY = 3


class Travel_Center:

    def __init__(self, train_input_list: List[Train], stationlist: Stationlist,
                 linelist: Linelist, result: Result):
        """
        Initializing Travel_Center
        """
        self.max_train_capacity = 0
        self.train_line_time_list = []
        self.line_plan = []

        self.stationlist = stationlist
        self.linelist = linelist
        self.result = result

        station_input_list = []
        line_input_list = []

        for station_as_list in self.stationlist.stationlist:
            station_input_list.append(station_as_list)

        for line_as_list in self.linelist.linelist:
            line_input_list.append(line_as_list)

        self.line_input_list = line_input_list
        self.station_input_list = station_input_list
        self.train_input_list = train_input_list

        self.average_line_length = 0

        self.train_line_time_list.append([])

        self.plan = Plan()

        for train in train_input_list:
            if train.capacity > self.max_train_capacity:
                self.max_train_capacity = train.capacity
            self.train_line_time_list.append([])
            self.train_line_time_list[train.id].append(0)
            for line in line_input_list:
                self.train_line_time_list[train.id].append(
                    math.ceil(Decimal.from_float(line[L_LEN]) / Decimal.from_float(train.speed)) - 1)

        self.line_plan.append([])
        self.line_plan[0].append([])
        for station in station_input_list:
            self.line_plan.append([])
            self.line_plan[station[S_ID]].append([])
            self.line_plan[station[S_ID]].append([])
            self.plan.add_node(station[S_ID])
            for line in line_input_list:
                if line[L_S_ID_START] == station[S_ID]:
                    self.line_plan[station[S_ID]][0].append(line[L_S_ID_END])
                    self.line_plan[station[S_ID]][1].append(line[L_ID])
                    self.plan.add_edge(
                        station[S_ID], line[L_S_ID_END], line[L_LEN])
                elif line[L_S_ID_END] == station[S_ID]:
                    self.line_plan[station[S_ID]][0].append(line[L_S_ID_START])
                    self.line_plan[station[S_ID]][1].append(line[L_ID])
                    self.plan.add_edge(
                        station[S_ID], line[L_S_ID_START], line[L_LEN])

        full_lines_length = 0
        for line in line_input_list:
            full_lines_length += line[L_LEN]
        self.average_line_length = full_lines_length / len(line_input_list)

    def check_plan(self) -> bool:
        """
        Checks if all stations of the plan are connected via at least one route

        Returns:
            bool: status of plan, true = valid, false = invalid
        """
        if self.plan.is_connected():
            return True
        return False

    def find_routes(self, s_station_id: int, e_station_id: int) -> List[List[Line]]:
        """
        Determines the shortest line route between two stations calculated by dijkstra

        Args:
            s_station_id (int): the start station
            e_station_id (int): the end station

        Returns:
            Tuple[List[Line]]: lines of the route
        """
        _, prev_list = self.plan.dijkstra(s_station_id)
        path = self.plan.get_shortest_path(prev_list, e_station_id)
        lineplans = [path]
        lines = []
        j = 0
        for lineplan in lineplans:
            lines.append([])
            for i in range(len(lineplan) - 1):
                t = 0
                for station in self.line_plan[lineplan[i]][0]:
                    if station == lineplan[i + 1]:
                        lines[j].append(self.line_plan[lineplan[i]][1][t])
                        break
                    t += 1
            j += 1
        return lines

    def find_best_route(self, s_station_id: int, e_station_id: int) -> Tuple[int, List[Line]]:
        """
        Determines the length and the shortest line route between two stations

        Args:
            s_station_id (int): start station id
            e_station_id (int): end station id

        Returns:
            Tuple[int, List[Line]]: length, lines
        """
        lines = self.find_routes(s_station_id, e_station_id)
        short_len = 0
        short_line = None
        for line in lines:
            length = 0
            for each in line:
                length += self.line_input_list[each - 1][L_LEN]
            if short_len == 0 or short_len > length:
                short_len = length
                short_line = line
        return [short_len, short_line]

    def find_only_one_line_between_stations(self, start_station_id: int, end_station_id: int) -> Tuple[int, List[Line]]:
        """
        Find the line which connects two stations with each other

        Args:
            start_station_id (int): start station id
            end_station_id (int): end station id

        Returns:
            Tuple[int, List[Line]]: line length, line in list
        """
        t = 0
        line = None
        for next_station_id in self.line_plan[start_station_id][0]:
            if next_station_id == end_station_id:
                line = self.line_plan[start_station_id][1][t]
                break
            t += 1
        length = self.line_input_list[line - 1][L_LEN]
        return [length, [line]]

    def time_count_length(self, start_station: Station, end_station: Station) -> int:
        """
        Find the shortest route and its length by using dijkstra

        Args:
            start_station (Station): start station
            end_station (Station): end station

        Returns:
            int: length of the shortest route
        """
        length, _ = self.find_best_route(start_station.id, end_station.id)
        return length

    def time_count_train(self, start_station: Station, end_station: Station, train: Train, start_time: int,
                         use_one_line=False) -> Travel:
        """
        Find the shortest route by using dijkstra and creating a travel for the specific
        train at a specific start time

        Args:
            start_station (Station): start station
            end_station (Station): end station
            train (Train): train for creating the travel
            start_time (int): start time of the travel
            use_one_line (bool, optional): Find and use only an one line route. Defaults to False.

        Returns:
            Travel: travel with the train and beginning at the start time
        """
        if use_one_line == False:
            length, lines = self.find_best_route(
                start_station.id, end_station.id)
        else:
            length, lines = self.find_only_one_line_between_stations(
                start_station.id, end_station.id)
        line_time = []
        station_times = [TrainInStation(
            start_time, start_time + 1, train, None, start_station.id)]
        on_board = start_time + 1
        add_time = on_board + 1
        prev_station = start_station
        for li in range(len(lines)):
            line_time.append(TrainInLine(train.id, add_time,
                                         add_time + self.train_line_time_list[train.id][lines[li]], lines[li]))
            stations = self.get_stations_by_line(lines[li])
            if stations[0].id != prev_station.id:
                next_station = stations[0]
            else:
                next_station = stations[1]

            current_leave_time = None
            current_passenger_in_time = add_time + \
                self.train_line_time_list[train.id][lines[li]] + 1

            if next_station.id != end_station.id:
                current_leave_time = add_time + \
                    self.train_line_time_list[train.id][lines[li]]
                current_passenger_in_time = add_time + \
                    self.train_line_time_list[train.id][lines[li]]

            station_times.append(TrainInStation(
                add_time +
                self.train_line_time_list[train.id][lines[li]
                                                    ], current_passenger_in_time, train,
                current_leave_time, next_station.id))

            add_time += self.train_line_time_list[train.id][lines[li]] + 1

            prev_station = next_station

        if start_station != end_station:
            station_time = TrainInStation(
                add_time - 1, add_time, train, None, end_station.id)
        else:
            station_time = TrainInStation(
                start_time, start_time + 1, train, None, start_station.id)

        return Travel(start_time, on_board, line_time, station_time, start_station, end_station, train, station_times,
                      length)

    def get_fastest_train_by_start_times_and_route_length(self, trainlist: List[Train], start_time_list: List[int],
                                                          route_length: int) -> Tuple[Train, int]:
        """
        Get the fastest/eraliest train, if there are multiple trains with different possible start times
        and a specific route length

        Args:
            trainlist (List[Train]): trains
            start_time_list (List[int]): start times of the trains
            route_length (int): length of the route

        Returns:
            Tuple[Train, int]: the earliest train at the target, the start time of this train 
        """
        train_fastest = trainlist[0]
        train_fastest_start_time = start_time_list[0]
        time_all_smallest = start_time_list[0] + \
            route_length / trainlist[0].speed

        for count in range(len(trainlist)):
            time_all = start_time_list[count] + \
                route_length / trainlist[count].speed
            if time_all < time_all_smallest:
                time_all_smallest = time_all
                train_fastest = trainlist[count]
                train_fastest_start_time = start_time_list[count]

        return [train_fastest, train_fastest_start_time]

    def full_stations_list_not_empty(self, full_stations_list: List[Tuple[Station, int]]) -> bool:
        """
        Just checks if the list has at least one not empty element list

        Args:
            full_stations_list (List[Tuple[Station, int]]): list of the full station with the possible clearing time

        Returns:
            bool: True if the list has at least one not empty element list, else False
        """
        if full_stations_list == None:
            return False
        for full_stations in full_stations_list:
            if len(full_stations) > 0:
                return True
        return False

    def get_stations_by_line(self, line_id: int) -> Tuple[Station, Station]:
        """
        Get the two stations a line is connecting

        Args:
            line_id (int): line id

        Returns:
            Tuple[Station, Station]: the two stations
        """
        line = self.line_input_list[line_id - 1]
        station_1 = Station(self.station_input_list[line[L_S_ID_START] - 1]
                            [S_ID], self.station_input_list[line[L_S_ID_START] - 1][S_CAPACITY])
        station_2 = Station(self.station_input_list[line[L_S_ID_END] - 1]
                            [S_ID], self.station_input_list[line[L_S_ID_END] - 1][S_CAPACITY])
        return [station_1, station_2]

    def check_line_station(self, travel: Travel, clearing=False) -> Tuple[bool, int, bool, List[Tuple[Station, int]]]:
        """
        Checks the lines and stations for the specific times of a travel and calculates
        the smallest delay time, at which they are free, if they are not free at the current time.

        Args:
            travel (Travel): travel for checking
            clearing (bool, optional): True, if no full stations should be checked. Defaults to False.

        Returns:
            Tuple[bool, int, bool, List[Tuple[Station, int]]]: whole travel is free, delay time, end station is full, full stations on the route
        """
        line_availables_list = []
        line_time_changes = []
        station_availables_list = []
        station_time_changes = []
        available = True
        station_is_full = False
        full_stations = []
        next_station = travel.start_station
        prev_station_blocked = False
        for travel_in_line in travel.line_time:
            line_available, line_time_change = self.linelist.compare_free(
                travel_in_line)

            line_availables_list.append(line_available)
            line_time_changes.append(line_time_change)
            next_station = self.get_next_station_in_travel(
                travel, next_station)

            current_leave_time = None
            current_passenger_in_time = travel_in_line.end + 1

            if next_station.id != travel.end_station.id:
                current_leave_time = travel_in_line.end
                current_passenger_in_time = travel_in_line.end

            s_available, s_time_change = self.stationlist.compare_free_place(TrainInStation(
                travel_in_line.end, current_passenger_in_time, travel_in_line.train, current_leave_time,
                next_station.id))

            if s_available == False and s_time_change == -1 and clearing == False:  # full
                clear_time = self.check_clear_station(next_station, self.get_prev_station_in_travel(
                    travel, next_station), prev_station_blocked, travel_in_line.end - 2, travel.station_times,
                    travel.train, travel)
                full_stations.append([next_station, clear_time])
                s_time_change = clear_time
                prev_station_blocked = True
            else:
                prev_station_blocked = False

            station_availables_list.append(s_available)
            station_time_changes.append(s_time_change)

        station_available, station_time_change = self.stationlist.compare_free_place(
            travel.station_time)

        if station_available == False and station_time_change == -1:
            station_is_full = True
            available = False

        station_delay_time = 0
        if not station_available and station_is_full == False:
            station_delay_time = ((station_time_change) -
                                  travel.station_time.arrive_train_time)
            available = False

        delay_time = station_delay_time

        for i in range(len(travel.line_time)):
            if not line_availables_list[i]:
                available = False
                line_delay_time = line_time_changes[i] - \
                    travel.line_time[i].start
                if delay_time < line_delay_time:
                    delay_time = line_delay_time

        for i in range(0, len(travel.station_times[1:])):
            if not station_availables_list[i]:
                available = False
                current_station_delay_time = station_time_changes[i] - \
                    travel.station_times[i + 1].arrive_train_time
                if delay_time < current_station_delay_time:
                    delay_time = current_station_delay_time

        return [available, delay_time, station_is_full, full_stations]

    def delay_travel(self, travel: Travel, delay_time: int) -> None:
        """
        Delay travel by a given delay time

        Args:
            travel (Travel): travel to delay
            delay_time (int): delay time

        Returns:
            None
        """
        travel.start_time = travel.start_time + delay_time
        travel.on_board = travel.on_board + delay_time
        for i in range(0, len(travel.line_time)):
            travel.line_time[i].start = travel.line_time[i].start + delay_time
            travel.line_time[i].end = travel.line_time[i].end + delay_time
        for i in range(0, len(travel.station_times)):
            travel.station_times[i].arrive_train_time = travel.station_times[i].arrive_train_time + delay_time
            travel.station_times[i].passenger_in_train_time = travel.station_times[
                i].passenger_in_train_time + delay_time
            if travel.station_times[i].leave_time != None:
                travel.station_times[i].leave_time = travel.station_times[i].leave_time + delay_time
        travel.station_time.arrive_train_time = travel.station_time.arrive_train_time + delay_time
        travel.station_time.passenger_in_train_time = travel.station_time.passenger_in_train_time + delay_time

    def save_travel(self, travel: Travel, groups: Groups, passengers: List[Passenger], train_to_replace=None) -> bool:
        """
        Save a travel for the specific train and the times, in which the train is in the
        lines and stations

        Args:
            travel (Travel): travel for saving
            groups (Groups): groups instance for registering passengers as arrived
            passengers (List[Passenger]): passengers of the travel
            train_to_replace ([type], optional): the origin train, if a station is cleared. Defaults to None.

        Returns:
            bool: True, if the saving was successful, else False
        """
        enable, _, full, _ = self.check_line_station(
            travel)
        if enable or (full == True and train_to_replace):

            start_station_leave_time = None
            if travel.start_station != travel.end_station:
                start_station_leave_time = travel.on_board

            self.stationlist.add_train_leave_time(
                travel.train, start_station_leave_time, travel.start_station.id)

            for train_in_line in travel.line_time:
                self.linelist.add_new_train_in_line(train_in_line)
                self.result.save_train_depart(
                    train_in_line.train, train_in_line.start, train_in_line.line_id)

            for train_in_station in travel.station_times[1:len(travel.station_times) - 1]:
                self.stationlist.add_new_train_in_station(
                    train_in_station)

            if travel.start_station != travel.end_station:
                self.stationlist.add_new_train_in_station(
                    travel.station_time, train_to_replace)

            if passengers and groups:
                groups.passengers_arrive(passengers)
                for passenger in passengers:
                    self.result.save_passenger_board(
                        passenger.id, travel.on_board, travel.train.id)
                    self.result.save_passenger_detrain(
                        passenger.id, travel.station_time.passenger_in_train_time)

            return True
        else:
            return False

    def determine_and_save_shortest_travel(self, travels: List[Travel], groups: Groups,
                                           passengers: List[Passenger]) -> bool:
        """
        Determining the shortest travel and saving it, if it is possible 

        Args:
            travels (List[Travel]): travels to check and perhaps to save
            groups (Groups): groups instance for registering passengers as arrived
            passengers (List[Passenger]): passengers for the travels

        Raises:
            NameError: if for every travel no station is blocked and the delay time is 0

        Returns:
            bool: True, if one travel could be saved, else False
        """
        save = 0
        if len(travels):
            while not save:
                full_station_list = []
                availables = []
                delay_times = []
                # if full_end_station[i]=True, then for travels[i] the end_station is blocked
                full_end_station = []
                # blocked = (there are only trains with leave_time=None before the train will arrive)

                for travel in travels:
                    available, delay_time, full, full_stations = self.check_line_station(
                        travel)
                    availables.append(available)
                    delay_times.append(delay_time)
                    # full==1: the end_station is blocked by stopped trains with leave_time=None
                    full_end_station.append(full)
                    full_station_list.append(full_stations)

                i = 0
                available_run = 0
                travel_available = []
                for available in availables:
                    if available:
                        travel_available.append(travels[i])
                        available_run = 1
                    i += 1

                if available_run:
                    short_time = travel_available[0].station_time.arrive_train_time
                    short_travel = travel_available[0]
                    for travel in travel_available:
                        if short_time > travel.station_time.arrive_train_time:
                            short_time = travel.station_time.arrive_train_time
                            short_travel = travel
                    if passengers is None and groups:
                        b_choose, passengers = groups.group_choose(short_travel.start_station, short_travel.end_station,
                                                                   short_travel.train.capacity)
                        if not b_choose:
                            groups = None
                    save = self.save_travel(
                        short_travel, groups, passengers)

                # travels have to be delayed first, before clearing full stations
                elif 0 not in delay_times and -1 not in delay_times:
                    i = 0
                    for travel in travels:
                        self.delay_travel(travel, delay_times[i])
                        i += 1

                # at least one station is blocked on the route
                elif self.full_stations_list_not_empty(full_station_list):

                    # free all FULL stations on the route of the shortest travel, so the train of the travel can pass them
                    travel_short = None
                    smallest_arrive_time = sys.maxsize
                    t = 0
                    i = 0
                    for travel in travels:
                        if delay_times[i] == 0 and smallest_arrive_time > travel.station_time.arrive_train_time:
                            travel_short = travel
                            smallest_arrive_time = travel.station_time.arrive_train_time
                            t = i
                        i = i + 1
                    station_to_clear = full_station_list[t][0][0]
                    arrive_time = full_station_list[t][0][1]

                    self.clear_station(station_to_clear, self.get_prev_station_in_travel(
                        travel_short, station_to_clear), arrive_time - 2, travel_short.station_times,
                        travel_short.train, travel_short)

                    travels = [travel_short]

                else:
                    raise NameError(
                        "Error: no full stations or delayable travels")

            return True
        else:
            # error: input is invalid, because no route was found, but all stations have to be connected with each other
            # (so this should never happen)
            return False

    def check_valid_train_exist_in_stations(self, max_group_size: int) -> bool:
        """
        Checks if there is at least on train in at least one station, with a
        capacity >= max_group_size

        Args:
            max_group_size (int): group size of passengers with biggest group size

        Returns:
            bool: True, if there is a valid train for the group size, else False
        """
        for train in self.train_input_list:
            if train.capacity >= max_group_size:
                found = False
                for train_in_station in self.stationlist.trains_not_in_station:
                    if train == train_in_station.train:
                        found = True
                if not found:
                    return True
        return False

    def check_passengers(self, passengers: List[Passenger]) -> Tuple[Station, Station, int]:
        """
        Retrieves the start and end station of the passengers route and their group size

        Args:
            passengers (List[Passenger]): passengers to check

        Returns:
            Tuple[Station, Station, int]: start station, end station, group size
        """
        start_station = passengers[0].start_station
        end_station = passengers[0].end_station
        group_size = 0
        for passenger in passengers:
            group_size = group_size + passenger.group_size
        return [start_station, end_station, group_size]

    def check_train_in_station(self, start_station: Station, group_size: int, include_not_in_station_trains=True) -> \
            Tuple[List[int], List[Train], bool, int, int]:
        """
        Retrieves the trains with a valid capacity in a station, for a specific group size 

        Args:
            start_station (Station): start station
            group_size (int): group size to check, same as the min capacity of every train
            include_not_in_station_trains (bool, optional): If True, also trains with no start station will be checked for starting at the station. Defaults to True.

        Returns:
            Tuple[List[int], List[Train], bool, int, int]: start times of the trains, trains, trains found, train's capacity in current station, largest capacity among the trains
        """
        start_times, trains, _ = self.stationlist.read_trains_from_station(
            start_station.id, include_not_in_station_trains)
        train_capacity = 0
        if len(trains) > 0:
            for train in trains:
                if train_capacity < train.capacity:
                    train_capacity = train.capacity
        capacity_enable = self.check_capacity(
            trains, group_size, start_times, None)
        return start_times, trains, capacity_enable, train_capacity, self.max_train_capacity

        # choose train from other station

    def check_train_not_in_station(self, group_size: int, include_not_in_station_trains=True) -> Tuple[
            List[int], List[Train], List[Station], bool]:
        """
        Retrieves the trains with a valid capacity for a specifc group size in all
        stations of the whole plan

        Args:
            group_size (int): group size, same as the min capacity of the trains
            include_not_in_station_trains (bool, optional): If True, also trains with no start station will be checked for starting at the station. Defaults to True.

        Returns:
            Tuple[List[int], List[Train], List[Station], bool]: start times of the trains, trains, start stations of the trains, trains found
        """
        start_times, trains, start_stations = self.check_trains_in_all_station(
            include_not_in_station_trains)
        capacity_enable = self.check_capacity(
            trains, group_size, start_times, start_stations)
        return start_times, trains, start_stations, capacity_enable

    def get_neighboor_stations(self, station: Station) -> List[Station]:
        """
        Retrieves all neighboor stations of a station

        Args:
            station (Station): station for getting the neighboor stations

        Returns:
            List[Station]: neighboor stations
        """
        neighboor_stations = []
        for line in self.line_input_list:
            if line[L_S_ID_START] == station.id:
                neighboor_stations.append(
                    Station(line[L_S_ID_END], self.station_input_list[line[L_S_ID_END] - 1][S_CAPACITY]))
            elif line[L_S_ID_END] == station.id:
                neighboor_stations.append(
                    Station(line[L_S_ID_START], self.station_input_list[line[L_S_ID_START] - 1][S_CAPACITY]))

        return neighboor_stations

    def station_is_never_blocked(self, station: Station) -> bool:
        """
        Checks if a station is not blocked at least for one capacity

        Args:
            station (Station): station to check

        Returns:
            bool: True, if not blocked for one or more capacities, else False
        """
        for capacity in self.stationlist.stations[station.id]:
            if len(capacity) == 0:
                return True
            blocked = 0
            for train_in_station in capacity:
                if train_in_station.leave_time is None:
                    blocked = 1
            if blocked == 0:
                return True
        return False

    def station_is_in_station_times_list(self, station: Station, station_times_list: List[TrainInStation]) -> bool:
        """
        Checks if a station is in a list of TrainInStation entities/objects 

        Args:
            station (Station): station to find/check in the list
            station_times_list (List[TrainInStation]): list of TrainInStation entities/objects

        Returns:
            bool: True, if the station was found, else False
        """
        for station_time in station_times_list:
            if station.id == station_time.station_id:
                return True
        return False

    def get_next_station_in_travel(self, travel: Travel, station: Station) -> Station:
        """
        Retrieves the next station after a specific station on the route of a travel

        Args:
            travel (Travel): travel with the route
            station (Station): station for getting the next station on the route

        Returns:
            Station: next station or None, if the no next station was found
        """
        neighboor_stations = self.get_neighboor_stations(station)
        station_times = travel.station_times
        for i in range(1, len(station_times)):
            if station_times[i - 1].station_id == station.id:
                for neighboor_station in neighboor_stations:
                    if station_times[i].station_id == neighboor_station.id:
                        return neighboor_station
        return None

    def get_prev_station_in_travel(self, travel: Travel, station: Station) -> Station:
        """
        Retrieves the previous station bevor a specific station on the route of a travel

        Args:
            travel (Travel): travel with the route
            station (Station): station for getting the previous station on the route

        Returns:
            Station: previous station or None, if the no previous station was found
        """
        neighboor_stations = self.get_neighboor_stations(station)
        for i in range(1, len(travel.station_times)):
            if travel.station_times[i].station_id == station.id:
                for neighboor_station in neighboor_stations:
                    if travel.station_times[i - 1].station_id == neighboor_station.id:
                        return neighboor_station
        return None

    def station_has_more_than_one_free_capcacity(self, station: Station) -> bool:
        """
        Checks if a station has more than one free/not blocked capacities 

        Args:
            station (Station): station to check

        Returns:
            bool: True, if the station has more than one free capacity, else False
        """
        capacities = self.stationlist.stations[station.id]
        free = 0
        for capacity in capacities:
            if not Stationlist._capacity_is_full(capacity):
                free = free + 1
        return free >= 2

    def check_clear_station(self, target_station: Station, prev_station: Station, prev_station_blocked_before: bool,
                            arrive_time: int, stations_to_ignore: List[TrainInStation], train_to_replace=None,
                            original_travel=None) -> int:
        """
        Calculates the earliest possible clearing time for a station

        Args:
            target_station (Station): station to check for clearing
            prev_station (Station): previous station on the travel route
            prev_station_blocked_before (bool): blocking status of the previous station
            arrive_time (int): time/round the train of the travel wants to arrive at the station to clear
            stations_to_ignore (List[TrainInStation]): list of TrainInStation objects which includes all stations to ignore for clearing
            train_to_replace ([type], optional): the train which wants arrive at the station to clear. Defaults to None.
            original_travel ([type], optional): the travel of the train which wants arrive at the station to clear. Defaults to None.

        Raises:
            NameError: if no station for clearing is available

        Returns:
            int: earliest possible clearing time
        """

        # get the neighboor stations of the target_station,
        # so the blocking trains in the target_station can be moved to one of the free
        # (or not blocked) neighboor stations
        # print(target_station)
        neighboor_stations = self.get_neighboor_stations(target_station)
        next_station = None
        for neighboor_station in neighboor_stations:
            if self.station_is_never_blocked(neighboor_station) == True and (
                    not self.station_is_in_station_times_list(neighboor_station,
                                                              stations_to_ignore) or self.station_has_more_than_one_free_capcacity(
                        neighboor_station)):
                next_station = neighboor_station
                break
        if next_station == None and prev_station != None:
            for neighboor_station in neighboor_stations:
                if neighboor_station == prev_station:
                    next_station = prev_station
        if next_station == None:
            # no neighboor station is free (free = not blocked) and origin station is also not available
            raise NameError("clear station error: no station available")

        # get the blocking trains in the station (blocking trains = trains in the station with no leave time)
        # a station is only blocked, if all trains in the station have no leave time
        start_times, trains, _ = self.stationlist.read_trains_from_station(
            target_station.id, False)
        i = 0
        for start_time in start_times:
            if start_time < arrive_time:
                start_times[i] = arrive_time
            i = i + 1

        travels = []
        i = 0
        for train in trains:
            travels.append(self.time_count_train(target_station, next_station, train,
                                                 start_times[i], True))
            i = i + 1
        available = 0
        while not available:
            full_station_list = []
            availables = []
            delay_times = []
            # if full_end_station[i]=True, then for travels[i] the target_station is blocked
            full_end_station = []

            for travel in travels:
                available_current, delay_time, full, full_stations = self.check_line_station(
                    travel, True)
                availables.append(available_current)
                delay_times.append(delay_time)
                # full==1: the target_station is blocked by stopped trains with leave_time=None
                full_end_station.append(full)
                full_station_list.append(full_stations)

            i = 0
            available_run = 0
            travel_available = []
            for available in availables:
                if available:
                    travel_available.append(travels[i])
                    available_run = 1
                i += 1

            if available_run:
                short_time = travel_available[0].station_time.arrive_train_time
                short_travel = travel_available[0]
                for travel in travel_available:
                    if short_time > travel.station_time.arrive_train_time:
                        short_time = travel.station_time.arrive_train_time
                        short_travel = travel

                return short_travel.on_board + 1

            # target_station is for at least one travel free (so not blocked)
            elif False in full_end_station or 0 not in delay_times:
                i = 0
                for travel in travels:
                    self.delay_travel(travel, delay_times[i])
                    i += 1
            elif next_station == prev_station:
                short_time = sys.maxsize
                short_travel = None
                i = 0
                for travel in travels:
                    if short_time > travel.station_time.arrive_train_time and delay_times[i] == 0:
                        short_time = travel.station_time.arrive_train_time
                        short_travel = travel
                    i = i + 1

                start_times, trains, _ = self.stationlist.read_trains_from_station(
                    prev_station.id, False)

                other_train_is_blocking_station = False
                for train in trains:
                    if train != train_to_replace:
                        other_train_is_blocking_station = True

                if prev_station_blocked_before == False and other_train_is_blocking_station:
                    clear_time = self.check_clear_station(prev_station, self.get_prev_station_in_travel(original_travel,
                                                                                                        prev_station),
                                                          False,
                                                          travel.station_time.arrive_train_time - 2, stations_to_ignore,
                                                          train_to_replace, original_travel)
                    difference = clear_time - travel.station_time.arrive_train_time
                    if difference > 0:
                        return short_travel.on_board + 1 + difference

                return short_travel.on_board + 1

            else:
                # all neighboor stations are blocked (should actually not happen, because they are checked above)
                raise NameError("clear station error: no station available")
        return True

    def clear_station(self, target_station: Station, prev_station: Station, arrive_time: int,
                      stations_to_ignore: List[TrainInStation], train_to_replace=None, original_travel=None) -> bool:
        """
        Clears a station at the earliest possible clearing time

        Args:
            target_station (Station): station to check for clearing
            prev_station (Station): previous station on the travel route
            arrive_time (int): time/round the train of the travel wants to arrive at the station to clear
            stations_to_ignore (List[TrainInStation]): list of TrainInStation objects which includes all stations to ignore for clearing
            train_to_replace ([type], optional): the train which wants arrive at the station to clear. Defaults to None.
            original_travel ([type], optional): the travel of the train which wants arrive at the station to clear. Defaults to None.

        Raises:
            NameError: if no station for clearing is available

        Returns:
            bool: True, if station was cleared successful, else False
        """

        # clear station (move trains out of it to other stations)

        # get the neighboor stations of the target_station,
        # so the blocking trains in the target_station can be moved to one of the free
        # (or not blocked) neighboor stations
        neighboor_stations = self.get_neighboor_stations(target_station)
        next_station = None
        for neighboor_station in neighboor_stations:
            if self.station_is_never_blocked(neighboor_station) == True and (
                    not self.station_is_in_station_times_list(neighboor_station,
                                                              stations_to_ignore) or self.station_has_more_than_one_free_capcacity(
                        neighboor_station)):
                next_station = neighboor_station
                break
        if next_station == None and prev_station != None:
            for neighboor_station in neighboor_stations:
                if neighboor_station == prev_station:
                    next_station = prev_station
        if next_station == None:
            # no neighboor station is free (free = not blocked) and origin station is also not available
            raise NameError("clear station error: no station available")

        # get the blocking trains in the station (blocking trains = trains in the station with no leave time)
        # a station is only blocked, if all trains in the station have no leave time
        start_times, trains, _ = self.stationlist.read_trains_from_station(
            target_station.id, False)
        i = 0
        for start_time in start_times:
            if start_time < arrive_time:
                start_times[i] = arrive_time
            i = i + 1

        travels = []
        i = 0
        for train in trains:
            travels.append(self.time_count_train(target_station, next_station, train,
                                                 start_times[i], True))
            i = i + 1
        available = 0
        while not available:
            full_station_list = []
            availables = []
            delay_times = []
            # if full_end_station[i]=True, then for travels[i] the target_station is blocked
            full_end_station = []

            for travel in travels:
                available_current, delay_time, full, full_stations = self.check_line_station(
                    travel, True)
                availables.append(available_current)
                delay_times.append(delay_time)
                # full==1: the target_station is blocked by stopped trains with leave_time=None
                full_end_station.append(full)
                full_station_list.append(full_stations)

            i = 0
            available_run = 0
            travel_available = []
            for available in availables:
                if available:
                    travel_available.append(travels[i])
                    available_run = 1
                i += 1

            if available_run:
                short_time = travel_available[0].station_time.arrive_train_time
                short_travel = travel_available[0]
                for travel in travel_available:
                    if short_time > travel.station_time.arrive_train_time:
                        short_time = travel.station_time.arrive_train_time
                        short_travel = travel

                self.save_travel(
                    short_travel, None, None)
                available = 1
            # target_station is for at least one travel free (so not blocked)
            elif False in full_end_station or 0 not in delay_times:
                i = 0
                for travel in travels:
                    self.delay_travel(travel, delay_times[i])
                    i += 1
            elif next_station == prev_station:
                short_time = sys.maxsize
                short_travel = None
                i = 0
                for travel in travels:
                    if short_time > travel.station_time.arrive_train_time and delay_times[i] == 0:
                        short_time = travel.station_time.arrive_train_time
                        short_travel = travel
                    i = i + 1

                start_times, trains, _ = self.stationlist.read_trains_from_station(
                    prev_station.id, False)

                if prev_station and train_to_replace not in trains and len(trains) == prev_station.capacity:
                    self.clear_station(prev_station, self.get_prev_station_in_travel(original_travel, prev_station),
                                       short_travel.station_time.arrive_train_time - 2, stations_to_ignore,
                                       train_to_replace, original_travel)
                self.save_travel(
                    short_travel, None, None, train_to_replace)
                available = 1
            else:
                # all neighboor stations are blocked (should actually not happen, because they are checked above)
                raise NameError("clear station error: no station available")
        return True

    # move a train to start station
    def train_move_to_start_station(self, start_station: Station, trains: List[Train], start_times: List[int],
                                    start_stations: List[Station], groups: Groups) -> bool:
        """
        Moves the fastest train by given trains and start times to a specific station

        Args:
            start_station (Station): station to move the fastest train
            trains (List[Train]): possible trains
            start_times (List[int]): start times of the trains
            start_stations (List[Station]): start stations of the trains
            groups (Groups): train move with group, if possible

        Returns:
            bool: True, if moving train was successful, else False
        """
        save = self._train_to_station(
            start_station, trains, start_times, start_stations, groups)
        return save

    def remove_passing_station_trains(self, start_station: Station, trains: List[Train],
                                      start_times: List[int]) -> None:
        """
        Removes all trains from given trains which just pass a specific station from a time

        Args:
            start_station (Station): station to check for passing trains
            trains (List[Train]): trains to check
            start_times (List[int]): start time of the trains

        Returns:
            None
        """
        capacities = self.stationlist.stations[start_station.id]
        i = 0
        for train in trains:
            for capacity in capacities:
                for _train_in_station in capacity:
                    if train == _train_in_station.train:
                        if start_times[i] <= _train_in_station.arrive_train_time:
                            if _train_in_station.arrive_train_time == _train_in_station.passenger_in_train_time:
                                trains.remove(train)
                                start_times.pop(i)
            i += 1
        return

    def check_capacity(self, trains: List[Train], group_size: int, start_times: List[int],
                       start_stations: List[Station]) -> bool:
        """
        Checks capacity of given trains and removes them if they have an invalid capacity

        Args:
            trains (List[Train]): trains to check
            group_size (int): min capacity a train should have
            start_times (List[int]): start times of the trains
            start_stations (List[Station]): start stations of the trains

        Returns:
            bool: True, if at least one train with valid capacity was found, else False
        """
        b_capacity = False
        if len(trains) != 0:
            i = 0
            while True:
                if trains[i].capacity < group_size:
                    start_times.pop(i)
                    trains.pop(i)
                    if start_stations is not None:
                        start_stations.pop(i)
                else:
                    i += 1
                    b_capacity = True
                if i >= len(trains):
                    break
        return b_capacity

    def check_trains_in_all_station(self, include_not_in_station_trains=True) -> Tuple[
            List[int], List[Train], List[Station]]:
        """
        Retrieves trains of all stations of the whole plan

        Args:
            include_not_in_station_trains (bool, optional): True, if also trains with no start station should be included/checked for starting at a station. Defaults to True.

        Returns:
            Tuple[List[int], List[Train], List[Station]]: start times of the valid trains, valid trains, starst stations of the valid trains
        """
        trains = []
        start_times = []
        start_stations = []
        for i in range(1, len(self.stationlist.stations)):
            start_time, train, station = self.stationlist.read_trains_from_station(
                i, include_not_in_station_trains)
            for t in train:
                trains.append(t)
            for s in start_time:
                start_times.append(s)
                start_stations.append(station)

        return start_times, trains, start_stations

    def get_trains_with_limit_by_start_time_and_speed(self, trains: List[Train], start_times: List[int],
                                                      start_stations: List[Station], limit: int) -> Tuple[
            List[Train], List[int], List[Station]]:
        """
        Calculates the fastest/earliest trains under a limit for moving over an average route

        Args:
            trains (List[Train]): trains
            start_times (List[int]): start times of the trains
            start_stations (List[Station]): start stations of the trains
            limit (int): limits the returning trains

        Returns:
            Tuple[List[Train],List[int],List[Station]]: fastest/earlist trains, start times, start stations
        """
        trains_limit = []
        station_times_limit = []
        start_stations_limit = []
        average_path_length = (
            (len(self.station_input_list) - 1) / 2) * self.average_line_length
        average_times_train_arriving = []
        for i in range(len(trains)):
            average_times_train_arriving.append(
                [trains[i], start_times[i], start_stations[i],
                 start_times[i] + (average_path_length / trains[i].speed)])

        average_times_train_arriving.sort(key=lambda time_train: time_train[3])

        for i in range(limit):
            trains_limit.append(average_times_train_arriving[i][0])
            station_times_limit.append(average_times_train_arriving[i][1])
            start_stations_limit.append(average_times_train_arriving[i][2])

        return trains_limit, station_times_limit, start_stations_limit

    @staticmethod
    def determine_trains_limit(stations_amount: int) -> int:
        """
        Determines/sets the limit of calling trains by the amount of stations
        Used for optimizing the whole calculation time

        Args:
            stations_amount (int): amount of stations in the plan

        Returns:
            int: limit of calling trains
        """
        if stations_amount < 50:
            return 50
        elif stations_amount < 100:
            return 6
        elif stations_amount < 150:
            return 4
        elif stations_amount < 200:
            return 2
        elif stations_amount < 250:
            return 1
        else:
            return 1

    def _train_to_station(self, end_station: Station, trains: List[Train], start_times: List[int],
                          start_stations: List[Station], groups: Groups) -> bool:
        """
        Moves the fastest train by given trains and start times to a specific station
        Used as a helper function

        Args:
            start_station (Station): station to move the fastest train
            trains (List[Train]): possible trains
            start_times (List[int]): start times of the trains
            start_stations (List[Station]): start stations of the trains
            groups (Groups): train move with group, if possible

        Returns:
            bool: True, if moving train was successful, else False
        """
        travels = []
        trains_to_call = trains
        calling_trains_limit = Travel_Center.determine_trains_limit(
            len(self.stationlist.stations))

        if calling_trains_limit >= len(trains):
            calling_trains_limit = len(trains)
        else:
            trains_to_call, start_times, start_stations = self.get_trains_with_limit_by_start_time_and_speed(
                trains, start_times, start_stations, calling_trains_limit)

        for i in range(calling_trains_limit):
            start = start_stations[i]
            train = trains_to_call[i]
            start_time = start_times[i]
            travels.append(self.time_count_train(
                start, end_station, train, start_time))

        self.determine_and_save_shortest_travel(
            travels, groups, None)

        return True
