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
        self.star_station = Station(
            id=-1, capacity=sys.maxsize)   # the "*" station
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

    def check_station(self, parameters: List) -> bool:
        ''' used in parse_lines(), check logic and syntax of input station
        regulation:
            1. if it contains less or more parameter then the format (int)ID, (int)capacity
            2. if format of id is not "S1", like "asdad123asdasd", or "station1"
            3. if capacity < 0
            4. p[1] is int
        '''
        if len(parameters) != 2:
            # print("parameter < 2")
            return False

        if parameters[0][0] != "S":
            # print("first letter not S")
            return False
        if not parameters[0][1:].isdigit():
            print(parameters[0][1:])
            # print("not number")
            return False

        if not parameters[1].isdigit():
            # print("capacity not number")
            return False
        if _string_to_int(parameters[1]) < 0:
            # print("wrong capacity")
            return False
        return True

    def check_line(self, parameters: List) -> bool:
        ''' used in parse_lines(), check logic and syntax of input line
        [0]str(ID) [1]str(Anfang) [2]str(Ende) [3]dec(Länge) [4]int(Kapazität)
        regulation:
            1. if the parameters less or more than 5
            2. if the id not in format "L1"
            3. if the id of stations not in format "S1"
            4. if the starting and end station not exist
            5. if length < 0
            6. if capacity < 0
            7. if length is not double
            8. if capacity is not int
        '''
        if len(parameters) != 5:
            # print("parameter < 5")
            return False
        if parameters[0][0] != "L":
            # print("first letter not L")
            return False

        if not parameters[0][1:].isdigit():
            # print(parameters[0][1:])
            # print("L1 not number")
            return False

        if parameters[1][0] != "S":
            # print("start station not S")
            return False
        if not parameters[1][1:].isdigit():
            # print(parameters[1][1:])
            # print("start station not number")
            return False

        if parameters[2][0] != "S":
            # print("end station not S")
            return False
        if not parameters[2][1:].isdigit():
            # print(parameters[2][1:])
            # print("end station not number")
            return False

        if self.find_station(_string_to_int(parameters[1])) == None:
            # print("station not exist")
            return False
        if self.find_station(_string_to_int(parameters[2])) == None:
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

    def check_train(self, parameters: List) -> bool:
        ''' used in parse_lines(), check logic and syntax of input train
        0 str(ID) 1 str(Startbahnhof)/* 2 dec(Geschwindigkeit) 3 int(Kapazität)
        regulation:
            1. if the parameters less or more than 4
            2. if the id not in format "T1"
            3. if the id of station not in format "S1" or not "*"
            4. if the station does not exist
            5. if speed < 0
            6. if capacity < 0
        '''
        if len(parameters) != 4:
            # print("parameter < 4")
            return False

        if parameters[0][0] != "T":
            # print("first letter not T")
            return False
        if not parameters[0][1:].isdigit():
            # print(parameters[0][1:])
            # print("T1 not number")
            return False

        if parameters[1] != "*":
            if parameters[1][0] != "S" or not parameters[1][1:].isdigit():
                # print("start station not S or not number or not *")
                return False
            else:
                if self.find_station(_string_to_int(parameters[1])) == None:
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

    def check_passenger(self, parameters: List) -> bool:
        ''' used in parse_lines(), check logic and syntax of input passenger
        0 str(ID) 1 str(Startbahnhof) 2 str(Zielbahnhof) 3 int(Gruppengröße) 4 int(Ankunftszeit)
        regulation:
            1. if the parameters less or more than 5
            2. if the id not in format "P1"
            3. if the id of stations not in format "S1"
            4. if the stations does not exist
            5. if size < 0
            6. if time < 0
            7. size int
            8. time int
        '''
        if len(parameters) != 5:
            # print("parameter < 5")
            return False
        if parameters[0][0] != "P":
            # print("first letter not P")
            return False
        if not parameters[0][1:].isdigit():
            # print(parameters[0][1:])
            # print("P1 not number")
            return False

        if parameters[1][0] != "S":
            # print("start station not S")
            return False
        if not parameters[1][1:].isdigit():
            # print(parameters[1][1:])
            # print("start station not number")
            return False
        if parameters[2][0] != "S":
            # print("end station not S")
            return False
        if not parameters[2][1:].isdigit():
            # print(parameters[2][1:])
            # print("end station not number")
            return False
        if self.find_station(_string_to_int(parameters[1])) == None:
            return False
        if self.find_station(_string_to_int(parameters[2])) == None:
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
        ''' check the logic of all input
        regulation:
            1. if there are only 1 station or no line
            software will be stop
        Note:
            1. if the stations, that are used in lines, don't exist
            2. if the stations, that are used in trains, don't exist
            3. if the stations, that are used in passengers, don't exist
            the line, train and passenger will not be added in input.

        '''
        if len(self.Stations) < 2:
            return False

        if len(self.Lines) < 1:
            return False

        if len(self.Trains) < 1:
            return False

        return True

    def parse_lines(self, lines: list):
        ''' this is used in from_input(), from_input_stdin() to parse a line read from file or stdin. The lines here means a list of line from text'''
        i = 0
        while(i < len(lines)-1):
            if lines[i] == ("[Stations]"):
                while(True):
                    if("" == lines[i+1]) or ('[Lines]' in lines[i+1]) or ('[Stations]' in lines[i+1]) or ('[Trains]' in lines[i+1]) or ('[Passengers]' in lines[i+1]):
                        break
                    i += 1
                    parameters = lines[i].split(" ")
                    if self.check_station(parameters):
                        self.add_station(
                            id=parameters[0], capacity=parameters[1])

            if lines[i] == ("[Lines]"):
                while(True):
                    if("" == lines[i+1]) or ('[Lines]' in lines[i+1]) or ('[Stations]' in lines[i+1]) or ('[Trains]' in lines[i+1]) or ('[Passengers]' in lines[i+1]):
                        break
                    i += 1
                    parameters = lines[i].split(" ")
                    if self.check_line(parameters):
                        self.add_line(id=parameters[0], start_id=parameters[1],
                                      end_id=parameters[2], length=parameters[3], capacity=parameters[4])

            if lines[i] == ("[Trains]"):
                while(True):
                    if("" == lines[i+1]) or ('[Lines]' in lines[i+1]) or ('[Stations]' in lines[i+1]) or ('[Trains]' in lines[i+1]) or ('[Passengers]' in lines[i+1]):
                        break
                    i += 1
                    parameters = lines[i].split(" ")
                    if self.check_train(parameters):
                        self.add_train(
                            id=parameters[0], start_id=parameters[1], speed=parameters[2], capacity=parameters[3])

            if lines[i] == ("[Passengers]"):
                while(True):
                    if("" == lines[i+1]) or ('[Lines]' in lines[i+1]) or ('[Stations]' in lines[i+1]) or ('[Trains]' in lines[i+1]) or ('[Passengers]' in lines[i+1]):
                        break
                    i += 1
                    parameters = lines[i].split(" ")
                    if self.check_passenger(parameters):
                        self.add_passenger(id=parameters[0], start_id=parameters[1],
                                           end_id=parameters[2], size=parameters[3], target=parameters[4])

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


def _isDouble(string: str) -> bool:
    ''' check if string is double '''
    s = string.split('.')
    if len(s) > 2:
        return False
    else:   # [].[] or []
        for si in s:
            if not si.isdigit():
                return False
        return True
