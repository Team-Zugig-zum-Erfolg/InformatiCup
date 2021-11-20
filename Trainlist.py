from typing import List
from classes.Station import Station
from classes.Line import Line
from classes.Passenger import Passenger
from classes.Train import Train





class Trainlist:


    trains = []
    
    
    def initial(self, trainlist):
      
        train_number = 1
        self.trains.append([])
        for train in trainlist:
            self.trains.append([]) 
            self.trains[train_number].append(int(train[3])) #Add capacity
            train_number = train_number + 1
        return True    
   
    def add_new_passengers_in_train(self, passengers, start, end, train_number):

        for pa_in_train in self.trains[train_number]:
            if type(pa_in_train) == int:
                continue
            if pa_in_train[1] == start and pa_in_train[2] == end:
                self.trains[train_number][0].extend(passengers)
                return True

        self.trains[train_number].append([passengers,start,end]);
        return True

    def _calculate_capacity_passengers(self, passengers):
        capacity = 0
        for pa in passengers:
            capacity = capacity + pa.get_group_size()	
        return capacity

    def check_capacity(self, new_passengers, start_time, end_time, train_number):

        capacity = -1
        new_capacity = self._calculate_capacity_passengers(new_passengers)

        for pa_in_train in self.trains[train_number]:
            if type(pa_in_train) == int:
                capacity = pa_in_train
                break

        for i in range(start_time+1,end_time):
            used_capacity_in_round = 0
            for pa_in_train in self.trains[train_number]:
                if type(pa_in_train) == int:
                    continue
                if pa_in_train[1] <= i and i <= pa_in_train[2]:
                    used_capacity_in_round = used_capacity_in_round + self._calculate_capacity_passengers(pa_in_train[0])
            if (capacity-used_capacity_in_round) < new_capacity:
                return False
        return True

test = Trainlist()
test.initial([[1,2,10,4],[2,2,4,2]])
test.add_new_passengers_in_train([Passenger(1,Station(2,20),Station(4,20),4,10)],2,6,1)
print(test.check_capacity([Passenger(1,Station(2,20),Station(4,20),4,10)],5,100,1))
