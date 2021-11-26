from typing import List
# from classes.Station import Station
# from classes.Line import Line
# from classes.Passenger import Passenger
# from classes.Train import Train
from Input import Input
# import Station
# import Line
# import Passenger
# import Train
# import Input

import time

class Result:
    # format
    # 0 Start S2
    # 2 Depart L1

    # 1 Board T2
    # 6 Detrain

    # [train T1]
    # 0 Start S2
    # 2 Depart L1
    # 3 Depart L2 ...
    # so it's better to collect all history of a train together

    trains:List[Train] = []
    passengers:List[Passenger] = []

    train_ids:set = set()
    passenger_ids:set = set()


    
    def save_train_depart(self, train_id, depart_time, line_id):
        ''' find the train in trains[], add this action in its history'''
        train = self.find_or_add_train(train_id)    # find the train in list, or add one in list
        train.add_depart(depart_time,Line(line_id,None,None,0.0))

    def save_train_start(self, start_time, train_id, station_id):
        train = self.find_or_add_train(train_id)
        train.add_start(start_time,Station(station_id,0))

    def save_passenger_board(self, passenger_id, board_time, train_id):
        p = self.find_or_add_passenger(passenger_id)
        p.add_board(board_time,Train(train_id,None,0.0,0))

    def save_passenger_detrain(self, passenger_id, detrain_time):
        p = self.find_or_add_passenger(passenger_id)
        p.add_detrain(detrain_time)
    
    def find_or_add_train(self, train_id:int)->Train:
        '''find the train in the trains[], if not exist, create one'''
        # currently cannot deal with duplication
        if train_id in self.train_ids:                                      # already exist
            find_result = filter(lambda t: t.id == train_id, self.trains)   # find it
            found_train = list(find_result)                                 # convert to list
            if len(found_train) == 1:
                return found_train[0]
            else:   # duplication
                print(f"* <!> [Warning] from Result: there train [{train_id}] is duplicated, \n! * there are [{len(found_train)}] such trains in [trains]")
                # self.handle_duplication_train()
                return found_train[0]
        else:   # train not exist, add one
            train = Train(train_id,None,0.0,0)  # new train
            self.train_ids.add(train_id)        # add in set() ids, to record the id in a set (there are no duplication)
            self.trains.append(train)
            return train

    def find_or_add_passenger(self, passenger_id:int)->Passenger:
        '''find the train in the trains[], if not exist, create one, currently cannot deduplicate'''
        if passenger_id in self.passenger_ids:                                      # already exist
            find_result = filter(lambda p: p.id == passenger_id, self.passengers)   # find it
            found_p = list(find_result)
            if len(found_p) == 1:                                                   # found one 
                '''found one passenger, already saved in a list'''
                return found_p[0]
            else:                                                                   # found many, duplication!
                # self.handle_duplication_passenger()
                print(f"* <!> [Warning] from Result: there Passenger [{passenger_id}] is duplicated, \n! * there are [{len(found_p)}] such passengers in [passengers]")
                return found_p[0]
        else:   # train not exist, add one
            p = Passenger(passenger_id,None,None,0,0)
            self.passenger_ids.add(passenger_id)
            self.passengers.append(p)
            return p

    def add_passenger(self, passenger:Passenger):
        '''add a Passanger in list, if already exist(with same id), merge the history'''
        '''also save the id in a Set, for easily to check if some exist'''
        '''if you need to add a P only with id, please use find_or_add_passenger'''
        if passenger.id in self.passenger_ids:          # already exist
            # passenger already exists, only need to merge history
            self.find_or_add_passenger(passenger.id).merge(passenger)
        else:                                           # not exist
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

    def to_output_text(self):
        result = ""
        for t in self.trains:
            result =+ f"[Train:{t.get_id_str()}]\n"
            result =+ t.to_str_output()
            result =+ "\n"
        for p in self.passengers:
            result =+ f"[Passenger:{p.get_id_str()}]\n"
            result =+ p.to_str_output()
            result =+ "\n"
        return result

    def to_file(self):
        ''' save input format in local file '''
        path = self.path_generator()
        state = False
        file = open(path, 'w')  
        file.write(self.to_output_text())  
        file.close()
        state = True
        return state

    def path_generator(self) -> str:
        ''' generate a path for local file '''
        path = "./result/Output"
        path = path +"-"+ time.strftime("%y%m%d-%H%M%S",time.localtime(time.time()))
        path = path + ".txt"
        return path

    def compare_with(path:str):
        pass


#%%

r = Result()
r.save_passenger_board(1,5,2)
r.save_passenger_detrain(9,2)
r.save_train_depart(1,2,3)
r.save_train_start(2,2,2)

r.to_output_text()