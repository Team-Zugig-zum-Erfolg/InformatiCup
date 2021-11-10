from typing import List
from Station import Station
from Line import Line
from Passenger import Passenger
# from Train import Train
import time


class Result:

    train_history = []
    passenger_history = []
    

    def add_passenger_board(Time:int, Passenger:Passenger, Train):
        # r = {'Time':Time, 'Passenger': Passenger, 'Para':Train}
        pass

    def add_passenger_detrain(Time:int, Passenger:Passenger):
        # r = [Time, Passenger.ID]
        pass


    def add_train_start():
        pass

    def add_train_depart():
        pass


    def sort():
        '''
        train_history[] and passenger_history[] will be sorted
        based on the name of train and name of passenger
        and based on time
        '''
        pass
    
    def to_file(path:str):
        pass

    def path_generator():
        pass

    def compare_with(path:str):
        pass
