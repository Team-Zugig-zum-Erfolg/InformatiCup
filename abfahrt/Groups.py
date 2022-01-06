from typing import List
# This module provides runtime support for type hints. The most fundamental support consists of the types Any, Union, Callable, TypeVar, and Generic. For a full specification, please see PEP 484. For a simplified introduction to type hints, see PEP 483. (https://docs.python.org/3/library/typing.html)
from typing import Tuple
# These can be used as types in annotations using [], each having a unique syntax. (https://docs.python.org/3/library/typing.html)

from abfahrt.classes.Station import Station
from abfahrt.classes.Line import Line
from abfahrt.classes.Passenger import Passenger

class Groups:

    def __init__(self, passengers: List[Passenger]):
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
                if route_searched[0].start_station == passenger.start_station and route_searched[0].end_station == passenger.end_station:
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
            group:[Passenger] (List): List of all Passengers in Group

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
            Passenger (List): List of all Passengers
        """      
        if len(self.route) == 0:
            return None
        self.route.sort(key=self._get_min_target_round)
        return self.route[0]

    def passengers_arrive(self, group: List[Passenger]) -> bool:
        """
        Checks if Passengers in Group have arivved

        Args:
            group:[Passenger] (List): List of all Passengers in Group

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
            group:[Passenger] (List): List of all Passengers in Group

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

    def split_group(self, group: List[Passenger]) -> bool:
        """
        Passengers in a Group will be splitted, if possible 

        Args:
            group:[Passenger] (List): List of all Passengers in a Group

        Returns:
           bool: Has splitting worked?, true = splitting worked, false = splitting has not worked
        """  
        
        if group not in self.route:
            return False
        self.route.remove(group)

        passenger_with_max_time = self.get_passenger_with_most_time(group)

        group.remove(passenger_with_max_time)

        first_group = group
        second_group = [passenger_with_max_time]
        if len(first_group) != 0:
            self.route.append(first_group)
        if len(second_group) != 0:
            self.route.append(second_group)
        return True