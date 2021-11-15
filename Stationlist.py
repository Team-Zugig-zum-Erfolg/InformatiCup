from classes import Station

class Stationlist:

    station_objects = []    #the station objects of type class Station
    stations = []           #the stations with capacities
    
    
    def initial(self, stationlist):
        
        self.station_objects = stationlist
        for station in stationlist:
            self.stations.append([])
        return True    
   
    def compare_free_place(self, train, in_station_time, station_number):

        trains_in_station = 0
        earliest_leave_time = -1
        station_capacities = self.stations[station_number]
        if len(station_capacities) < self.station_objects[station_number].getCapacity():
            return [True,-1]
        for train_in_station in station_capacities:
                if train_in_station[0] <= in_station_time and (train_in_station[1] >= in_station_time or train_in_station[3] >= in_station_time):
                    if earliest_leave_time > train_in_station[3] or earliest_leave_time == -1:
                        earliest_leave_time = train_in_station[3]
                    elif earliest_leave_time > train_in_station[1]:
                        earliest_leave_time = train_in_station[1]
                    trains_in_station = trains_in_station + 1
                if trains_in_station == self.station_objects[station_number].getCapacity():
                    return [False,earliest_leave_time]
        return [True,-1]
    
    def add_new_train_in_station(self, train, in_station_time, station_number):

        self.stations[station_number].append([in_station_time,in_station_time + 1,train,-1])
        return True


    def add_train_leave_time(self, train, leave_time, station_number):
        capacity = 0
        for train_in_station in self.stations[station_number]:
            if train_in_station[2] == train:
                self.stations[station_number][capacity][3] = leave_time
                return True
            capacity = capacity + 1
        return False


    def read_trains_from_station(self, station_number):
        trains = []
        for train_in_station in self.stations[station_number]:
            if train_in_station[2] not in trains:
                trains.append(train_in_station[2])
        return trains


station1 = Station("S1",10)
station2 = Station("S2",20)

stationlist = Stationlist()


stationlist.initial([station1,station2])

stationlist.add_new_train_in_station("T1",12,0)
print(stationlist.read_trains_from_station(0))




