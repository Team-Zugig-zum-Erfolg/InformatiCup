"""
    This is Input for parsing and reading the input from stdin or a file or generator
"""
from typing import List
from typing import Tuple
# This module provides runtime support for type hints. The most fundamental support consists of the types Any, Union, Callable, TypeVar, and Generic. For a full specification, please see PEP 484. For a simplified introduction to type hints, see PEP 483. (https://docs.python.org/3/library/typing.html)

import time
# This module provides various time-related functions. For related functionality, see also the datetime and calendar modules. (https://docs.python.org/3/library/time.html)

import re
# This module provides regular expression matching operations similar to those found in Perl. (https://docs.python.org/3/library/re.html)

import sys
# This module provides access to some variables used or maintained by the interpreter and to functions that interact strongly with the interpreter. (https://docs.python.org/3/library/sys.html)

from abfahrt.classes.Station import Station
from abfahrt.classes.Line import Line
from abfahrt.classes.Passenger import Passenger
from abfahrt.classes.Train import Train
from abfahrt.Generator import Generator


class Input:

    def __init__(self):
        """
        Initializing Input
        """
        self.star_station = Station(
            id=-1, capacity=sys.maxsize)   # the "*" station
        self.Stations: List["Station"] = []
        self.Lines: List["Line"] = []
        self.Trains: List["Train"] = []
        self.Passengers: List["Passenger"] = []
        self.Generator = Generator()

        self.str_ids_stations = {}
        self.str_ids_lines = {}
        self.str_ids_trains = {}
        self.str_ids_passengers = {}

    def get_star_station(self) -> Station:
        """
        Returns the assumed station for the star-train

        Returns:
            Station: a assumed star_station
        """
        return self.star_station

    def _check_station_str(self, name: str, insert=False) -> int:
        if name in self.str_ids_stations:
            return self.str_ids_stations[name]
        elif insert:
            self.str_ids_stations[name] = len(self.str_ids_stations)+1
            return self.str_ids_stations[name]
        return None

    def _check_line_str(self, name: str, insert=False) -> int:
        if name in self.str_ids_lines:
            return self.str_ids_lines[name]
        elif insert:
            self.str_ids_lines[name] = len(self.str_ids_lines)+1
            return self.str_ids_lines[name]
        return None

    def _check_train_str(self, name: str, insert=False) -> int:
        if name in self.str_ids_trains:
            return self.str_ids_trains[name]
        elif insert:
            self.str_ids_trains[name] = len(self.str_ids_trains)+1
            return self.str_ids_trains[name]
        return None

    def _check_passenger_str(self, name: str, insert=False) -> int:
        if name in self.str_ids_passengers:
            return self.str_ids_passengers[name]
        elif insert:
            self.str_ids_passengers[name] = len(self.str_ids_passengers)+1
            return self.str_ids_passengers[name]
        return None

    def find_station(self, id) -> Station:
        """
        Returns a station with id if it exist. if not exist yet, return None

        Args:
            id (int): the id of the station

        Returns:
            Station: the station or None
        """
        find = list(filter(lambda t: t.id == id, self.Stations))
        if(len(find) > 0):
            return find[0]  # assume there are no duplications
        else:
            return None

    def find_line(self, id) -> Line:
        """
        Returns a line with id if it exist. if not exist yet, return None

        Args:
            id (int): id of station

        Returns:
            Line: the line or None
        """
        find = list(filter(lambda t: t.id == id, self.Lines))
        if(len(find) > 0):
            return find[0]  # assume there are no duplications
        else:
            return None

    def find_train(self, id) -> Train:
        """
        Returns a train with id if it exist. if not exist yet, return None
        Args:
            id (int): id of train

        Returns:
            Train: the train or None
        """
        find = list(filter(lambda t: t.id == id, self.Trains))
        if(len(find) > 0):
            return find[0]  # assume there are no duplications
        else:
            return None

    def find_passenger(self, id) -> Passenger:
        """
        Returns a passenger with id if it exist. if not exist yet, return None

        Args:
            id (int): id of passenger

        Returns:
            Passenger: the passenger or None
        """
        find = list(filter(lambda t: t.id == id, self.Passengers))
        if(len(find) > 0):
            return find[0]  # assume there are no duplications
        else:
            return None

    def add_station(self, id: str, capacity: str):
        """
        This method is used in parse_lines(), add a station to member attribute Stations

        Args:
            id (str): id of station
            capacity (str): capacity of station
        """
        id = self._check_station_str(id, True)
        station = self.find_station(id)
        if not station:  # a station is not founded
            self.Stations.append(Station(id=id, capacity=int(capacity)))

    def add_line(self, id: str, start_id: str, end_id: str, length: str, capacity: str):
        """
        This method is used in parse_lines(), add a line to member attribute Lines

        Args:
            id (str): id of line
            start_id (str): the id of the start station
            end_id (str): the id of the end station
            length (str): the length of the line
            capacity (str): capacity of line
        """
        id = self._check_line_str(id, True)
        line = self.find_line(id)
        if not line:
            self.Lines.append(Line(id=id, start=self.find_station(self._check_station_str(start_id)), end=self.find_station(
                self._check_station_str(end_id)), length=float(length), capacity=int(capacity)))

    def add_train(self, id: str, start_id: str, speed: str, capacity: str):
        """
        This method is used in parse_lines(), add a train to member attribute Trains

        Args:
            id (str): id of train
            start_id (str): the id of the start station
            speed (str): the speed of the train
            capacity (str): capacity of train
        """
        id = self._check_train_str(id, True)
        train = self.find_train(id)
        if not train:           # there are no such train duplicated
            if start_id == "*":  # a star train
                self.Trains.append(Train(id=id, start_station=self.star_station, speed=float(
                    speed), capacity=int(capacity)))
            else:               # a normal train
                self.Trains.append(Train(id=id, start_station=self.find_station(
                    self._check_station_str(start_id)), speed=float(speed), capacity=int(capacity)))

    def add_passenger(self, id: str, start_id: str, end_id: str, size: str, target: str):
        """
        This method is used in parse_lines(), add a passenger to member attribute Passengers

        Args:
            id (str): id of passenger
            start_id (str): the id of the start station
            end_id (str): the id of the end station
            size (str): the size of the passenger
            target (str): target time of the passenger
        """
        id = self._check_passenger_str(id, True)
        passenger = self.find_passenger(id)
        if not passenger:
            # assume station and station already wrote in [station] section
            self.Passengers.append(Passenger(id=id, start_station=self.find_station(self._check_station_str(
                start_id)), end_station=self.find_station(self._check_station_str(end_id)), group_size=int(size), target_time=int(target)))

    def from_generator(self) -> list:
        """
        Generates and uses random input from Generator

        Returns:
            list: the generated input
        """
        output = self.Generator.random_input_generate_as_classes()
        return output

    def from_stdin(self) -> list:
        """
        Reads input from STDIN

        Returns:
            list: parsed lines/input
        """
        lines = sys.stdin.readlines()
        mylines = []  # Declare an empty list.

        for line in lines:  # For each line in the file,
            mylines.append(line.rstrip('\n'))  # strip newline and add to list.
        mylines.append("")
        return self.parse_lines(mylines)

    def to_input_text(self) -> str:
        """
        Returns a string of input in format

        Returns:
            str: the output text
        """
        text = "# Bahnhöfe: str(ID) \n [Stations] \n"
        for station in self.Stations:
            text = text + station.to_str_input() + "\n"
        text = text + "\n"

        text = text + \
            "# Strecken: str(ID) str(Anfang) str(Ende) dec(Länge) int(Kapazität)\n"
        text = text + "[Lines]\n"
        for line in self.Lines:
            text = text + line.to_str_input() + "\n"
        text = text + "\n"

        text = text + \
            "# Züge: str(ID) str(Startbahnhof)/* dec(Geschwindigkeit) int(Kapazität)\n"
        text = text + "[Trains]\n"
        for train in self.Trains:
            text = text + train.to_str_input() + "\n"
        text = text + "\n"

        text = text + \
            "# Passagiere: str(ID) str(Startbahnhof) str(Zielbahnhof) int(Gruppengröße) int(Ankunftszeit)\n"
        text = text + "[Passengers]\n"
        for passenger in self.Passengers:
            text = text + passenger.to_str_input() + "\n"
        text = text + "\n"
        # or i can use list, str = "\n".join(list)
        return text

    def to_input_file(self, path: str) -> bool:
        """
        Saves input format in local file

        Returns:
            bool: True if saving file was successful, else False
        """
        try:
            file = open(path, 'w')
        except OSError:
            return False
        with file:
            file.write(self.to_input_text())
            file.close()
            return True

    def path_generator(self) -> str:
        """
        Generates a path for local file: "year month day - hour minute second.txt"

        Returns:
            str: the generated filename
        """
        filename = "Input-" + \
            time.strftime("%y%m%d-%H%M%S",
                          time.localtime(time.time())) + ".txt"
        return filename

    def from_file(self, path: str) -> list:
        """
        Loads input from a local file

        Args:
            path (str): the path of a input file

        Returns:
            list: parsed input of the file
        """
        mylines = []  # Declare an empty list.
        # Open lorem.txt for reading text.
        with open(path, "rt") as myfile:
            for myline in myfile:  # For each line in the file,
                # strip newline and add to list.
                mylines.append(myline.rstrip('\n'))
            mylines.append("")
        return self.parse_lines(mylines)

    def check_station(self, parameters: list) -> bool:
        """
        used in parse_lines(), check logic and syntax of input station

        Args:
            parameters (list): a list of parameters with type str

        Returns:
            bool: True if valid input, else False
        """
        if len(parameters) != 2:
            # print("parameter < 2")
            return False

        if parameters[0][0] == "#":
            # print("first letter not S")
            return False

        if self._check_station_str(parameters[0]):
            return False

        if not parameters[1].isdigit():
            # print("capacity not number")
            return False
        if _string_to_int(parameters[1]) < 0:
            # print("wrong capacity")
            return False
        return True

    def check_line(self, parameters: list) -> bool:
        """
        used in parse_lines(), check logic and syntax of input line
            regulation:
            1. if the parameters less or more than 5
            2. if the id not in format "L1"
            3. if the id of stations not in format "S1"
            4. if the starting and end station not exist
            5. if length < 0
            6. if capacity < 0
            7. if length is not double
            8. if capacity is not int
            -> then false

        Args:
            parameters (list): a list of parameters with type str

        Returns:
            bool: True if valid input, else False
        """
        if len(parameters) != 5:
            # print("parameter < 5")
            return False
        if parameters[0][0] == "#":
            # print("first letter not L")
            return False

        if self._check_line_str(parameters[0]):
            return False

        if self.find_station(self._check_station_str(parameters[1])) == None:
            # print("station not exist")
            return False
        if self.find_station(self._check_station_str(parameters[2])) == None:
            # print("station not exist")
            return False

        if not _isDouble(parameters[3]):  # length should be double
            # print("length not number")
            return False
        if _string_to_int(parameters[3]) < 0:
            # print("length length")
            return False

        if not parameters[4].isdigit():
            # print("capacity not number")
            return False
        if _string_to_int(parameters[4]) < 0:
            # print("wrong capacity")
            return False
        return True

    def check_train(self, parameters: list) -> bool:
        """
        used in parse_lines(), check logic and syntax of input train
        0 str(ID) 1 str(Startbahnhof)/* 2 dec(Geschwindigkeit) 3 int(Kapazität)
        regulation:
            1. if the parameters less or more than 4
            2. if the id not in format "T1"
            3. if the id of station not in format "S1" or not "*"
            4. if the station does not exist
            5. if speed < 0
            6. if capacity < 0
            -> then false

        Args:
            parameters (list): a list of parameters with type str

        Returns:
            bool: True if valid input, else False
        """
        if len(parameters) != 4:
            # print("parameter < 4")
            return False

        if parameters[0][0] == "#":
            # print("first letter not T")
            return False

        if self._check_train_str(parameters[0]):
            return False

        if parameters[1] != "*":
            if self.find_station(self._check_station_str(parameters[1])) == None:
                return False

        # speed should be double
        if not _isDouble(parameters[2]):
            # print("speed not number")
            return False
        if _string_to_int(parameters[2]) < 0:
            # print("wrong speed")
            return False

        if not parameters[3].isdigit():
            # print("capacity not number")
            return False
        if _string_to_int(parameters[3]) < 0:
            # print("wrong capacity")
            return False

        return True

    def check_passenger(self, parameters: list) -> bool:
        """
        Used in parse_lines(), check logic and syntax of input passenger
        0 str(ID) 1 str(Startbahnhof) 2 str(Zielbahnhof) 3 int(Gruppengröße) 4 int(Ankunftszeit)

        Note:
            regulation/checks:
            1. if the parameters less or more than 5
            2. if the id not in format "P1"
            3. if the id of stations not in format "S1"
            4. if the stations does not exist
            5. if size < 0
            6. if time < 0
            7. size not int
            8. time not int

        Args:
            parameters (list): a list of parameters with type str

        Returns:
            bool: True if valid input, else False
        """
        if len(parameters) != 5:
            # print("parameter < 5")
            return False
        if parameters[0][0] == "#":
            # print("first letter not P")
            return False

        if self._check_passenger_str(parameters[0]):
            return False

        if self.find_station(self._check_station_str(parameters[1])) == None:
            return False
        if self.find_station(self._check_station_str(parameters[2])) == None:
            return False

        if not parameters[3].isdigit():
            # print("size not number")
            return False
        if _string_to_int(parameters[3]) < 0:
            # print("wrong size")
            return False

        if not parameters[4].isdigit():
            # print("time not number")
            return False
        if _string_to_int(parameters[4]) < 0:
            # print("wrong time")
            return False

        return True

    def check_input(self) -> bool:
        """
        check the logic of all input
        regulation:
            1. if there are only 1 station or no line
            software will be stop
        Note:
            1. if the stations, that are used in lines, don't exist
            2. if the stations, that are used in trains, don't exist
            3. if the stations, that are used in passengers, don't exist
            -> the line, train and passenger will not be added in input.

        Returns:
            bool: True if valid input, else False
        """

        if len(self.Stations) < 2:
            return False

        if len(self.Lines) < 1:
            return False

        if len(self.Trains) < 1:
            return False

        return True

    def parse_lines(self, lines: list) -> Tuple[List[Station], List[Line], List[Train], List[Passenger]]:
        """
        This is used in from_input(), from_stdin() to parse a line read from file or stdin. The lines here means a list of line from text

        Args: 
            lines (list): the lines readed from file or stdin

        Returns:
            Tuple[List[Station], List[Line], List[Train], List[Passenger]]: a list of readed stations, readed lines, readed trains and readed passengers
        """
        i = 0
        while(i < len(lines)-1):
            if lines[i] == ("[Stations]"):
                while(True):
                    if(i+1 >= len(lines)-1) or ('[Lines]' in lines[i+1]) or ('[Stations]' in lines[i+1]) or ('[Trains]' in lines[i+1]) or ('[Passengers]' in lines[i+1]):
                        break
                    i += 1
                    parameters = lines[i].split(" ")
                    if self.check_station(parameters):
                        self.add_station(
                            id=parameters[0], capacity=parameters[1])
            i += 1

        i = 0
        while(i < len(lines)-1):
            if lines[i] == ("[Lines]"):
                while(True):
                    if(i+1 >= len(lines)-1) or ('[Lines]' in lines[i+1]) or ('[Stations]' in lines[i+1]) or ('[Trains]' in lines[i+1]) or ('[Passengers]' in lines[i+1]):
                        break
                    i += 1
                    parameters = lines[i].split(" ")
                    if self.check_line(parameters):
                        self.add_line(id=parameters[0], start_id=parameters[1],
                                      end_id=parameters[2], length=parameters[3], capacity=parameters[4])
            if lines[i] == ("[Trains]"):
                while(True):
                    if(i+1 >= len(lines)-1) or ('[Lines]' in lines[i+1]) or ('[Stations]' in lines[i+1]) or ('[Trains]' in lines[i+1]) or ('[Passengers]' in lines[i+1]):
                        break
                    i += 1
                    parameters = lines[i].split(" ")
                    if self.check_train(parameters):
                        self.add_train(
                            id=parameters[0], start_id=parameters[1], speed=parameters[2], capacity=parameters[3])
            if lines[i] == ("[Passengers]"):
                while(True):
                    if(i+1 >= len(lines)-1) or ('[Lines]' in lines[i+1]) or ('[Stations]' in lines[i+1]) or ('[Trains]' in lines[i+1]) or ('[Passengers]' in lines[i+1]):
                        break
                    i += 1
                    parameters = lines[i].split(" ")
                    if self.check_passenger(parameters):
                        self.add_passenger(id=parameters[0], start_id=parameters[1],
                                           end_id=parameters[2], size=parameters[3], target=parameters[4])
            i += 1
        return self.Stations, self.Lines, self.Trains, self.Passengers

    def print_input(self):
        """
        Prints information of input
        """
        print("---------------")
        print("| * printing input started ...")
        print(f"| * Stations: [{len(self.Stations)}]")
        for i in range(len(self.Stations)):
            print(f"|   * [{i+1}/{len(self.Stations)}] " +
                  self.Stations[i].to_str_input())

        print(f"| * Lines: [{len(self.Lines)}]")
        for i in range(len(self.Lines)):
            print(f"|   * [{i+1}/{len(self.Lines)}] " +
                  self.Lines[i].to_str_input())

        print(f"| * Trains: [{len(self.Trains)}]")
        for i in range(len(self.Trains)):
            print(f"|   * [{i+1}/{len(self.Trains)}] " +
                  self.Trains[i].to_str_input())

        print(f"| * Passengers: [{len(self.Passengers)}]")
        for i in range(len(self.Passengers)):
            print(f"|   * [{i+1}/{len(self.Passengers)}] " +
                  self.Passengers[i].to_str_input())

        print("| * print input finished")
        print("---------------")
        return


# helper methods
def _string_to_int(string: str) -> int:
    """
    a helper function convert from string to int, like S1 -> 1

    Args: 
        string (str): input string

    Returns:
        (int): return value if this is a int, return 0 if this is not a int 
    """
    r = re.findall('\d+', string)
    if (len(r) > 0):
        return int(r[0])
    else:
        return 0


def _isDouble(string: str) -> bool:
    """
    check if string is double

    Args: 
        string (str): input string

    Returns:
        (bool): true if this is a double (x.x or x) 
    """
    s = string.split('.')
    if len(s) > 2:
        return False
    else:   # [].[] or []
        for si in s:
            if not si.isdigit():
                return False
        return True
