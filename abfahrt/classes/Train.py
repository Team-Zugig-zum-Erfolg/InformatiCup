# This module provides runtime support for type hints. The most fundamental support consists of the types Any, Union, Callable, TypeVar, and Generic. For a full specification, please see PEP 484. For a simplified introduction to type hints, see PEP 483. (https://docs.python.org/3/library/typing.html)
from typing import List

from abfahrt.classes.Station import Station
from abfahrt.classes.Line import Line


class Train:

    id: int = 0
    start_station: Station = None
    speed: float = 0.0
    capacity: int = 0
    history: List[str] = []

    def __init__(self, id: int, start_station: Station, speed: float, capacity: int):
        """
        Creating a train

        Args:
            id (int): id
            start_station (Station): start station
            speed (float): speed
            capacity (int): capacity
        """
        self.id = id
        self.start_station = start_station
        self.speed = speed
        self.capacity = capacity
        self.history = []

    def to_list(self):
        """
        Convert to list

        Returns:
            the list of information
        """
        return [self.id, self.start_station.id, self.speed, self.capacity]

    def to_str_input(self) -> str:
        """
        This method is used for input, generate information of one passenger

        Returns:
            output: string of information
        """
        if self.start_station.id < 0:
            output = " ".join(
                [self.get_id_str(), "*", str(self.speed), str(self.capacity)])
        else:
            output = " ".join([self.get_id_str(), self.start_station.get_id_str(), str(
                self.speed), str(self.capacity)])
        return output

    def to_str_output(self) -> str:
        """
        Used for output, generate string of it's history

        Returns:
            str: string of information
        """
        output = "\n".join(self.history)
        return output

    def get_id_str(self) -> str:
        """
        Get id with T in a string

        Returns:
            str: train id as string
        """
        out = "T" + str(self.id)
        return out

    def add_start(self, time: int, station: str):
        """
        Add this action in history

        Args:
            time (int): start time
            station (str): starting station
        """
        out = str(time) + " " + "Start" + " " + station
        self.history.insert(0, out)

    def add_depart(self, time: int, line: str):
        """
        Add this action in history

        Args:
            time (int): depart time
            line (str): the line it goes
        """
        out = str(time) + " " + "Depart" + " " + line
        self.history.append(out)

    def merge(self, train):
        """
        Merge history of two train together (they should have same id)

        Args:
            train (Train): another train
        """
        self.history += train.history

    def get_id(self):
        """
        Get the id of the train

        Returns:
            int: id of the train
        """
        return self.id

    def set_id(self, id_train):
        """
        Set the id of the train

        Args:
            id_train (int): id to set

        Returns:
            bool: True, if successful, else False
        """
        if type(id_train) != str:
            return False
        self.id = id_train
        return True

    def set_start_station(self, start_station: Station):
        """
        Set the start station of the train

        Args:
            start_station (Station): start station to set

        Returns:
            bool: True, if successful set, else False
        """
        if not isinstance(start_station, Station):
            return False
        self.start_station = start_station
        return True

    def get_start_station(self):
        """
        Get the start station of the train

        Returns:
            Station: the start station
        """
        return self.start_station

    def set_speed(self, speed: float):
        """
        Set the speed of the train

        Args:
            speed (float): speed to set

        Returns:
            bool: True, if set was successful, else False
        """
        if type(speed) != float:
            return False
        self.speed = speed
        return True

    def get_speed(self):
        """
        Get the speed of the train

        Returns:
            float: the speed of the train
        """
        return self.speed

    def set_capacity(self, capacity: int):
        """
        Set the capacity of the train

        Args:
            capacity (int): capacity to set

        Returns:
            bool: True, if set was successful, else False
        """
        if type(capacity) != int:
            return False
        self.capacity = capacity
        return True

    def get_capacity(self):
        """
        Get the capacity of the train

        Returns:
            int: the capacity of the train
        """
        return self.capacity

    def to_str(self):
        """
        Get the train as string

        Returns:
            str: train as string
        """
        output = " ".join([self.get_id_str(), self.start_station.get_id_str(), str(
            self.get_capacity()), str(self.get_speed())])
        return output

    def __repr__(self):
        """
        Representing train as string

        Returns:
            str: train as string
        """
        output = " ".join([self.get_id_str(), self.start_station.get_id_str(), str(
            self.get_capacity()), str(self.get_speed())])
        return output

    def __eq__(self, other):
        """
        Compares the train with an other train

        Args:
            other (Train): other train to compare

        Returns:
            bool: True, if trains are equal, else False
        """
        if (isinstance(other, Train)):
            return self.id == other.id and self.capacity == other.capacity and self.start_station == other.start_station and self.speed == other.speed
        return False
