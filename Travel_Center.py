from typing import List
from classes.Station import Station
from classes.Line import Line
from classes.Passenger import Passenger
from classes.Train import Train
from Stationlist import Stationlist
from Linelist import Linelist
from Trainlist import Trainlist
from Passengerlist import Passengerlist


class Travel_Center:

    stationlist_manager = None
    linelist_manager = None
    trainlist_manager = None
    passengerlist_manager = None

    def __init__(self):

        self.stationlist_manager = Stationlist()
        self.linelist_manager = Linelist()
        self.trainlist_manager = Trainlist()
        self.passengerlist_manager = Passengerlist()
    
    def initial(self,stationlist,linelist,trainlist,passengerlist):

        self.stationlist_manager.initial(stationlist)
        self.linelist_manager.initial(linelist)
        self.trainlist_manager.initial(trainlist)
        self.passengerlist_manager.initial(passengerlist)
        return True

    #returns all trains, which are available directly (so they are defined with * as the starting station). Such a train can only be available, if this train can be in this start_station since the beginning, so since round 0
    def new_trains_available(self,start_station):
        return [[Train(1,2,12,1)]]

    #Returns the trains, which are WAITING/STOPPED at an arbitrary station. It also returns the belonging station, where the train is waiting and the start_time
    def callable_trains_not_in_move(self,start_station):
        return [[Train(1,2,12,1),Station(1,4),10]]

    #Returns the trains, which are in MOVING (so they follow a route and have passengers), but can change their route to start_station and then to end_station without damaging the arriving time of their passengers
    #
    #start_station:int  the station to change the route first
    #end_station:int    the station to pass after passing the start_station
    #
    #Return:            [[callable_train:class Train,station_of_the_train:class Station,start_time:int],....]
    def callable_trains_in_move(self,start_station,end_station):
        return [[Train(1,2,12,1),Station(1,4),10]]

    #does the same as callable_trains_not_in_move, but with saving the route, so writing the train to Stationlist and Linelist and adding the passengers to the train in the specific time range
    def call_train_not_in_move(self,train,start_station,end_station,passengers):
        return True
    
    #does the same as callable_trains_in_move, but with saving the new/changed route of the train, so writing/changing the train to Stationlist and Linelist and adding the passengers to the train in the specific time range
    def call_train_in_move(self,train,start_station,end_station,passengers):
        return True
    
    #checks the capacity of the train, so whether new passengers can be added to the train in a give time range or not  
    def check_capacity_train(self,train,start_time,end_time,passengers):
        return True

    #determines/calculates the route with the train from start_station to end_station starting at a given start_time
    def determine_route(self,train,start_station,end_station,start_time):
        train = None
        start_time = 0
        end_time = 0
        return [train,start_time,end_time]

    #moves the train to an another station from the end_station (if this station is full), where there is more than one capacity free (so not set by a train), so that the train will not block other trains passing this station
    def optimize_full_station(self,train,end_station):
        return True

    #saves the route for the train from start_station to end_station with the passengers by writing to Stationlist and Linelist and Trainlist
    def save_route(self,train,start_station,end_station,passengers):
        return True
