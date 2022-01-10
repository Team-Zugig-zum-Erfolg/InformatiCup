"""
    This is Groups for managing and sorting the passengers
"""
from typing import List
# This module provides runtime support for type hints. The most fundamental support consists of the types Any, Union, Callable, TypeVar, and Generic. For a full specification, please see PEP 484. For a simplified introduction to type hints, see PEP 483. (https://docs.python.org/3/library/typing.html)
from typing import Tuple
# These can be used as types in annotations using [], each having a unique syntax. (https://docs.python.org/3/library/typing.html)

from abfahrt.classes.Station import Station
from abfahrt.classes.Line import Line
from abfahrt.classes.Passenger import Passenger


class Groups:

    def __init__(self, passengers: List[Passenger]):
        """
        Initializing Groups
        """
        self.route = []
        if type(passengers) != list:
            return
        self.max_size = 0
        for passenger in passengers:
            route_number = 0
            added = 0
            if self.max_size < passenger.group_size:
                self.max_size = passenger.group_size
            for route_searched in self.route:
                if route_searched[0].start_station == passenger.start_station and \
                        route_searched[0].end_station == passenger.end_station:
                    self.route[route_number].append(passenger)
                    added = 1
                    break
                route_number += 1
            if added == 0:
                self.route.append([passenger])

    def _get_min_target_round(self, group: List[Passenger]) -> int:
        """
        Get the first arrival Time of the Passengers in a Group

        Args:
            group: List[Passenger] (list): List of all Passengers in Group

        Returns:
           int: smallest Target Round
        """
        min = -1
        for pa in group:
            if min == -1:
                min = pa.target_time
                continue
            if pa.target_time < min:
                min = pa.target_time
        return min

    def get_priority(self) -> List[Passenger]:
        """
        Get the arrival time sorted from all Passengers 

        Returns:
            Passenger (list): List of all Passengers
        """
        if len(self.route) == 0:
            return None
        self.route.sort(key=self._get_min_target_round)
        return self.route[0]

    def passengers_arrive(self, group: List[Passenger]) -> bool:
        """
        Checks if Passengers in Group have arivved

        Args:
            group: List[Passenger] (list): List of all Passengers in Group

        Returns:
            bool: status Passenger arrived?, true = have arrived, false = haven't arrived
        """
        if group not in self.route:
            return False
        self.route.remove(group)
        return True

    def get_passenger_with_most_time(self, group: List[Passenger]) -> Passenger:
        """
        Get the Passenger from Group with the latest arrival Time

        Args:
            group: List[Passenger] (list): List of all Passengers in Group

        Returns:
           int: largest Target Round
        """
        if len(group) == 0:
            return None
        passenger_max_time = group[0]
        for passenger in group:
            if passenger.target_time > passenger_max_time.target_time:
                passenger_max_time = passenger
        return passenger_max_time

    def split_group(self, group: List[Passenger], train_capacity_in_station: int, max_train_capacity: int) -> bool:
        """
        Passengers in a Group will be splitted, if possible 

        Args:
            group: List[Passenger] (list): List of all Passengers in Group
            train_capacity_in_station (int): Train's Capacity in current Station
            max_train_capacity (int): Largest Capacity among the Trains

        Returns:
           bool: Has splitting worked?, true = splitting worked, false = splitting has not worked
        """

        if group not in self.route:
            return False
        self.route.remove(group)
        first_passenger_group = group[0]
        if first_passenger_group.group_size <= train_capacity_in_station:
            capacity = train_capacity_in_station
        elif first_passenger_group.group_size <= max_train_capacity:
            capacity = max_train_capacity
        else:
            capacity = first_passenger_group.group_size
        capacity_count = 0
        first_group = []
        second_group = []
        group.sort(key=lambda x: x.target_time)
        for passenger in group:
            if passenger.group_size <= capacity - capacity_count:
                first_group.append(passenger)
                capacity_count += passenger.group_size
            else:
                second_group.append(passenger)

        if len(first_group) != 0:
            self.route.append(first_group)
        if len(second_group) != 0:
            self.route.append(second_group)
        return True

    def group_choose(self, start_station: Station, end_station: Station, train_capacity: int) -> Tuple[
            bool, List[Passenger]]:
        """
        Determining the group of passengers with the starting station and the ending station, if possible

        Args:
            start_station (Station): start station
            end_station (Station): end station
            train_capacity (int): train's capacity

        Returns:
            Tuple[bool, List[Passenger]]: Has a group? (true = yes, false = no), passengers (true -> group, false -> None)
        """
        choose_group = []
        group_size = 0
        for group in self.route:
            if group[0].start_station == start_station and group[0].end_station == end_station:
                choose_group = group
                break
        if choose_group is None:
            return [False, None]
        else:
            choose_group.sort(key=lambda x: x.target_time)
            for passenger in choose_group:
                group_size = group_size + passenger.group_size
            if group_size > train_capacity:
                if len(choose_group) > 1:
                    self.split_group(
                        choose_group, train_capacity, train_capacity)
                    return self.group_choose(start_station, end_station, train_capacity)
                else:
                    return [False, None]
            else:
                return [True, choose_group]
