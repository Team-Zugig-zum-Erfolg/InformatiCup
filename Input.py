from typing import List
from classes.Station import Station
from classes.Line import Line
from classes.Passenger import Passenger
from classes.Train import Train
import time


class Input:
    Stations: List["Station"] = []
    Lines: List["Line"] = []
    Trains: List["Train"] = []
    Passengers: List["Passenger"] = []

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

    @staticmethod
    def from_file(path:str):
        ''' load input from local file '''
        # contains '#': pass
        # contains []: start
        
        input = Input()

        pass

    def print_input(self):
        ''' print information of input '''
        print("---------------")
        print("| * printing input started ...")
        print(f"| * Stations: ({len(self.Stations)})")
        for i in range(len(self.Stations)):
            print(f"| * [{i}/{len(self.Stations)}]" + self.Stations[i].to_str_input())

        print(f"| * Lines: ({len(self.Lines)})")
        for i in range(len(self.Lines)):
            print(f"| * [{i}/{len(self.Lines)}]" + self.Lines[i].to_str_input())

        print(f"| * Trains: ({len(self.Trains)})")
        for i in range(len(self.Trains)):
            print(f"| * [{i}/{len(self.Trains)}]" + self.Trains[i].to_str_input())

        print(f"| * Passengers: ({len(self.Passengers)})")
        for i in range(len(self.Passengers)):
            print(f"| * [{i}/{len(self.Passengers)}]" + self.Passengers[i].to_str_input())

        print("| * print input finished")
        print("---------------")
        return


input = Input()
print(input.to_input_text())
print(input.path_generator())
input.print_input()


