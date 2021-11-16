from classes import Passenger
import random

class Generator:

    
    def random_input_generate(self, size_station, size_lines, size_trains, size_pa):

        stations = []
        lines = []
        trains = []
        passengers = []


        for i in range(1,size_station+1):
            stations.append(self.random_station_generate(i))

        for i in range(1,size_lines+1):
            lines.append(self.random_line_generate(i,stations,lines))

        for i in range(1,size_trains+1):
            trains.append(self.random_train_generate(i,stations,trains))

        for i in range(1,size_pa+1):
            passengers.append(self.random_passenger_generate(i,stations,passengers))


        
        return [stations,lines,trains,passengers]
            
    def random_station_generate(self,number):

        station = []
        station_name = "S" + str(number)
        station_capacity = random.randint(1,8)
        station = [station_name,station_capacity]
        return station

    def random_line_generate(self,number,stations,lines):

        size_stations = len(stations)
        
        line_id = "L" + str(number)
        
        line_end_0 = 0
        line_end_1 = 0
        while True:
            line_end_0 = random.randint(1,size_stations)
            line_end_1 = random.randint(1,size_stations)
            while line_end_1 == line_end_0:
                line_end_1 = random.randint(1,size_stations)
            contain = 0
            for line_current in lines:
                if line_current[1] == ["S"+str(line_end_0),"S"+str(line_end_1)]:
                    contain = 1
            if contain == 1:
                continue
            else:
                break
        
        line_end = ["S"+str(line_end_0),"S"+str(line_end_1)]
        line_capacity = random.randint(1,20)
        line_length = random.randint(1,10)
        
        return [line_id,line_end,line_length,line_capacity]

    def random_train_generate(self,number,stations,trains):

        size_stations = len(stations)

        train_id = "T" + str(number)
        train_start_station = "*"
        while True:
            every = random.randint(1,10)
            if every <= 4:
                break
            train_start_station = "S" + str(random.randint(1,size_stations))
            used = 0
            for train in trains:
                if train[1] == train_start_station:
                    used = used + 1
            check = 0
            for station in stations:
                if station[0] == train_start_station:
                    if used < station[1]:
                        check = 1
            if check == 1:
                break

        train_speed = round(random.uniform(0, 2), 1)
        train_capacity = random.randint(1,20)

        return [train_id,train_start_station,train_speed,train_capacity]

    def random_passenger_generate(self,number,stations,passengers):

        size_stations = len(stations)

        passenger_id = "P" + str(number)
      
        passenger_start_station = random.randint(1,size_stations)
        passenger_end_station = random.randint(1,size_stations)
        while passenger_start_station == passenger_end_station:
            passenger_end_station = random.randint(1,size_stations)

        passenger_group_size = random.randint(1,10)
        passenger_target_round = random.randint(1,10)

        return [passenger_id,"S"+str(passenger_start_station),"S"+str(passenger_end_station),passenger_group_size,passenger_target_round]

generator = Generator()

print(generator.random_input_generate(4,4,4,4))
