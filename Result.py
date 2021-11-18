from typing import List
from classes.Station import Station
from classes.Line import Line
from classes.Passenger import Passenger
from classes.Train import Train
from Input import Input
import time

class Result:
    # format
    # 0 Start S2
    # 2 Depart L1

    # 1 Board T2
    # 6 Detrain


    trains:List[Train] = []
    passengers:List[Passenger] = []

    train_ids:set = set()
    passenger_ids:set = set()
    # Han: current not 100% sure how to save and gather information
    # so I create two kinds of lists
    # because the output format is 
    # [train T1]
    # 0 Start S2
    # 2 Depart L1
    # 3 Depart L2 ...
    # so it's better to collect all history of a train together
    train_history:List[str] = []
    passenger_history:List[str] = []
    
    def save_train_depart(self, train_id, depart_time, line_id):
        '''issue Update Result: save the depart of a train in history'''
        ''' find the train in trains[], add this action in the history'''
        train = self.find_or_add_train(train_id)
        train.add_depart(depart_time,Line(line_id,None,None,0.0))

    def save_train_start(self, start_time, train_id, station_id):
        train = self.find_or_add_train(train_id)
        train.add_start(start_time,Station(station_id,0))

    def save_passenger_board(self, passenger_id, board_time, train_id):
        p = self.find_or_add_passenger(passenger_id)
        p.add_board(board_time,Train(train_id,None,0.0,0))

    def save_passenger_detrain():
        '''6 Detrain'''
        pass
    
    def find_or_add_train(self, train_id:int)->Train:
        '''find the train in the trains[], if not exist, find one, currently cannot deduplicate'''
        find_result = filter(lambda t: t.id == train_id, self.trains)
        found_train = list(find_result)
        if len(found_train) == 0:
            # train not exist, add one
            train = Train(train_id,None,0.0,0)
            self.train_ids.add(train_id)
            self.trains.append(train)
            return train
        elif len(found_train) == 1:
            return found_train[0]
        else:
            print(f"! * Warning from Result: there train [{train_id}] is duplicated, \n! * there are [{len(found_train)}] such trains in [trains]")
            return found_train[0]

    def find_or_add_passenger(self, passenger_id:int)->Passenger:
        '''find the train in the trains[], if not exist, find one, currently cannot deduplicate'''
        find_result = filter(lambda t: t.id == passenger_id, self.passengers)
        found_p = list(find_result)
        if len(found_p) == 0:
            # train not exist, add one
            p = Passenger(passenger_id,None,None,0,0)
            self.passenger_ids.add(passenger_id)
            self.passengers.append(p)
            return p
        elif len(found_p) == 1:
            '''found one passenger, already saved in a list'''
            return found_p[0]
        else:
            print(f"! * Warning from Result: there Passenger [{passenger_id}] is duplicated, \n! * there are [{len(found_p)}] such passengers in [passengers]")
            return found_p[0]

    def add_passenger(self, passenger:Passenger):
        '''add a Passanger in list, if already exist(with same id), merge the history'''
        '''also save the id in a Set, for easily to check if some exist'''
        '''if you need to add a P only with id, please use find_or_add_passenger'''
        # perhaps the parameter is Groups.print_output()
        if passenger.id in self.passenger_ids:
            # passenger already exists, only need to merge history
            self.find_or_add_passenger(passenger.id).merge(passenger)
        else:
            # p not exist, add new one in list
            self.passengers.append(passenger)
            self.passenger_ids.add(passenger.id)

    def add_train(self,train:Train):
        if train.id in self.train_ids:
            self.find_or_add_train(train.id).merge(train)
        else:
            self.trains.append(train)
            self.train_ids.add(train.id)

    def passengers_add_from_input(self, input:Input):
        '''from input add all passengers'''
        for passenger in input.Passengers:
            self.add_passenger(passenger)
        
    def passengers_read_from_input(self, input:Input):
        '''directly read all passengers from input.passengers'''
        self.passengers = input.Passengers

    def train_add_from_input(self, input:Input):
        '''from input add all passengers'''
        for train in input.Trains:
            self.add_passenger(train)
        
    def train_read_from_input(self, input:Input):
        '''directly read all passengers from input.passengers'''
        self.trains = input.Trains



#%% saving methods

    def to_file(path:str):
        '''issue Update Result'''
        pass

    def path_generator(self) -> str:
        ''' generate a path for local file '''
        path = "./result/Output"
        path = path +"-"+ time.strftime("%y%m%d-%H%M%S",time.localtime(time.time()))
        path = path + ".txt"
        return path

    def compare_with(path:str):
        pass
