import math
import sys

from Stationlist import Stationlist
from Linelist import Linelist
from classes.Travel import Travel
from classes.TrainInLine import TrainInLine
from classes.TrainInStation import TrainInStation
from classes.Station import Station
import Result

L_ID = 0
L_S_ID_START = 1
L_S_ID_END = 2
L_LEN = 3
L_CAPACITY = 4

S_ID = 0
S_CAPACITY = 1

T_ID = 0
T_S_ID = 1
T_SPEED = 2
T_CAPACITY = 3

LINE_INPUT_LIST = []
STATION_INPUT_LIST = []
TRAIN_INPUT_LIST = []

S_LINEPLAN = []

TARGET_TIME = 0


class Travel_Center:
    train_line_time_list = []

    def __init__(self, station_input_list, line_input_list, train_input_list):
        global LINE_INPUT_LIST
        global STATION_INPUT_LIST
        global TRAIN_INPUT_LIST

        global S_LINEPLAN
        self.train_line_time_list.append([])
        LINE_INPUT_LIST = line_input_list
        STATION_INPUT_LIST = station_input_list
        TRAIN_INPUT_LIST = train_input_list
        for train in train_input_list:
            self.train_line_time_list.append([])
            self.train_line_time_list[train.id].append(0)
            for line in line_input_list:
                self.train_line_time_list[train.id].append(
                    math.ceil(line[L_LEN] / train.speed)-1)
        S_LINEPLAN.append([])
        S_LINEPLAN[0].append([])
        for station in station_input_list:
            S_LINEPLAN.append([])
            S_LINEPLAN[station[S_ID]].append([])
            S_LINEPLAN[station[S_ID]].append([])
            for line in line_input_list:
                if line[L_S_ID_START] == station[S_ID]:
                    S_LINEPLAN[station[S_ID]][0].append(line[L_S_ID_END])
                    S_LINEPLAN[station[S_ID]][1].append(line[L_ID])
                elif line[L_S_ID_END] == station[S_ID]:
                    S_LINEPLAN[station[S_ID]][0].append(line[L_S_ID_START])
                    S_LINEPLAN[station[S_ID]][1].append(line[L_ID])

    def _get_all_line_station(self, s_station_id, e_station_id, lineplan):
        lineplan = lineplan + [s_station_id]
        if s_station_id == e_station_id:
            return [lineplan]

        lineplans = []
        for node in S_LINEPLAN[s_station_id][0]:
            if node not in lineplan:
                newpaths = self._get_all_line_station(node, e_station_id, lineplan)
                for newpath in newpaths:
                    lineplans.append(newpath)
        return lineplans

    def _find_lines(self, s_station_id, e_station_id):
        lineplans = self._get_all_line_station(s_station_id, e_station_id, [])
        lines = []
        j = 0
        for lineplan in lineplans:
            lines.append([])
            for i in range(len(lineplan) - 1):
                for line in LINE_INPUT_LIST:
                    if line[L_S_ID_START] == lineplan[i] and line[L_S_ID_END] == lineplan[i + 1]:
                        lines[j].append(line[L_ID])
                    elif line[L_S_ID_END] == lineplan[i] and line[L_S_ID_START] == lineplan[i + 1]:
                        lines[j].append(line[L_ID])
            j += 1
        return lines

    def find_best_line(self, s_station_id, e_station_id):
        lines = self._find_lines(s_station_id, e_station_id)
        short_len = 0
        short_line = None
        for line in lines:
            length = 0
            for each in line:
                length += LINE_INPUT_LIST[each - 1][L_LEN]
            if short_len == 0 or short_len > length:
                short_len = length
                short_line = line
        return [short_len, short_line]

    def time_count_train(self, start_station, end_station, train, start_time):

        length, lines = self.find_best_line(start_station.id, end_station.id)
        line_time = []
        station_times = [TrainInStation(start_time,start_time+1,train,None,start_station.id)]
        on_board = start_time + 1
        add_time = on_board + 1
        prev_station = start_station
        for li in range(len(lines)):
            line_time.append(TrainInLine(train.id, add_time,
                                         add_time + self.train_line_time_list[train.id][lines[li]], lines[li]))
            stations = Travel_Center.get_stations_by_line(lines[li])
            if stations[0].id != prev_station.id:
                next_station = stations[0]
            else:
                next_station = stations[1]
            prev_station = next_station
            
            station_times.append(TrainInStation(add_time + self.train_line_time_list[train.id][lines[li]],add_time + self.train_line_time_list[train.id][lines[li]],train.id,add_time + self.train_line_time_list[train.id][lines[li]],next_station.id))                          
            
            add_time += self.train_line_time_list[train.id][lines[li]]
        
        station_time = TrainInStation(add_time, add_time + 1, train, None, end_station.id)

        return Travel(start_time, on_board, line_time, station_time, start_station, end_station, train, station_times)

    @staticmethod
    def get_stations_by_line(line_id):
        line = LINE_INPUT_LIST[line_id-1]
        station_1 = Station(STATION_INPUT_LIST[line[L_S_ID_START]-1][S_ID],STATION_INPUT_LIST[line[L_S_ID_START]-1][S_CAPACITY])
        station_2 = Station(STATION_INPUT_LIST[line[L_S_ID_END]-1][S_ID],STATION_INPUT_LIST[line[L_S_ID_END]-1][S_CAPACITY])
        return [station_1,station_2]

    @staticmethod
    def check_line_station(travel: Travel, stationlist: Stationlist, linelist: Linelist, result, travel_center):
        line_availables_list = []
        line_time_changes = []
        available = True
        station_is_full = False
        full_stations = []
        prev_station = travel.start_station
        for travel_in_line in travel.line_time:
            line_available, line_time_change = linelist.compare_free(travel_in_line)
            # print("line_time_change: "+str(line_time_change))
            # print("line_time_change: "+str(line_available))
            line_availables_list.append(line_available)
            line_time_changes.append(line_time_change)
            stations = Travel_Center.get_stations_by_line(travel_in_line.line_id)
            if stations[0].id != prev_station.id:
                next_station = stations[0]
            else:
                next_station = stations[1]
            if next_station.id != travel.end_station.id:
                s_available, s_time_change = stationlist.compare_free_place(TrainInStation(travel_in_line.end,travel_in_line.end,travel_in_line.train,travel_in_line.end,next_station.id))
                if s_available == False and s_time_change == -1: #full
                    full_stations.append([next_station,travel_in_line.end]) 
                line_availables_list.append(s_available)
                line_time_changes.append(s_time_change)

            prev_station = next_station
        station_available, station_time_change = stationlist.compare_free_place(travel.station_time)

        if station_available == False and station_time_change == -1:
            station_is_full = True
            available = False
            # print("full")

        station_delay_time = 0
        if not station_available and station_is_full == False:
            # print("station_time_change: "+str(station_time_change))
            # print("out_train_time:"+str(travel.station_time.passenger_out_train_time))
            station_delay_time = ((station_time_change + 1) - travel.station_time.passenger_out_train_time)
            # print("station_delay_time:"+str(station_delay_time))
            available = False

        delay_time = station_delay_time

        i=0
        t=0
        for _line_time in travel.line_time:
            if not line_availables_list[i]:
                available = False

                line_delay_time = line_time_changes[t] - travel.line_time[i].start
                if delay_time < line_delay_time:
                    delay_time = line_delay_time
            if (len(line_time_changes) - t) > 1:
                if not line_availables_list[i+1]:
                    current_station_delay_time = line_time_changes[t+1] - travel.line_time[i].end
                    if delay_time < current_station_delay_time:
                        delay_time = current_station_delay_time
            t = t + 2
            i = i + 1

        return [available, delay_time, station_is_full, full_stations]

    @staticmethod
    def delay_travel(travel: Travel, delay_time):
        travel.start_time = travel.start_time + delay_time
        travel.on_board = travel.on_board + delay_time
        for i in range(0, len(travel.line_time)):
            travel.line_time[i].start = travel.line_time[i].start + delay_time
            travel.line_time[i].end = travel.line_time[i].end + delay_time
        for i in range(0, len(travel.station_times)):
            travel.station_times[i].passenger_out_train_time = travel.station_times[i].passenger_out_train_time + delay_time
            travel.station_times[i].passenger_in_train_time = travel.station_times[i].passenger_in_train_time + delay_time
        travel.station_time.passenger_out_train_time = travel.station_time.passenger_out_train_time + delay_time
        travel.station_time.passenger_in_train_time = travel.station_time.passenger_in_train_time + delay_time

    @staticmethod
    def save_travel(travel: Travel, groups, passengers, stationlist: Stationlist, linelist: Linelist, result: Result, travel_center, ignore_full_station=False):
        enable, delay_time, full , _ = Travel_Center.check_line_station(travel, stationlist, linelist, result, travel_center)
        if enable or (full == True and ignore_full_station==True):
            
            save = stationlist.add_train_leave_time(travel.train, travel.on_board, travel.start_station.id, result)

            prev_station = travel.start_station
            for line in travel.line_time:
                save = linelist.add_new_train_in_line(line)

                stations = Travel_Center.get_stations_by_line(line.line_id)
                if stations[0].id != prev_station.id:
                    next_station = stations[0]
                else:
                    next_station = stations[1]
                if next_station.id != travel.end_station.id:
                    stationlist.add_new_train_in_station(TrainInStation(line.end,line.end,TRAIN_INPUT_LIST[line.train-1],line.end,next_station.id),result)

                if save:
                    result.save_train_depart(line.train, line.start, line.line_id)

            

            save = stationlist.add_new_train_in_station(travel.station_time, result,ignore_full_station)

            if passengers is not None:

                groups.passengers_arrive(passengers)

                for passenger in passengers:
                    result.save_passenger_board(passenger.id, travel.on_board, line.train)
                    result.save_passenger_detrain(passenger.id, travel.station_time.passenger_in_train_time)

        return [save, delay_time]

    @staticmethod
    def check_passengers(route):
        start_station = route[0].start_station
        end_station = route[0].end_station
        group_size = 0
        global TARGET_TIME
        TARGET_TIME = route[0].target_time
        for passenger in route:
            group_size = group_size + passenger.group_size
        return [start_station, end_station, group_size]

    @staticmethod
    def check_train_in_station(start_station, group_size, stationlist: Stationlist, linelist: Linelist):
        start_times, trains, station_current = stationlist.read_trains_from_station(start_station.id)
        capacity_enable = Travel_Center._check_capacity(trains, group_size, start_times, None)
        Travel_Center._remove_passing_station_trains(start_station,trains,start_times,stationlist)
        available = False
        if len(trains) > 0:
            available = True
        return start_times, trains, available

    @staticmethod
    def check_train_not_in_station(group_size, stationlist: Stationlist):  # choose train from other station
        start_times, trains, start_stations = Travel_Center._check_trains_in_all_station(stationlist)
        capacity_enable = Travel_Center._check_capacity(trains, group_size, start_times, start_stations)
        return start_times, trains, start_stations, capacity_enable

    @staticmethod
    def get_neighboor_stations(station):

        neighboor_stations = []

        for line in LINE_INPUT_LIST:
            if line[L_S_ID_START] == station.id:
                neighboor_stations.append(
                    Station(line[L_S_ID_END], STATION_INPUT_LIST[line[L_S_ID_END] - 1][S_CAPACITY]))
            elif line[L_S_ID_END] == station.id:
                neighboor_stations.append(
                    Station(line[L_S_ID_START], STATION_INPUT_LIST[line[L_S_ID_START] - 1][S_CAPACITY]))

        return neighboor_stations

    @staticmethod
    def station_is_never_blocked(station, stationlist):

        for capacity in stationlist.stations[station.id]:
            if len(capacity) == 0:
                return True
            blocked = 0
            for train_in_station in capacity:
                if train_in_station.leave_time == None:
                    blocked = 1
            if blocked == 0:
                return True
        return False

    @staticmethod
    def train_is_blocking_other_train_in_station(station, train, stationlist):

        for capacity in stationlist.stations[station.id]:
            for train_in_station in capacity:
                if train_in_station.train == train and train_in_station.leave_time == None:
                    for _train_in_station in capacity:
                        if _train_in_station.passenger_out_train_time > train_in_station.passenger_out_train_time and _train_in_station.train != train:
                            return True

        return False

    @staticmethod
    def clear_station_with_specific_train(end_station, train, arrive_time, linelist: Linelist, stationlist: Stationlist,
                                          result, travel_center):
        # get the neighboor stations of the end_station,
        # so the blocking trains in the end_station can be moved to one of the free (or not blocked) neighboor stations
        neighboor_stations = Travel_Center.get_neighboor_stations(end_station)
        next_station = None
        for neighboor_station in neighboor_stations:
            if Travel_Center.station_is_never_blocked(neighboor_station, stationlist) == True:
                next_station = neighboor_station
                break
        if next_station == None:
            raise ValueError ("clear station error: no station available")  # no neighboor station is free (free = not blocked)

        travel = travel_center.time_count_train(end_station, next_station, train, arrive_time)
        available = 0
        while not available:
            available, delay_time, _, _ = Travel_Center.check_line_station(travel, stationlist, linelist,result,travel_center)
            if available:
                Travel_Center.save_travel(travel, None, None, stationlist, linelist, result,travel_center)
            elif delay_time != -1:
                Travel_Center.delay_travel(travel, delay_time)
            else:
                raise ValueError("clear station error: no station available")  # all neighboor stations are blocked (should actually not happen, because they are checked above)

        if Travel_Center.train_is_blocking_other_train_in_station(next_station, travel.train, stationlist):
            Travel_Center.clear_station_with_specific_train(next_station, travel.train,
                                                            travel.station_time.passenger_out_train_time,
                                                            linelist, stationlist, result, travel_center)
        return True

    @staticmethod
    def station_is_in_station_times_list(station, station_times_list):
        for station_time in station_times_list:
            if station.id == station_time.station_id:
                return True
        return False

    @staticmethod
    def station_has_more_than_one_free_capcacity(station, stationlist):
        capacities = stationlist.stations[station.id]
        free = 0
        for capacity in capacities:
            if not Stationlist._capacity_is_full(capacity):
                free = free + 1

        return (free == 2)

    @staticmethod
    def clear_station(end_station, origin_station, arrive_time, linelist:Linelist, stationlist: Stationlist, result,
                      travel_center,stations_to_ignore):
        # clear station (move trains out of it to other stations)
        # clear station (move trains out of it to other stations)

        # get the neighboor stations of the end_station,
        # so the blocking trains in the end_station can be moved to one of the free
        # (or not blocked) neighboor stations
        neighboor_stations = Travel_Center.get_neighboor_stations(end_station)
        next_station = None
        for neighboor_station in neighboor_stations:
            if Travel_Center.station_is_never_blocked(neighboor_station, stationlist) == True and (not Travel_Center.station_is_in_station_times_list(neighboor_station,stations_to_ignore) or Travel_Center.station_has_more_than_one_free_capcacity(neighboor_station, stationlist)):
                next_station = neighboor_station
                break
        if next_station == None and origin_station != None:
            for neighboor_station in neighboor_stations:
                if neighboor_station.id == origin_station.id:
                    next_station = origin_station
        if next_station == None:
            raise ValueError("clear station error: no station available")  #no neighboor station is free (free = not blocked) and origin station is also not available

        # get the blocking trains in the station (blocking trains = trains in the station with no leave time)
        # a station is only blocked, if all trains in the station have no leave time
        start_times, trains, station = stationlist.read_trains_from_station(end_station.id)
        
        travels = []
        # print("next_station:"+str(next_station))
        # print("train_in_next_station:"+str(stationlist.stations[end_station.id]))
        i=0
        for train in trains:
            travels.append(travel_center.time_count_train(end_station, next_station, train,
                                                start_times[i]))  # smallest start time
            i= i + 1
        available = 0
        while not available:
            full_station_list = []
            availables = []
            delay_times = []
            full_end_station = [] #if full_end_station[i]=True, then for travels[i] the end_station is blocked
        # (there are only trains with leave_time=None before the train will arrive)
     
            for travel in travels:
                available_current, delay_time, full, full_stations = Travel_Center.check_line_station(travel, stationlist, linelist,result,travel_center)
                availables.append(available_current)
                delay_times.append(delay_time)
                full_end_station.append(full) #full==1: the end_station is blocked by stopped trains with leave_time=None
                full_station_list.append(full_stations)
            
            i = 0
            available_run = 0
            travel_available = []
            for available in availables:
                if available:
                        travel_available.append(travels[i])
                        available_run = 1
                i += 1

            if available_run:
                    short_time = travel_available[0].station_time.passenger_out_train_time
                    short_travel = travel_available[0]
                    for travel in travel_available:
                        if short_time > travel.station_time.passenger_out_train_time:
                            short_time = travel.station_time.passenger_out_train_time
                            short_travel = travel
            
                    Travel_Center.save_travel(short_travel, None, None, stationlist, linelist, result,travel_center)
                    available = 1
            elif False in full_end_station: # end_station is for at least one travel free (so not blocked)
                    i = 0
                    for travel in travels:
                        Travel_Center.delay_travel(travel, delay_times[i])
                        i += 1
            else:
                raise ValueError("clear station error: no station available")  # all neighboor stations are blocked (should actually not happen, because they are checked above)

        return True

    @staticmethod  # move a train to start station
    def train_move_to_start_station(start_station, trains, start_times, start_stations, stationlist, linelist,
                                    result: Result, travel_center):
        save = travel_center._train_to_station(start_station, trains, start_times, start_stations, stationlist,
                                               linelist, result, travel_center)
        return save

    @staticmethod
    def _remove_passing_station_trains(start_station,trains,start_times,stationlist):
        capacities = stationlist.stations[start_station.id]
        i=0
        for train in trains:
            for capacity in capacities:
                for _train_in_station in capacity:
                    if train.id == _train_in_station.train.id:
                        if start_times[i] <= _train_in_station.passenger_out_train_time:
                            if _train_in_station.passenger_out_train_time == _train_in_station.passenger_in_train_time:
                                trains.remove(train)
            i = i + 1

    @staticmethod
    def _check_capacity(trains, group_size, start_times, start_stations):
        b_capacity = False
        if len(trains) != 0:
            i = 0
            while True:
                if trains[i].capacity < group_size:
                    start_times.pop(i)
                    trains.pop(i)
                    if start_stations is not None:
                        start_stations.pop(i)
                else:
                    i += 1
                    b_capacity = True
                if i >= len(trains):
                    break
        return b_capacity

    @staticmethod
    def _check_trains_in_all_station(stationlist: Stationlist):
        trains = []
        start_times = []
        start_stations = []
        for i in range(1, len(stationlist.stations)):
            start_time, train, station = stationlist.read_trains_from_station(i)
            for t in train:
                trains.append(t)

            for s in start_time:
                start_times.append(s)
                start_stations.append(station)

        return start_times, trains, start_stations

    def _train_to_station(self, end_station, trains, start_times, start_stations, stationlist, linelist, result: Result,
                          travel_center):
        travels = []
        for i in range(0, len(trains)):
            start = start_stations[i]
            train = trains[i]
            start_time = start_times[i]
            # print("-----")
            # print(start)
            # print(end_station)
            # print(train)
            # print(start_time)
            travels.append(self.time_count_train(start, end_station, train, start_time))

        availables = []
        while True not in availables:  # find travels until minimal 1 travel
            # available, linelist, stationlist, travel, delay_time
            availables = []
            delay_times = []
            full_end_station = []
            # print("train_to_station")
            for travel in travels:
                available, delay_time, full, _ = Travel_Center.check_line_station(travel, stationlist, linelist,result,travel_center)
                availables.append(available)
                delay_times.append(delay_time)
                full_end_station.append(full)

            if True not in availables and (False in full_end_station):
                i = 0
                for travel in travels:
                    Travel_Center.delay_travel(travel, delay_times[i])
                    i = i + 1
            elif True in full_end_station:
                smallest_arrive_time = travels[0].station_time.passenger_out_train_time + delay_times[0]
                shortest_travel = travels[0]
                i = 0
                # calculate the smallest time, when to move a stopped train out of the blocked station
                for travel in travels:
                    if (travels[i].station_time.passenger_out_train_time + delay_times[i]) < smallest_arrive_time:
                        smallest_arrive_time = travels[i].station_time.passenger_out_train_time + delay_times[i]
                        shortest_travel = travel
                    i += 1

                Travel_Center.clear_station(end_station,travel.start_station, smallest_arrive_time - 2, linelist, stationlist, result, travel_center, travel.station_times)

        # print(availables)
        travels_available = []
        i = 0
        for available in availables:
            if available:
                travels_available.append(travels[i])
            i += 1

        end_station_time = sys.maxsize
        travel_choose = None

        for travel in travels_available:
            if end_station_time > travel.station_time.passenger_in_train_time:
                end_station_time = travel.station_time.passenger_in_train_time
                travel_choose = travel
        # print(stationlist.stations)
        # print("travel:"+str(travel_choose))
        save, _ = Travel_Center.save_travel(travel_choose, None, None, stationlist, linelist, result,travel_center)
        if Travel_Center.train_is_blocking_other_train_in_station(end_station, travel_choose.train, stationlist):
            Travel_Center.clear_station_with_specific_train(end_station, travel_choose.train,
                                                            travel_choose.station_time.passenger_out_train_time,
                                                            linelist, stationlist, result, travel_center)

        return save
