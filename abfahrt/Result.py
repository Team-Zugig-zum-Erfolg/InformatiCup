"""
    This is Result for registering, saving and printing the output
"""
from typing import List
# This module provides runtime support for type hints. The most fundamental support consists of the types Any, Union, Callable, TypeVar, and Generic. For a full specification, please see PEP 484. For a simplified introduction to type hints, see PEP 483. (https://docs.python.org/3/library/typing.html)

import time
# This module provides various time-related functions. For related functionality, see also the datetime and calendar modules. (https://docs.python.org/3/library/time.html)

import os
# This module provides a portable way of using operating system dependent functionality. If you just want to read or write a file see open(), if you want to manipulate paths, see the os.path module, and if you want to read all the lines in all the files on the command line see the fileinput module. For creating temporary files and directories see the tempfile module, and for high-level file and directory handling see the shutil module. (https://docs.python.org/3/library/os.html)

from abfahrt.classes.Passenger import Passenger
from abfahrt.classes.Train import Train
from abfahrt.classes.Station import Station
from abfahrt.Input import Input


class Result:

    def __init__(self, input_instance: Input):
        """
        Intializing Result

        Args:
            input_instance (Input): instance of Input
        """
        self.trains = input_instance.Trains
        self.passengers = input_instance.Passengers

        self.input = input_instance

        self.ids_str_stations = [""] * (len(self.input.str_ids_stations)+1)
        self.ids_str_lines = [""] * (len(self.input.str_ids_lines)+1)
        self.ids_str_trains = [""] * (len(self.input.str_ids_trains)+1)
        self.ids_str_passengers = [""] * (len(self.input.str_ids_passengers)+1)

        for k, i in self.input.str_ids_stations.items():
            self.ids_str_stations[i] = k

        for k, i in self.input.str_ids_lines.items():
            self.ids_str_lines[i] = k

        for k, i in self.input.str_ids_trains.items():
            self.ids_str_trains[i] = k

        for k, i in self.input.str_ids_passengers.items():
            self.ids_str_passengers[i] = k

        self.id_trains: set = set()
        self.id_passengers: set = set()

    def _get_str_by_id_line(self, id: int) -> str:
        return self.ids_str_lines[id]

    def _get_str_by_id_station(self, id: int) -> str:
        return self.ids_str_stations[id]

    def _get_str_by_id_train(self, id: int) -> str:
        return self.ids_str_trains[id]

    def _get_str_by_id_passenger(self, id: int) -> str:
        return self.ids_str_passengers[id]

    def save_train_depart(self, id_train: int, time: int, id_line: int) -> None:
        """
        Find the train in trains[], add this action in its history

        Args:
            id_train (int): id of the train
            time (int): depart time of the train
            id_line (int): id of the line

        Returns:
            None
        """
        # find the train in list, or add one in list
        train = self.trains[id_train-1]
        train.add_depart(time=time, line=self._get_str_by_id_line(id_line))

    def save_train_start(self, id_train: int, time: int, id_station: int) -> None:
        """
        Find the train in trains[], add this action in its history

        Args:
            id_train (int): id of the train
            time (int): time of start
            id_station (int): id of the station

        Returns:
            None
        """
        train = self.trains[id_train-1]
        train.add_start(
            time=time, station=self._get_str_by_id_station(id_station))

    def save_passenger_board(self, id_passenger: int, time: int, id_train: int) -> None:
        """
        Find the passenger in passenger[], add this action in its history

        Args:
            id_passenger (int): id of the passenger
            time (int): time of board
            id_train (int): id of the train

        Returns:
            None
        """
        p = self.passengers[id_passenger-1]
        p.add_board(time=time, train=self._get_str_by_id_train(id_train))

    def save_passenger_detrain(self, id_passenger: int, time: int) -> None:
        """
        Find the passenger in passenger[], add this action in its history

        Args:
            id_passenger (int): id of the passenger
            time (int): time of detrain

        Returns:
            None
        """
        p = self.passengers[id_passenger-1]
        p.add_detrain(time=time)

    # saving methods
    def to_output_text(self) -> str:
        """
        Create the output text

        Returns:
            str: the output text
        """
        result = ""
        for t in self.trains:
            result += f"[Train:{self._get_str_by_id_train(t.id)}]\n"
            result += t.to_str_output()
            result += "\n"
            result += "\n"
        for p in self.passengers:
            result += f"[Passenger:{self._get_str_by_id_passenger(p.id)}]\n"
            result += p.to_str_output()
            result += "\n"
            result += "\n"
        return result

    def to_file_same(self) -> bool:
        """
        Save output to file in SAME file called output.txt

        Returns:
            bool: True if successful, else False
        """
        path = './output.txt'
        try:
            file = open(path, 'w')
        except OSError:
            return False
        with file:
            file.write(self.to_output_text())
            file.close()
            return True
