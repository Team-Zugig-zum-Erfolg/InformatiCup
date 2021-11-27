from typing import List
from classes.Station import Station
from classes.Line import Line
from classes.Passenger import Passenger
from classes.Train import Train
import time
import re


class Input:
    star_station = Station(id=-1,capacity=999)   # the "*" station
    Stations: List["Station"] = []
    Lines: List["Line"] = []
    Trains: List["Train"] = []
    Passengers: List["Passenger"] = []

    def get_star_station(self):
        return self.star_station

    def find_station(self, id)->Station:
        # station may be none, if input is *
        find = list(filter(lambda t: t.id == id, self.Stations))
        if(len(find)>0):
            return find[0]  # assume there are no duplications
        else: 
            # print("[Warning] Input.find_station: this station doesn't exist")
            # but what if adding a station?
            # when adding a train, the station doesnt exist, need to print a warnin
            # write a log
            return None

    def find_line(self, id)->Line:
        find = list(filter(lambda t: t.id == id, self.Lines))
        if(len(find)>0):
            return find[0]  # assume there are no duplications
        else: return None

    def find_train(self, id)->Train:
        find = list(filter(lambda t: t.id == id, self.Trains))
        if(len(find)>0):
            return find[0]  # assume there are no duplications
        else: return None

    def find_passenger(self, id)->Passenger:
        find = list(filter(lambda t: t.id == id, self.Passengers))
        if(len(find)>0):
            return find[0]  # assume there are no duplications
        else: return None

    # a more elegent way to add elements
    # input could be all string,
    # check duplication

    def add_station(self, id:str, capacity:str):
        # station: int(ID), int capacity
        id = _string_to_int(id)
        station = self.find_station(id)
        if not station: # a station is not founded
            self.Stations.append(Station(id = id, capacity = int(capacity)))
        # self.if_station_added(id)
        # true: find_station().capacity = xx
        # false: append

    def add_line(self, id:str, start_id:str, end_id:str, length:str, capacity:str):
        id = _string_to_int(id)
        line = self.find_line(id)
        if not line:
            self.Lines.append(Line(id =id, start = self.find_station(_string_to_int(start_id)), end = self.find_station(_string_to_int(end_id)), length = float(length), capacity = int(capacity)))
        # ?? what if the station not exist?

        # Strecken: int(ID) station(Anfang) station(Ende) dec(Länge) int(Kapazität)

    def add_train(self, id:str, start_id:str, speed:str, capacity:str):
        # Züge: int(ID) station(Startbahnhof)/* dec(Geschwindigkeit) int(Kapazität)
        id = _string_to_int(id)
        train = self.find_train(id)
        if not train:           # there are no such train duplicated
            if start_id == "*": # a star train
                self.Trains.append(Train(id=id, start_station= self.star_station, speed = float(speed), capacity = int(capacity)))
            else:               # a normal train
                self.Trains.append(Train(id=id, start_station= self.find_station(_string_to_int(start_id)), speed = float(speed), capacity = int(capacity)))
                # assume that this station exist

    def add_passenger(self, id:str, start_id:str, end_id:str, size:str, target:str):
        # Passagiere: int(ID) station(Startbahnhof) station(Zielbahnhof) int(Gruppengröße) int(Ankunftszeit)
        id = _string_to_int(id)
        passenger = self.find_passenger(id)
        if not passenger:
            # assume station and station already wrote in [station] section
            self.Passengers.append(Passenger(id = id, start_station = self.find_station(_string_to_int(start_id)), end_station = self.find_station(_string_to_int(end_id)), group_size = int(size), target_time =int(target)))

    def if_station_exist():
        pass

    def if_line_exist():
        pass

    def if_train_exist():
        pass

    def if_passenger_exist():
        pass

    def to_input_text(self) -> str:
        ''' return a string of input in format '''
        text = "# Bahnhöfe: str(ID) \n [Stations] \n"
        for station in self.Stations:
            text = text + station.to_str_input() + "\n"
        text = text + "\n"

        text = text + "# Strecken: str(ID) str(Anfang) str(Ende) dec(Länge) int(Kapazität)\n"
        text = text + "[Lines]\n"
        for line in self.Lines:
            text = text + line.to_str_input() + "\n"
        text = text + "\n"

        text = text + "# Züge: str(ID) str(Startbahnhof)/* dec(Geschwindigkeit) int(Kapazität)\n"
        text = text + "[Trains]\n"
        for train in self.Trains:
            text = text + train.to_str_input() + "\n"
        text = text + "\n"

        text = text + "# Passagiere: str(ID) str(Startbahnhof) str(Zielbahnhof) int(Gruppengröße) int(Ankunftszeit)\n"
        text = text + "[Passengers]\n"
        for passenger in self.Passengers:
            text = text + passenger.to_str_input() + "\n"
        text = text + "\n"
        # or i can use list, str = "\n".join(list)
        return text

    def to_input_file(self, path:str) -> bool:
        ''' save input format in local file '''
        state = False
        file = open(path, 'w')  
        file.write(self.to_input_text())  
        file.close()
        state = True
        return state

    def path_generator(self) -> str:
        ''' generate a path for local file '''
        path = "./result/Input"
        path = path +"-"+ time.strftime("%y%m%d-%H%M%S",time.localtime(time.time()))
        path = path + ".txt"
        return path

    def from_file(self, path:str):
        ''' load input from local file '''
        # contains '#': pass
        # contains []: start
        i = 0
        mylines = []                                # Declare an empty list.
        with open (path, "rt") as myfile:           # Open lorem.txt for reading text.
            for myline in myfile:                   # For each line in the file,
                mylines.append(myline.rstrip('\n')) # strip newline and add to list.
            mylines.append("")
            # print(mylines)
        while(i < len(mylines)-1):
            if mylines[i] == ("[Stations]"):
                while(True):
                    i += 1
                    parameters = mylines[i].split(" ")
                    self.add_station(id=parameters[0], capacity=parameters[1])
                    if(('#' in mylines[i+1]) or ("" == mylines[i+1])) or ('[' in mylines[i+1]) or (']' in mylines[i+1]):
                        break

            if mylines [i] == ("[Lines]"): 
                # print(i)     
                while(True):
                    i+=1
                    parameters = mylines[i].split(" ")
                    self.add_line(id=parameters[0],start_id=parameters[1],end_id=parameters[2],length=parameters[3],capacity=parameters[4])
                    if(('#' in mylines[i+1]) or ("" == mylines[i+1]))or ('[' in mylines[i+1]) or (']' in mylines[i+1]):
                        break

            if mylines [i] == ("[Trains]"): 
                # print(i)     
                while(True):
                    i+=1 
                    parameters = mylines[i].split(" ")
                    self.add_train(id=parameters[0],start_id=parameters[1],speed=parameters[2],capacity=parameters[3])
                    if(('#' in mylines[i+1]) or ("" == mylines[i+1])) or ('[' in mylines[i+1]) or (']' in mylines[i+1]):
                        break


            if mylines [i] == ("[Passengers]"):
                while(True):
                    i += 1 
                    parameters = mylines[i].split(" ")
                    self.add_passenger(id=parameters[0],start_id=parameters[1],end_id=parameters[2],size=parameters[3],target=parameters[4])
                    if(('#' in mylines[i+1]) or ("" == mylines[i+1])) or ('[' in mylines[i+1]) or (']' in mylines[i+1]):
                        break    
                break
    
            i+=1
        return self.Stations,self.Lines,self.Trains,self.Passengers


    def print_input(self):
        ''' print information of input '''
        print("---------------")
        print("| * printing input started ...")
        print(f"| * Stations: ({len(self.Stations)})")
        for i in range(len(self.Stations)):
            print(f"| * [{i}/{len(self.Stations)}] " + self.Stations[i].to_str_input())

        print(f"| * Lines: ({len(self.Lines)})")
        for i in range(len(self.Lines)):
            print(f"| * [{i}/{len(self.Lines)}] " + self.Lines[i].to_str_input())

        print(f"| * Trains: ({len(self.Trains)})")
        for i in range(len(self.Trains)):
            print(f"| * [{i}/{len(self.Trains)}] " + self.Trains[i].to_str_input())

        print(f"| * Passengers: ({len(self.Passengers)})")
        for i in range(len(self.Passengers)):
            print(f"| * [{i}/{len(self.Passengers)}] " + self.Passengers[i].to_str_input())

        print("| * print input finished")
        print("---------------")
        return


# test _string_to_int()
# print(type(_string_to_int("A1")))

# helper methods
def _string_to_int(string: str) -> int:
    r = re.findall('\d+', string)
    if (len(r) > 0):
        return int(r[0])
    else:
        return 0


def _string_to_float(string: str) -> float:
    r = re.findall('\d+', string)
    if (len(r) > 0):
        return float(r[0])
    else:
        return 0

input = Input()
a,b,c,d = input.from_file("./test/test-input-1.txt")
for i in a:
    print(i.to_str_input())
for i in b:
    print(i.to_str_input())
for i in c:
    print(i.to_str_input())
for i in d:
    print(i.to_str_input())

# print(input.to_input_text())
# # print(input.path_generator())
# input.print_input()


# print(input.Trains[0].start_station)