# This module provides runtime support for type hints. The most fundamental support consists of the types Any, Union, Callable, TypeVar, and Generic. For a full specification, please see PEP 484. For a simplified introduction to type hints, see PEP 483. (https://docs.python.org/3/library/typing.html)
from typing import List

from abfahrt.classes.Station import Station
from abfahrt.classes.Line import Line


class Train:
    # Züge: str(ID) str(Startbahnhof)/* dec(Geschwindigkeit) int(Kapazität)

    id: int = 0
    start_station: Station = None
    speed: float = 0.0
    capacity: int = 0
    history: List[str] = []

    def __init__(self, id: int, start_station: Station, speed: float, capacity: int):
        '''if start_station is *, input value of start_station could be None '''
        self.id = id
        self.start_station = start_station
        self.speed = speed
        self.capacity = capacity
        self.history = []

    def to_list(self):
        return [self.id, self.start_station.id, self.speed, self.capacity]

    def to_str_input(self) -> str:
        if self.start_station.id < 0:
            output = " ".join(
                [self.get_id_str(), "*", str(self.speed), str(self.capacity)])
        else:
            output = " ".join([self.get_id_str(), self.start_station.get_id_str(), str(
                self.speed), str(self.capacity)])
        return output

    def to_str_output(self) -> str:
        output = "\n".join(self.history)
        return output

    def get_id_str(self) -> str:
        ''' get id with T in a string '''
        out = "T" + str(self.id)
        return out

    def add_start(self, time: int, station: str):
        # print(" *-> enter train")
        out = str(time) + " " + "Start" + " " + station
        # print(f" --- train [{self.id}] add start",out)
        # print(" --- ", self.history)
        self.history.insert(0, out)

    def add_depart(self, time: int, line: str):
        # print(" *-> enter train")
        out = str(time) + " " + "Depart" + " " + line
        # print(f" --- train [{self.id}] add depart: ",out)
        # print(" --- history:", self.history)
        self.history.append(out)

    def merge(self, train):
        self.history += train.history

    def get_id(self):
        return self.id

    def set_id(self, id_train):
        if type(id_train) != str:
            return False
        self.id = id_train
        return True

    def set_start_station(self, start_station):
        if type(start_station) != str:
            return False
        self.start_station = start_station
        return True

    def get_start_station(self):
        return self.start_station

    def set_speed(self, speed):
        if type(speed) != float:
            return False
        self.speed = speed
        return True

    def get_speed(self):
        return self.speed

    def set_capacity(self, capacity):
        if type(capacity) != int:
            return False
        self.capacity = capacity
        return True

    def get_capacity(self):
        return self.capacity

    def to_str(self):
        output = " ".join([self.get_id_str(), self.start_station.get_id_str(), str(
            self.get_capacity()), str(self.get_speed())])
        return output

    def __repr__(self):
        output = " ".join([self.get_id_str(), self.start_station.get_id_str(), str(
            self.get_capacity()), str(self.get_speed())])
        return output

    def __eq__(self, other):
        if (isinstance(other, Train)):
            return self.id == other.id and self.capacity == other.capacity and self.start_station == other.start_station and self.speed == other.speed
        return False
