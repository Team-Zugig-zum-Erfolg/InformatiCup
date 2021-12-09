from typing import List
from classes.Passenger import Passenger
from classes.Train import Train
from classes.Station import Station
from Input import Input
import time
import os


class Result:
    # Format
    # [Train T1]
    # 0 Start S2
    # 2 Depart L1
    # 3 Depart L2
    # [Passenger P1]
    # 1 Board T2
    # 6 Detrain

    trains:List[Train] = []
    passengers:List[Passenger] = []

    id_trains:set = set()
    id_passengers:set = set()


    
    def save_train_depart(self, id_train, time, id_line):
        ''' find the train in trains[], add this action in its history'''
        # print(f"-> enter [save_train_depart], id={id_train}, time={time}, id_line={id_line}")

        train = self.find_or_add_train(id_train)    # find the train in list, or add one in list
        train.add_depart(time = time, line_id = id_line)
        # print(" - save_train_depart:", train.id)
        # print(" - location:", id(train))
        # for i in self.trains:
        #     print(" + train: ", i.id," history: ", i.history)
        # print("===")

    def save_train_start(self, id_train, time, id_station):
        # print(f"-> enter [save_train_start], id={id_train}, time={time}, id_line={id_station}")

        # for i in self.trains:
        #     print(" + train: ", i.id," history: ", i.history)

        train = self.find_or_add_train(id_train)

        # for i in self.trains:
        #     print(" + train: ", i.id," history: ", i.history)

        train.add_start(time = time, station_id = id_station)
        
        # print(" - save_train_start:", train.id)
        # print(" - location:", id(train))
        # for i in self.trains:
        #     print(" + train: ", i.id," history: ", i.history)
        # print("===")

    def save_passenger_board(self, id_passenger, time, id_train):
        # print(f"-> enter [save_passenger_board], id={id_passenger}, time={time}, id_line={id_train}")
        p = self.find_or_add_passenger(id_passenger)
        p.add_board(time = time, train_id = id_train)

        # print(" - save_passenger_board:", p.id)
        # print(" - location:", id(p))
        # for i in self.passengers:
        #     print(" - passenger: ", i.id," history: ", i.history)
        # print("===")

    def save_passenger_detrain(self, id_passenger, time):
        # print(f"-> enter [save_passenger_detrain], id={id_passenger}, time={time}")
        p = self.find_or_add_passenger(id_passenger)
        p.add_detrain(time = time)
        # print(" - save_passenger_detrain:", p.id)
        # print(" - location:", id(p))
        # for i in self.passengers:
        #     print(" - passenger: ", i.id," history: ", i.history)
        # print("===")
    
    def find_or_add_train(self, id_train:int)->Train:
        '''find the train in the trains[], if not exist, create one'''
        # print("*-> enter [find_or_add_train]")

        # for i in self.trains:
        #     print(" + train: ", i.id," history: ", i.history)

        # currently cannot deal with duplication
        if id_train in self.id_trains:                                      # already exist
            # print(f" -- train id [{id_train}] exist")
            find_result = filter(lambda t: t.id == id_train, self.trains)   # find it
            found_train = list(find_result)                                 # convert to list
            # print(f" -- train id [{id_train}] found with id [{found_train[0].id}]")
            if len(found_train) == 1:
                # print(" -- [find] location: ", id(found_train[0]))
                return found_train[0]
            else:   # duplication
                # print(f"* <!> [Warning] from Result: there train [{id_train}] is duplicated, \n! * there are [{len(found_train)}] such trains in [trains]")
                # self.handle_duplication_train()
                return found_train[0]
        else:   # train not exist, add one
            # print(f" -- id [{id_train}] not exist, now added")
            # for i in self.trains:
            #     print(" + train: ", i.id," history: ", i.history)
            train = Train(id_train,Station(0,0),0.0,0)  # new train
            # print(" -- new train history",train.history)
            # for i in self.trains:
            #     print(" + train: ", i.id," history: ", i.history)
            self.id_trains.add(id_train)        # add in set() ids, to record the id in a set (there are no duplication)
            # for i in self.trains:
            #     print(" + train: ", i.id," history: ", i.history)

            self.trains.append(train)
            # for i in self.trains:
            #     print(" + train: ", i.id," history: ", i.history)
            # print(f" -- train id [{id_train}] added with id [{train.id}]")
            # print(" -- [find] location: ", id(train))

            #sort the trains list
            self.trains.sort(key=lambda x : x.id)
            
            return train

    def find_or_add_passenger(self, id_passenger:int)->Passenger:
        '''find the train in the trains[], if not exist, create one, currently cannot deduplicate'''
        # print("*-> enter [find_or_add_passenger]")
        if id_passenger in self.id_passengers:                                      # already exist
            find_result = filter(lambda p: p.id == id_passenger, self.passengers)   # find it
            found_p = list(find_result)
            if len(found_p) == 1:                                                   # found one 
                '''found one passenger, already saved in a list'''
                return found_p[0]
            else:                                                                   # found many, duplication!
                # self.handle_duplication_passenger()
                print(f"* <!> [Warning] from Result: there Passenger [{id_passenger}] is duplicated, \n! * there are [{len(found_p)}] such passengers in [passengers]")
                return found_p[0]
        else:   # train not exist, add one
            p = Passenger(id_passenger,None,None,0,0)
            self.id_passengers.add(id_passenger)
            self.passengers.append(p)
            
            #sort the passengers list
            self.passengers.sort(key=lambda x : x.id)
            
            return p

    def add_passenger(self, passenger:Passenger):
        '''add a Passanger in list, if already exist(with same id), merge the history'''
        '''also save the id in a Set, for easily to check if some exist'''
        '''if you need to add a P only with id, please use find_or_add_passenger'''
        if passenger.id in self.id_passengers:          # already exist
            # passenger already exists, only need to merge history
            self.find_or_add_passenger(passenger.id).merge(passenger)
        else:                                           # not exist
            # p not exist, add new one in list
            self.passengers.append(passenger)
            self.id_passengers.add(passenger.id)

            #sort the passengers list
            self.passengers.sort(key=lambda x : x.id)

    def add_train(self,train:Train):
        if train.id in self.id_trains:
            self.find_or_add_train(train.id).merge(train)
        else:
            self.trains.append(train)
            self.id_trains.add(train.id)
            
            #sort the trains list
            self.trains.sort(key=lambda x : x.id)

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
            self.add_train(train)
        
    def train_read_from_input(self, input:Input):
        '''directly read all passengers from input.passengers'''
        self.trains = input.Trains



