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

    def get_str_by_id_line(self, id):
        return self.ids_str_lines[id]

    def get_str_by_id_station(self, id):
        return self.ids_str_stations[id]

    def get_str_by_id_train(self, id):
        return self.ids_str_trains[id]

    def get_str_by_id_passenger(self, id):
        return self.ids_str_passengers[id]

    def save_train_depart(self, id_train, time, id_line):
        """
        find the train in trains[], add this action in its history

        Args:
            id_train (int): id of the train
            time (int): depart time of the train
            id_line (int): id of the line
        """
        # find the train in list, or add one in list
        train = self.trains[id_train-1]
        train.add_depart(time=time, line=self.get_str_by_id_line(id_line))

    def save_train_start(self, id_train, time, id_station):
        """
        find the train in trains[], add this action in its history

        Args:
            id_train (int): id of the train
            time (int): time of start
            id_station (int): id of the station
        """
        train = self.trains[id_train-1]
        train.add_start(
            time=time, station=self.get_str_by_id_station(id_station))

    def save_passenger_board(self, id_passenger, time, id_train):
        """
        find the passenger in passenger[], add this action in its history

        Args:
            id_passenger (int): id of the passenger
            time (int): time of board
            id_train (int): id of the train
        """
        p = self.passengers[id_passenger-1]
        p.add_board(time=time, train=self.get_str_by_id_train(id_train))

    def save_passenger_detrain(self, id_passenger, time):
        """
        find the passenger in passenger[], add this action in its history

        Args:
            id_passenger (int): id of the passenger
            time (int): time of detrain
        """
        p = self.passengers[id_passenger-1]
        p.add_detrain(time=time)

    def find_or_add_train(self, id_train: int) -> Train:
        """
        find the train in the trains[], if not exist, create one

        Args:
            id_train (int): the id of the train

        Returns:
            train: the found train
        """
        # currently cannot deal with duplication
        if id_train in self.id_trains:                                      # already exist
            find_result = filter(lambda t: t.id == id_train,
                                 self.trains)   # find it
            # convert to list
            found_train = list(find_result)
            if len(found_train) == 1:
                return found_train[0]
            else:   # duplication
                return found_train[0]
        else:   # train not exist, add one
            train = Train(id_train, Station(0, 0), 0.0, 0)  # new train
            self.id_trains.add(id_train)
            self.trains.append(train)
            # sort the trains list
            self.trains.sort(key=lambda x: x.id)

            return train

    def find_or_add_passenger(self, id_passenger: int) -> Passenger:
        """
        find the passenger in the passengers[], if not exist, create one, currently cannot deduplicate

        Args:
            id_passenger (int): the id of the passenger

        Returns:
            passenger: the found passenger
        """
        if id_passenger in self.id_passengers:                                      # already exist
            find_result = filter(
                lambda p: p.id == id_passenger, self.passengers)   # find it
            found_p = list(find_result)
            if len(found_p) == 1:                                                   # found one
                '''found one passenger, already saved in a list'''
                return found_p[0]
            else:                                                                   # found many, duplication!
                # self.handle_duplication_passenger()
                print(
                    f"* <!> [Warning] from Result: there Passenger [{id_passenger}] is duplicated, \n! * there are [{len(found_p)}] such passengers in [passengers]")
                return found_p[0]
        else:   # train not exist, add one
            p = Passenger(id_passenger, None, None, 0, 0)
            self.id_passengers.add(id_passenger)
            self.passengers.append(p)

            # sort the passengers list
            self.passengers.sort(key=lambda x: x.id)

            return p

    def add_passenger(self, passenger: Passenger):
        """
        add a Passanger in list, if already exist(with same id), merge the history
        also save the id in a Set, for easily to check if some exist
        if you need to add a P only with id, please use find_or_add_passenger

        Args:
            passenger (Passenger): a passenger
        """

        if passenger.id in self.id_passengers:          # already exist
            # passenger already exists, only need to merge history
            self.find_or_add_passenger(passenger.id).merge(passenger)
        else:                                           # not exist
            # p not exist, add new one in list
            self.passengers.append(passenger)
            self.id_passengers.add(passenger.id)

            # sort the passengers list
            self.passengers.sort(key=lambda x: x.id)

    def add_train(self, train: Train):
        if train.id in self.id_trains:
            self.find_or_add_train(train.id).merge(train)
        else:
            self.trains.append(train)
            self.id_trains.add(train.id)
            # sort the trains list
            self.trains.sort(key=lambda x: x.id)

    def passengers_add_from_input(self, input: Input):
        """
        from input add all passengers
        """
        for passenger in input.Passengers:
            self.add_passenger(passenger)

    def passengers_read_from_input(self, input: Input):
        """
        directly read all passengers from input.passengers
        """
        self.passengers = input.Passengers

    def train_add_from_input(self, input: Input):
        """
        from input add all passengers
        """
        for train in input.Trains:
            self.add_train(train)

    def train_read_from_input(self, input: Input):
        """
        directly read all passengers from input.passengers
        """
        self.trains = input.Trains

    # saving methods
    def to_output_text(self):
        """
        create the output text

        Returns:
            result: the output text
        """
        result = ""
        for t in self.trains:
            result += f"[Train:{self.get_str_by_id_train(t.id)}]\n"
            result += t.to_str_output()
            result += "\n"
            result += "\n"
        for p in self.passengers:
            result += f"[Passenger:{self.get_str_by_id_passenger(p.id)}]\n"
            result += p.to_str_output()
            result += "\n"
            result += "\n"
        return result

    def to_file_same(self):
        """
        save output file in SAME file output

        Returns:
            state: true if successfully
        """
        path = './output.txt'
        state = False
        file = open(path, 'w')
        file.write(self.to_output_text())
        file.close()
        state = True
        return state

    def to_file(self, folder="result"):
        """
        save output format in local file 

        Args:
            folder: folder: the folder to save this file, default is "result"

        Returns:
            state: true if successfully
        """
        dir_name = str(folder)
        path = self.path_generator(folder=dir_name)
        state = False
        if os.path.isdir(dir_name):
            file = open(path, 'w')
        else:
            os.mkdir(dir_name)
            file = open(path, 'w')
        file.write(self.to_output_text())
        file.close()
        state = True
        return state

    def path_generator(self, folder="result") -> str:
        """
        generate a path for local file: "year month day - hour minute second.txt"

        Returns:
            filename (str): the generated filename
        """
        dir_name = str(folder)
        path = "./" + dir_name + "/Output"
        path = path + "-" + \
            time.strftime("%y%m%d-%H%M%S", time.localtime(time.time()))
        path = path + ".txt"
        return path
