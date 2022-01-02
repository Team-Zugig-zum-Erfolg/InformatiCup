# This module implements pseudo-random number generators for various distributions. (https://docs.python.org/3/library/random.html)
import random


from abfahrt.classes.Passenger import Passenger
from abfahrt.classes.Station import Station
from abfahrt.classes.Line import Line
from abfahrt.classes.Train import Train


class Generator:

    def _list_to_class_object(self, list_properties, class_name, stations):
        _class = globals()[class_name]

        for i in range(len(list_properties)):
            if type(list_properties[i]) == str:
                if i == 0:
                    list_properties[i] = int(list_properties[i][1:])
                elif list_properties[i] != "*":
                    station_id = int(list_properties[i][1:])
                    list_properties[i] = stations[station_id-1]
                else:
                    list_properties[i] = Station(-1, 999)

        return _class(*list_properties)

    def random_input_generate_as_classes(self, size_station=10, size_lines=20, size_trains=10, size_pa=10, sc_max=10, lc_max=2, ll_max=10, tc_max=20, pgs_max=10, ptr_max=10):
        stations = []
        lines = []
        trains = []
        passengers = []

        output = self.random_input_generate(
            size_station, size_lines, size_trains, size_pa, sc_max, lc_max, ll_max, tc_max, pgs_max, ptr_max)

        for i in range(len(output[0])):
            stations.append(self._list_to_class_object(
                output[0][i], "Station", None))

        for i in range(len(output[1])):
            lines.append(self._list_to_class_object(
                output[1][i], "Line", stations))

        for i in range(len(output[2])):
            trains.append(self._list_to_class_object(
                output[2][i], "Train", stations))

        for i in range(len(output[3])):
            passengers.append(self._list_to_class_object(
                output[3][i], "Passenger", stations))

        return [stations, lines, trains, passengers]

    def random_input_generate_file(self, size_station, size_lines, size_trains, size_pa, sc_max, lc_max, ll_max, tc_max, pgs_max, ptr_max, max_speed_train):
        output = self.random_input_generate(
            size_station, size_lines, size_trains, size_pa, sc_max, lc_max, ll_max, tc_max, pgs_max, ptr_max, max_speed_train)

        out_file = open("output_generated.txt", "w")

        out_file.write("[Stations]\n")
        self.write_objects_to_file(output[0], out_file)

        out_file.write("\n")

        out_file.write("[Lines]\n")
        self.write_objects_to_file(output[1], out_file)

        out_file.write("\n")

        out_file.write("[Trains]\n")
        self.write_objects_to_file(output[2], out_file)

        out_file.write("\n")

        out_file.write("[Passengers]\n")

        self.write_objects_to_file(output[3], out_file)

        out_file.close()

    def write_objects_to_file(self, _objects, out_file):

        for _object in _objects:
            i = 1
            for attr in _object:
                if type(attr) != str:
                    out_file.write(str(attr))
                else:
                    out_file.write(str(attr))
                if i == len(_object):
                    out_file.write("\n")
                else:
                    out_file.write(" ")
                i += 1

    def _depth_search(self, station, station_lines, visited):
        visited[station] = True
        for next in station_lines[station]:
            if not visited[next]:
                self._depth_search(next, station_lines, visited)
        return

    def _check_all_stations_connected(self, stations, station_lines):
        visited = [True]
        for i in range(len(stations)):
            visited.append(False)
        self._depth_search(1, station_lines, visited)
        t = 0
        for b in visited:
            if not b:
                return False
            t += 1
        return True

    def random_input_generate(self, size_station, size_lines, size_trains, size_pa, sc_max, lc_max, ll_max, tc_max, pgs_max, ptr_max, max_speed_train):

        stations = []
        lines = []
        trains = []
        passengers = []

        station_lines = [[]]

        random.seed(None)

        for i in range(1, size_station+1):
            stations.append(self.random_station_generate(i, sc_max))
            station_lines.append([])

        for i in range(1, size_lines+1):
            line = self.random_line_generate(
                i, stations, lines, lc_max, ll_max)
            lines.append(line)
            station_lines[int(line[1][1:])].append(int(line[2][1:]))
            station_lines[int(line[2][1:])].append(int(line[1][1:]))

        for i in range(1, size_trains+1):
            trains.append(self.random_train_generate(
                i, stations, trains, tc_max, max_speed_train))

        for i in range(1, size_pa+1):
            passengers.append(self.random_passenger_generate(
                i, stations, passengers, pgs_max, ptr_max))

        # check if not too many trains have the same initial start station
        # regenerating trains while at least one station has too many trains starting initially at it
        again = 1
        while(again == 1):
            for station in stations:
                again = 0
                trains_starting = 0
                for train in trains:
                    if train[1] == station[0]:
                        trains_starting += 1
                if trains_starting > station[1]:
                    trains = []
                    for i in range(1, size_trains+1):
                        trains.append(self.random_train_generate(
                            i, stations, trains, tc_max, max_speed_train))
                    again = 1
                    break

        # check if all passengers have a valid (not too huge) group size
        # regenerating passengers while at least one passenger has a too huge group size
        again = 1
        while(again == 1):
            for passenger in passengers:
                found = 0
                again = 0
                for train in trains:
                    if passenger[3] <= train[3]:
                        found = 1
                        break
                if found == 0:
                    passengers = []
                    for i in range(1, size_pa+1):
                        passengers.append(self.random_passenger_generate(
                            i, stations, passengers, pgs_max, ptr_max))
                    again = 1
                    break

        # check if every station is connected via at least one path with every other station
        # regenerating lines while not every station is connected with every each other station
        again = 1
        while again == 1:
            if self._check_all_stations_connected(stations, station_lines) == False:
                lines = []
                station_lines = []
                for i in range(0, size_station+1):
                    station_lines.append([])
                for i in range(1, size_lines+1):
                    line = self.random_line_generate(
                        i, stations, lines, lc_max, ll_max)
                    lines.append(line)
                    station_lines[int(line[1][1:])].append(int(line[2][1:]))
                    station_lines[int(line[2][1:])].append(int(line[1][1:]))
                again = 1
            else:
                again = 0

        return [stations, lines, trains, passengers]

    def random_station_generate(self, number, station_capacity_max):

        station = []
        station_name = "S" + str(number)
        station_capacity = random.randint(1, station_capacity_max)
        station = [station_name, station_capacity]
        return station

    def random_line_generate(self, number, stations, lines, line_capacity_max, line_length_max):

        size_stations = len(stations)

        line_id = "L" + str(number)
        line_end_0 = 0
        line_end_1 = 0
        while True:
            line_end_0 = random.randint(1, size_stations)
            line_end_1 = random.randint(1, size_stations)
            while line_end_1 == line_end_0:
                line_end_1 = random.randint(1, size_stations)
            contain = 0
            for line_current in lines:
                if line_current[1] == "S"+str(line_end_0) and line_current[2] == "S"+str(line_end_1) or line_current[1] == "S"+str(line_end_1) and line_current[2] == "S"+str(line_end_0):
                    contain = 1
            if contain == 1:
                continue
            else:
                break

        line_start = "S"+str(line_end_0)
        line_end = "S"+str(line_end_1)
        line_capacity = random.randint(1, line_capacity_max)
        line_length = random.randint(1, line_length_max)

        return [line_id, line_start, line_end, line_length, line_capacity]

    def random_train_generate(self, number, stations, trains, train_capacity_max, max_speed_train):

        size_stations = len(stations)
        train_id = "T" + str(number)
        train_start_station = "*"
        while True:
            every = random.randint(1, 10)
            if every <= 4:
                break
            train_start_station = "S" + str(random.randint(1, size_stations))
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

        train_speed = random.randint(1, max_speed_train)
        train_capacity = random.randint(1, train_capacity_max)

        return [train_id, train_start_station, train_speed, train_capacity]

    def random_passenger_generate(self, number, stations, passengers, group_size, target_round):

        size_stations = len(stations)
        passenger_id = "P" + str(number)

        passenger_start_station = random.randint(1, size_stations)
        passenger_end_station = random.randint(1, size_stations)
        while passenger_start_station == passenger_end_station:
            passenger_end_station = random.randint(1, size_stations)

        passenger_group_size = random.randint(1, group_size)
        passenger_target_round = random.randint(1, target_round)

        return [passenger_id, "S"+str(passenger_start_station), "S"+str(passenger_end_station), passenger_group_size, passenger_target_round]