#%% saving methods

    def to_output_text(self):
        result = ""
        for t in self.trains:
            result += f"[Train:{t.get_id_str()}]\n"
            result += t.to_str_output()
            result += "\n"
            result += "\n"
        for p in self.passengers:
            result += f"[Passenger:{p.get_id_str()}]\n"
            result += p.to_str_output()
            result += "\n"
            result += "\n"
        return result

    def to_file_same(self):
        ''' save output file in SAME file output '''
        path = './output.txt'
        state = False
        file = open(path, 'w')  
        file.write(self.to_output_text())  
        file.close()
        state = True
        return state

    def to_file(self, folder = "result"):
        ''' save output format in local file 
        parameter: folder: the folder to save this file, default is "result"
        '''
        dir_name = str(folder)
        path = self.path_generator(folder = dir_name)
        state = False
        if os.path.isdir(dir_name):
            file = open(path, 'w')
        else:
            os.mkdir(dir_name)
            file = open(path, 'w')
        file.write(self.to_output_text())  
        file.close()
        state = True
        return state

    def path_generator(self, folder = "result") -> str:
        ''' generate a path for local file '''
        dir_name = str(folder)
        path = "./" + dir_name + "/Output"
        path = path +"-"+ time.strftime("%y%m%d-%H%M%S",time.localtime(time.time()))
        path = path + ".txt"
        # filename = "Output-" + time.strftime("%y%m%d-%H%M%S",time.localtime(time.time())) + ".txt"
        # return filename
        return path

    def compare_with(path:str):
        pass




def test_save_train_depart(r, id, time, line):
    print("****************************")
    print(f"soll: depart, train [{id}], time: [{time}], line: [{line}]")
    print("- Before -:")
    print(r.to_output_text())
    print()
    r.save_train_depart(id_train=id,time=time,id_line=line)
    print("- After -:")
    print(r.to_output_text())

def test_save_train_start(r, id, time ,station):
    print("****************************")
    print(f"soll: start, train [{id}], time: [{time}], station: [{station}]")
    print("- Before -:")
    print(r.to_output_text())
    print()
    r.save_train_start(id_train=id,time=time,id_station=station)
    print("- After -:")
    print(r.to_output_text())

def test_save_passenger_board(r, id, time, train):
    print("****************************")
    print(f"soll: board, passenger [{id}], time: [{time}], train: [{train}]")
    print("- Before -:")
    print(r.to_output_text())
    print()
    r.save_passenger_board(id_passenger=id, time=time, id_train=train)
    print("- After -:")
    print(r.to_output_text())

def test_save_passenger_detrain(r, id, time):
    print("****************************")
    print(f"soll: detrain, passenger [{id}], time: [{time}]")
    print("- Before -:")
    print(r.to_output_text())
    print()
    r.save_passenger_detrain(id_passenger=id, time=time)
    print("- After -:")
    print(r.to_output_text())