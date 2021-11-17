from classes import Station

class Stationlist:

    
    stations = []           #the stations with capacities
    
    
    def initial(self, stationlist):
        
        station_number = 0
        for station in stationlist:
            self.stations.append([])
            for i in range(0,station[1]):
                self.stations[station_number].append([])
            station_number = station_number + 1
        return True    
   
    def compare_free_place(self, train, in_station_time, station_number):

        earliest_leave_time = -1
        station_capacities = self.stations[station_number]
        for capacity in station_capacities:
            not_free = 0
            for train_in_station in capacity:
                if self._train_in_station_is_full(train_in_station,in_station_time):
                    if earliest_leave_time > train_in_station[3] and train_in_station[3] != -1:
                            earliest_leave_time = train_in_station[3]
                    elif earliest_leave_time > train_in_station[1]:
                        earliest_leave_time = train_in_station[1]
                    elif earliest_leave_time == -1:
                        if train_in_station[3] != -1:
                            earliest_leave_time = train_in_station[3]
                        else:
                            earliest_leave_time = train_in_station[1]
                    not_free = 1
                    break
            if not_free == 0:
                return [True,-1]
            
        return [False,earliest_leave_time]

    def _train_in_station_is_full(self,train_in_station, in_station_time):
        return (train_in_station[0] <= in_station_time and (train_in_station[1] >= in_station_time or train_in_station[3] >= in_station_time))

    
    def add_new_train_in_station(self, train, in_station_time, station_number):

        capacity_number = 0
        for capacity in self.stations[station_number]:
            free = 1
            for train_in_station in capacity:
                if self._train_in_station_is_full(train_in_station,in_station_time):
                    free = 0
                    break
            if free == 1:
                self.stations[station_number][capacity_number].append([in_station_time,in_station_time + 1,train,-1])
                return True
            capacity_number = capacity_number + 1
        return False


    def add_train_leave_time(self, train, leave_time, station_number):

        capacity_number = 0
        for capacity in self.stations[station_number]:
            t=0
            for train_in_station in capacity:
                if train_in_station[2] == train and train_in_station[3] == -1:
                    self.stations[station_number][capacity_number][t][3] = leave_time
                    return True
                t=t+1
            capacity_number = capacity_number + 1
        return False


    def read_trains_from_station(self, station_number):
        trains = []
        for capacity in self.stations[station_number]:
            for train_in_station in capacity:
                if train_in_station[2] not in trains:
                    trains.append(train_in_station[2])
        return trains




stationlist = Stationlist()


stationlist.initial([["S1",1],["S2",2]])



stationlist.add_new_train_in_station("T1",12,0)


stationlist.add_new_train_in_station("T2",12,0)


print(stationlist.compare_free_place("T1",12,0))

stationlist.add_train_leave_time("T1",14,0)

print(stationlist.compare_free_place("T1",12,0))

print(stationlist.read_trains_from_station(0))




