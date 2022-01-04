# This module provides runtime support for type hints. The most fundamental support consists of the types Any, Union, Callable, TypeVar, and Generic. For a full specification, please see PEP 484. For a simplified introduction to type hints, see PEP 483. (https://docs.python.org/3/library/typing.html)
from typing import List

# This module provides various time-related functions. For related functionality, see also the datetime and calendar modules. (https://docs.python.org/3/library/time.html)
import time

# This module provides regular expression matching operations similar to those found in Perl. (https://docs.python.org/3/library/re.html)
import re

# This module provides access to some variables used or maintained by the interpreter and to functions that interact strongly with the interpreter. (https://docs.python.org/3/library/sys.html)
import sys


from abfahrt.classes.Station import Station
from abfahrt.classes.Line import Line
from abfahrt.classes.Passenger import Passenger
from abfahrt.classes.Train import Train
from abfahrt.Generator import Generator


class Input:

    def __init__(self):
        self.star_station = Station(id=-1, capacity=999)   # the "*" station
        self.Stations: List["Station"] = []
        self.Lines: List["Line"] = []
        self.Trains: List["Train"] = []
        self.Passengers: List["Passenger"] = []
        self.Generator = Generator()

    def get_star_station(self):
        ''' return the assumed station for the star-train '''
        return self.star_station

    def find_station(self, id) -> Station:
        ''' return a station with id if it exist. if not exist yet, return None'''
        find = list(filter(lambda t: t.id == id, self.Stations))
        if(len(find) > 0):
            return find[0]  # assume there are no duplications
        else:
            return None

    def find_line(self, id) -> Line:
        ''' return a line with id if it exist. if not exist yet, return None'''
        find = list(filter(lambda t: t.id == id, self.Lines))
        if(len(find) > 0):
            return find[0]  # assume there are no duplications
        else:
            return None

    def find_train(self, id) -> Train:
        ''' return a train with id if it exist. if not exist yet, return None'''
        find = list(filter(lambda t: t.id == id, self.Trains))
        if(len(find) > 0):
            return find[0]  # assume there are no duplications
        else:
            return None

    def find_passenger(self, id) -> Passenger:
        ''' return a passenger with id if it exist. if not exist yet, return None'''
        find = list(filter(lambda t: t.id == id, self.Passengers))
        if(len(find) > 0):
            return find[0]  # assume there are no duplications
        else:
            return None

    def add_station(self, id: str, capacity: str):
        ''' this method is used in parse_lines(), add a station to member attribute Stations '''
        id = _string_to_int(id)
        station = self.find_station(id)
        if not station:  # a station is not founded
            self.Stations.append(Station(id=id, capacity=int(capacity)))

    def add_line(self, id: str, start_id: str, end_id: str, length: str, capacity: str):
        ''' this method is used in parse_lines(), add a line to member attribute Lines '''
        id = _string_to_int(id)
        line = self.find_line(id)
        if not line:
            self.Lines.append(Line(id=id, start=self.find_station(_string_to_int(start_id)), end=self.find_station(
                _string_to_int(end_id)), length=float(length), capacity=int(capacity)))

    def add_train(self, id: str, start_id: str, speed: str, capacity: str):
        ''' this method is used in parse_lines(), add a train to member attribute Trains '''
        id = _string_to_int(id)
        train = self.find_train(id)
        if not train:           # there are no such train duplicated
            if start_id == "*":  # a star train
                self.Trains.append(Train(id=id, start_station=self.star_station, speed=float(
                    speed), capacity=int(capacity)))
            else:               # a normal train
                self.Trains.append(Train(id=id, start_station=self.find_station(
                    _string_to_int(start_id)), speed=float(speed), capacity=int(capacity)))

    def add_passenger(self, id: str, start_id: str, end_id: str, size: str, target: str):
        ''' this method is used in parse_lines(), add a passenger to member attribute Passengers '''
        id = _string_to_int(id)
        passenger = self.find_passenger(id)
        if not passenger:
            # assume station and station already wrote in [station] section
            self.Passengers.append(Passenger(id=id, start_station=self.find_station(_string_to_int(
                start_id)), end_station=self.find_station(_string_to_int(end_id)), group_size=int(size), target_time=int(target)))

    def from_generator(self):
        ''' generate a random input instance from Generator'''
        output = self.Generator.random_input_generate_as_classes()
        return output

    def from_stdin(self):
        ''' read input from stdin '''
        lines = sys.stdin.readlines()
        mylines = []  # Declare an empty list.

        for line in lines:  # For each line in the file,
            mylines.append(line.rstrip('\n'))  # strip newline and add to list.
        mylines.append("")
        # print(mylines)
        return self.parse_lines(mylines)

    def to_input_text(self) -> str:
        ''' return a string of input in format '''
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
        ''' save input format in local file '''
        state = False
        file = open(path, 'w')
        file.write(self.to_input_text())
        file.close()
        state = True
        return state

    def path_generator(self) -> str:
        ''' generate a path for local file '''
        filename = "Input-" + \
            time.strftime("%y%m%d-%H%M%S",
                          time.localtime(time.time())) + ".txt"
        return filename

    def from_file(self, path: str):
        ''' load input from local file '''
        mylines = []  # Declare an empty list.
        # Open lorem.txt for reading text.
        with open(path, "rt") as myfile:
            for myline in myfile:  # For each line in the file,
                # strip newline and add to list.
                mylines.append(myline.rstrip('\n'))
            mylines.append("")
        return self.parse_lines(mylines)

    def parse_lines(self, lines: list):
        ''' this is used in from_input(), from_input_stdin() to parse a line read from file or stdin'''
        i = 0
        while(i < len(lines)-1):
            if lines[i] == ("[Stations]"):
                while(True):
                    i += 1
                    parameters = lines[i].split(" ")
                    self.add_station(id=parameters[0], capacity=parameters[1])
                    if(('#' in lines[i+1]) or ("" == lines[i+1])) or ('[' in lines[i+1]) or (']' in lines[i+1]):
                        break

            if lines[i] == ("[Lines]"):
                while(True):
                    i += 1
                    parameters = lines[i].split(" ")
                    self.add_line(id=parameters[0], start_id=parameters[1],
                                  end_id=parameters[2], length=parameters[3], capacity=parameters[4])
                    if(('#' in lines[i+1]) or ("" == lines[i+1])) or ('[' in lines[i+1]) or (']' in lines[i+1]):
                        break

            if lines[i] == ("[Trains]"):
                while(True):
                    i += 1
                    parameters = lines[i].split(" ")
                    parameters[2] = float(parameters[2])- 0.0000000000000001
                    self.add_train(
                        id=parameters[0], start_id=parameters[1], speed=parameters[2], capacity=parameters[3])
                    if(('#' in lines[i+1]) or ("" == lines[i+1])) or ('[' in lines[i+1]) or (']' in lines[i+1]):
                        break

            if lines[i] == ("[Passengers]"):
                while(True):
                    i += 1
                    parameters = lines[i].split(" ")
                    self.add_passenger(id=parameters[0], start_id=parameters[1],
                                       end_id=parameters[2], size=parameters[3], target=parameters[4])
                    if(('#' in lines[i+1]) or ("" == lines[i+1])) or ('[' in lines[i+1]) or (']' in lines[i+1]):
                        break
                break
            i += 1
        return self.Stations, self.Lines, self.Trains, self.Passengers

    def print_input(self):
        ''' print information of input '''
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
    ''' convert from string to int, like S1 -> 1'''
    r = re.findall('\d+', string)
    if (len(r) > 0):
        return int(r[0])
    else:
        return 0
