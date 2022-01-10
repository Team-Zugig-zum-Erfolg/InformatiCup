from typing import List
# This module provides runtime support for type hints. The most fundamental support consists of the types Any, Union, Callable, TypeVar, and Generic. For a full specification, please see PEP 484. For a simplified introduction to type hints, see PEP 483. (https://docs.python.org/3/library/typing.html)

from abfahrt.classes.Station import Station


class Passenger:

    id: int = 0
    start_station: Station = None
    end_station: Station = None
    group_size: int = 0
    target_time: int = 0

    action_board_time: int = 0
    action_arrive_time: int = 0
    action_train: str = ""

    history: List[str] = []

    def __init__(self, id: int, start_station: Station, end_station: Station, group_size: int, target_time: int):
        """
        Creating a passenger

        Args:
            id (int): id
            start_station (Station): start station
            end_station (Station): end station
            group_size (int): group size
            target_time (int): expected target time
        """
        self.id = id
        self.start_station = start_station
        self.end_station = end_station
        self.group_size = group_size
        self.target_time = target_time
        self.history = []

    def to_list(self) -> list:
        """
        Convert to list

        Returns:
            list: the list of information/parameters
        """
        return [self.id, self.start_station.id, self.end_station.id, self.group_size, self.target_time]

    def to_str_input(self) -> str:
        """
        This method is used for input, generate information of one passenger

        Returns:
            str: string of information/parameters
        """
        output = " ".join([self.get_id_str(), self.start_station.get_id_str(
        ), self.end_station.get_id_str(), str(self.group_size), str(self.target_time)])
        return output

    def to_str_output(self) -> str:
        """
        Used for output, generate string of it's history

        Returns:
            str: string of information for output
        """
        output = "\n".join(self.history)
        return output

    def add_board(self, time: int, train: str):
        """
        Add this action in history

        Args:
            time (int): board time
            train (str): train
        """
        out = str(time) + " " + "Board" + " " + train
        self.history.append(out)

    def add_detrain(self, time: int):
        """
        Add this action in history

        Args:
            time (int): detrain time
        """
        out = str(time) + " " + "Detrain"
        self.history.append(out)

    def merge(self, passenger):
        """
        Merge history of two passengers together (they should have same id)

        Args:
            passenger (Passenger): another passenger
        """
        self.history += passenger.history

    def get_id_str(self) -> str:
        """
        Get the str(id) with P

        Returns:
            str: string of id
        """
        out = "P" + str(self.id)
        return out

    def get_id(self):
        """
        Get the int(id)

        Returns:
            int: int of id
        """
        return self.id

    def set_id(self, id_passenger: int):
        """
        Set id of passenger

        Args:
            id_passenger (int): Id of passenger

        Returns:
            bool: id_passenger is from type int?, true = Type int, false = Type is false
        """
        if type(id_passenger) != int:
            return False
        self.id = id_passenger
        return True

    def get_start_station(self):
        """
        Get start station of passenger

        Returns:
            start (Station): Boarding station
        """    
        return self.start_station

    def set_start_station(self, start_station: Station):
        """
        set start station of passenger

        Args:
            start (Station): first station to board

        Returns:
            bool: start is instance of Station?, true = Type is correct, false = Type is false
        """        
        if (isinstance(start_station, Station) == False):
            return False
        self.start_station = start_station
        return True

    def get_end_station(self):
        """
        Get end station of passenger

        Returns:
            end (Station): end station to deboard
        """   
        return self.end_station

    def set_end_station(self, end_station: Station):
        """
        set end station

        Args:
            end (Station): end station to deboard

        Returns:
            bool: end is instance of Station?, true = Type is correct, false = Type is false
        """     
        if (isinstance(end_station, Station) == False):
            return False
        self.end_station = end_station
        return True

    def get_group_size(self):
        """
        get group size of passengers

        Returns:
            int: returns group size
        """
        return self.group_size

    def set_group_size(self, size):
        """
        set group size

        Args:
            size (int): size of passenger group

        Returns:
            bool: size is from type int?, true = Type is correct, false = Type is false
        """    
        if type(size) != int:
            return False
        self.group_size = size
        return True

    def set_target_round(self, target_round):
        """
        [summary]

        Args:
            target_round ([type]): [description]

        Returns:
            [type]: [description]
        """
        if type(target_round) != int:
            return False
        self.target_time = target_round
        return True

    def get_target_round(self):
        """
        get target round of passengers

        Returns:
            int: returns target round
        """
        return self.target_time

    def __repr__(self):
        """
        representation of object Passenger ( can be used for print)

        Returns:
            string: string from object
        """   
        output = " ".join([self.get_id_str(), self.get_start_station().get_id_str(
        ), self.get_end_station().get_id_str(), str(self.get_group_size()), str(self.get_target_round())])
        return output

    def __eq__(self, other):
        """
        chek if both objects are equal.

        Args:
            other (object): unknown object

        Returns:
            bool: other is equal to Passenger?, true = Type is correct, false = Type is false
        """            
        if (isinstance(other, Passenger)):
            return self.id == other.id and self.group_size == other.group_size and self.start_station == other.start_station and self.end_station == other.end_station and self.target_time == other.target_time
        return False
