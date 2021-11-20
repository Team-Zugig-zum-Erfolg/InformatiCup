from typing import List
from classes.Station import Station
from classes.Line import Line
from classes.Passenger import Passenger
from classes.Train import Train


class Passengerlist:

    passengers = []
    
    def initial(self, passengerlist):
      
        self.passengers = passengerlist
        return True    
   
    
