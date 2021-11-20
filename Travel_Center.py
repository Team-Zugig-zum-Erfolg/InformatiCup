from typing import List
from classes.Station import Station
from classes.Line import Line
from classes.Passenger import Passenger
from classes.Train import Train
from Stationlist import Stationlist
from Linelist import Linelist
from Trainlist import Trainlist


class Travel_Center:

    stationlist_manager = None
    linelist_manager = None
    trainlist_manager = None

    def __init__(self):

        self.stationlist_manager = Stationlist()
        self.linelist_manager = Linelist()
        self.trainlist_manager = Trainlist()
    
    def initial(self,stationlist,linelist,trainlist):

        self.stationlist_manager.initial(stationlist)
        self.linelist_manager.initial(linelist)
        self.trainlist_manager.initial(trainlist)
        return True
    
    def callable_trains(self,start_station):
        return [Train(1,2,12,1)]
        
    def callable_trains_not_in_move(self,start_station):
        return [[Train(1,2,12,1),Station(1,4)]]

    def callable_trains_in_move(self,start_station,end_station):
        return [[Train(1,2,12,1),Station(1,4)]]

    def call_train_not_in_move(self,train,start_station,end_station,passengers):
        return True
    
    def call_train_in_move(self,train,start_station,end_station,passengers):
        return True
       
    def check_capacity_train(self,train,start_time,end_time,passengers):
        return True
    	
    def determine_route(self,train,start_station,end_station):

        train = None
        start_time = 0
        end_time = 0

        return [train,start_time,end_time]

    def optimize_full_station(self,train,end):
        return True

    def save_route(self,train,start_station,end_station,passengers):
        return True
