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
        
    def get_station_by_str(self, id_str:str):
    	if id_str == "*":
    		return Station(-1,0)
    	for station in self.Stations:
    		if station.get_id_str() == id_str:
    			return station
    	return Station(-1,0)
	
		

    #@staticmethod
    def from_file(self, path:str):
        ''' load input from local file '''
        # contains '#': pass
        # contains []: start
        
        i = 0

        mylines = []                                # Declare an empty list.
        with open (path, "rt") as myfile:    # Open lorem.txt for reading text.
            for myline in myfile:                   # For each line in the file,
                mylines.append(myline.rstrip('\n')) # strip newline and add to list.
            mylines.append("")
        while(i < len(mylines)-1):
            if mylines[i] == ("[Stations]"):
                while(True):
                    i+=1
                    parameters = mylines[i].split(" ")
                    self.Stations.append(Station(int(parameters[0][1]),int(parameters[1])))
                    if(('#' in mylines[i+1]) or ("" == mylines[i+1])):
                        break

            if mylines [i] == ("[Lines]"): 
                print(i)     
                while(True):
                    i+=1
                    parameters = mylines[i].split(" ")
                    self.Lines.append(Line(int(parameters[0][1]),self.get_station_by_str(parameters[1]),self.get_station_by_str(parameters[2]),float(parameters[3]),int(parameters[4])))
                    if(('#' in mylines[i+1]) or ("" == mylines[i+1])):
                        break


            if mylines [i] == ("[Trains]"): 
                print(i)     
                while(True):
                    i+=1 
                    parameters = mylines[i].split(" ")
                    self.Trains.append(Train(int(parameters[0][1]),self.get_station_by_str(parameters[1]),float(parameters[2]),int(parameters[3])))
                    if(('#' in mylines[i+1]) or ("" == mylines[i+1])):
                        break


            if mylines [i] == ("[Passengers]"): 
            	  
            	while(True):
            	
            		i+=1 
            		parameters = mylines[i].split(" ")
            		self.Passengers.append(Passenger(int(parameters[0][1]),self.get_station_by_str(parameters[1]),self.get_station_by_str(parameters[2]),int(parameters[3]),int(parameters[4])))
            		if(('#' in mylines[i+1]) or ("" == mylines[i+1])):
            			break    
            
    
            i+=1
        return True

    def output_stationlist(self):
    	output = []
    	for station in self.Stations:
    		output.append([station.get_id(),station.get_capacity()])
    	return output
    
    
    def output_linelist(self):
    	output = []
    	for line in self.Lines:
    		output.append([line.get_id(),line.get_start().get_id(),line.get_end().get_id(),line.get_length(),line.get_capacity()])
    	return output
    
    def output_trainlist(self):
    	output = []
    	for train in self.Trains:
    		output.append([train.get_id(),train.get_start_station().get_id(),train.get_speed(),train.get_capacity()])
    	return output
    	
    def output_passengerlist(self):
    
    	output = []
    	for passenger in self.Passengers:
    		output.append(passenger)
    
    	
    	return output
    	
    def print_input(self):
        ''' print information of input '''
        print("---------------")
        print("| * printing input started ...")
        print(f"| * Stations: ({len(self.Stations)})")
        for i in range(1,len(self.Stations)+1):
            print(f"| * [{i}/{len(self.Stations)}] " + self.Stations[i-1].to_str_input())

        print(f"| * Lines: ({len(self.Lines)})")
        for i in range(1,len(self.Lines)+1):
            print(f"| * [{i}/{len(self.Lines)}] " + self.Lines[i-1].to_str_input())

        print(f"| * Trains: ({len(self.Trains)})")
        for i in range(1,len(self.Trains)+1):
            print(f"| * [{i}/{len(self.Trains)}] " + self.Trains[i-1].to_str_input())

        print(f"| * Passengers: ({len(self.Passengers)})")
        for i in range(1,len(self.Passengers)+1):
            print(f"| * [{i}/{len(self.Passengers)}] " + self.Passengers[i-1].to_str_input())

        print("| * print input finished")
        print("---------------")
        return




