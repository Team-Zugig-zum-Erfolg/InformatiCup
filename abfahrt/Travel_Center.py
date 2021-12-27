import math # This module provides access to the mathematical functions defined by the C standard. (https://docs.python.org/3/library/math.html)
import sys # This module provides access to some variables used or maintained by the interpreter and to functions that interact strongly with the interpreter. (https://docs.python.org/3/library/sys.html)

from abfahrt.Stationlist import Stationlist
from abfahrt.Linelist import Linelist
from abfahrt.classes.Travel import Travel
from abfahrt.classes.TrainInLine import TrainInLine
from abfahrt.classes.TrainInStation import TrainInStation
from abfahrt.classes.Station import Station
from abfahrt.classes.Graph import Graph
from abfahrt.Result import Result


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

GRAPH = Graph()

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
            GRAPH.addNode(station[S_ID])
            for line in line_input_list:
                if line[L_S_ID_START] == station[S_ID]:
                    S_LINEPLAN[station[S_ID]][0].append(line[L_S_ID_END])
                    S_LINEPLAN[station[S_ID]][1].append(line[L_ID])
                    GRAPH.addEdge(station[S_ID],line[L_S_ID_END],line[L_LEN])
                elif line[L_S_ID_END] == station[S_ID]:
                    S_LINEPLAN[station[S_ID]][0].append(line[L_S_ID_START])
                    S_LINEPLAN[station[S_ID]][1].append(line[L_ID])
                    GRAPH.addEdge(station[S_ID],line[L_S_ID_START],line[L_LEN])

    def _get_all_line_station(self, s_station_id, e_station_id, lineplan):
        lineplan = lineplan + [s_station_id]
        if s_station_id == e_station_id:
            return [lineplan]

        lineplans = []
        for node in S_LINEPLAN[s_station_id][0]:
            found=False
            if node not in lineplan:
                for _lineplan in lineplans:
                    if node in _lineplan:
                        found=True
                        break
                if found == True:
                    continue
                if node != e_station_id and e_station_id in S_LINEPLAN[s_station_id][0]:
                    continue
                newpaths = self._get_all_line_station(node, e_station_id, lineplan)
                for newpath in newpaths:
                    lineplans.append(newpath)
        return lineplans

    def _find_lines(self, s_station_id, e_station_id):
        global GRAPH
        out, prev_list = Graph.dijkstra(GRAPH, s_station_id)
        path = [e_station_id]
        Graph.shortest(e_station_id,prev_list,path)
        lineplans = [path[::-1]]
        lines = []
        j = 0
        for lineplan in lineplans:
            lines.append([])
            for i in range(len(lineplan) - 1):
                t=0
                for station in S_LINEPLAN[lineplan[i]][0]:
                    if station == lineplan[i+1]:
                        lines[j].append(S_LINEPLAN[lineplan[i]][1][t])
                        break
                    t += 1
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


    def find_only_one_line_between_stations(self,start_station_id,end_station_id):
        t=0
        line = None
        for next_station_id in S_LINEPLAN[start_station_id][0]:
            if next_station_id == end_station_id:
                line = S_LINEPLAN[start_station_id][1][t]
                break
            t+=1
        length = LINE_INPUT_LIST[line - 1][L_LEN]
        return [length,[line]]

    def time_count_length(self,start_station,end_station):
        length, lines = self.find_best_line(start_station.id, end_station.id)
        return length

    def time_count_train(self, start_station, end_station, train, start_time, use_one_line=False):
        if use_one_line == False:
            length, lines = self.find_best_line(start_station.id, end_station.id)
        else:
            length, lines = self.find_only_one_line_between_stations(start_station.id, end_station.id)
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
            
            current_leave_time = None
            current_passenger_in_time = add_time + self.train_line_time_list[train.id][lines[li]] + 1

            if next_station.id != end_station.id:
                current_leave_time = add_time + self.train_line_time_list[train.id][lines[li]]
                current_passenger_in_time = add_time + self.train_line_time_list[train.id][lines[li]]

            station_times.append(TrainInStation(add_time + self.train_line_time_list[train.id][lines[li]],current_passenger_in_time,train,current_leave_time,next_station.id))                          
            
            add_time += self.train_line_time_list[train.id][lines[li]] + 1

            prev_station = next_station
        
        station_time = TrainInStation(add_time-1, add_time, train, None, end_station.id)

        return Travel(start_time, on_board, line_time, station_time, start_station, end_station, train, station_times, length)

    @staticmethod
    def full_stations_list_not_empty(full_stations_list):
        if full_stations_list == None:
            return False
        for full_stations in full_stations_list:
            if len(full_stations) > 0:
                return True
        return False

    @staticmethod
    def get_stations_by_line(line_id):
        line = LINE_INPUT_LIST[line_id-1]
        station_1 = Station(STATION_INPUT_LIST[line[L_S_ID_START]-1][S_ID],STATION_INPUT_LIST[line[L_S_ID_START]-1][S_CAPACITY])
        station_2 = Station(STATION_INPUT_LIST[line[L_S_ID_END]-1][S_ID],STATION_INPUT_LIST[line[L_S_ID_END]-1][S_CAPACITY])
        return [station_1,station_2]

    @staticmethod
    def check_line_station(travel: Travel, stationlist: Stationlist, linelist: Linelist, result: Result, travel_center):
        line_availables_list = []
        line_time_changes = []
        station_availables_list = []
        station_time_changes = []
        available = True
        station_is_full = False
        full_stations = []
        next_station = travel.start_station
        for travel_in_line in travel.line_time:
            line_available, line_time_change = linelist.compare_free(travel_in_line)
           
            line_availables_list.append(line_available)
            line_time_changes.append(line_time_change)
            next_station = Travel_Center.get_next_station_in_travel(travel,next_station)
            
           
            current_leave_time = None
            current_passenger_in_time = travel_in_line.end + 1

            if next_station.id != travel.end_station.id:
                current_leave_time = travel_in_line.end
                current_passenger_in_time = travel_in_line.end

            s_available, s_time_change = stationlist.compare_free_place(TrainInStation(travel_in_line.end,current_passenger_in_time,travel_in_line.train,current_leave_time,next_station.id))
            if s_available == False and s_time_change == -1: #full
                full_stations.append([next_station,travel_in_line.end]) 
            station_availables_list.append(s_available)
            station_time_changes.append(s_time_change)

          

        station_available, station_time_change = stationlist.compare_free_place(travel.station_time)

        if station_available == False and station_time_change == -1:
            station_is_full = True
            available = False

        station_delay_time = 0
        if not station_available and station_is_full == False:
            station_delay_time = ((station_time_change) - travel.station_time.arrive_train_time)
            available = False

        delay_time = station_delay_time

        
        for i in range(len(travel.line_time)):
            if not line_availables_list[i]:
                available = False
                line_delay_time = line_time_changes[i] - travel.line_time[i].start
                if delay_time < line_delay_time:
                    delay_time = line_delay_time

        
        for i in range(0,len(travel.station_times[1:])):
            if not station_availables_list[i]:
                    available = False
                    current_station_delay_time = station_time_changes[i] - travel.station_times[i+1].arrive_train_time
                    if delay_time < current_station_delay_time:
                        delay_time = current_station_delay_time

        return [available, delay_time, station_is_full, full_stations]

    @staticmethod
    def delay_travel(travel: Travel, delay_time):
        travel.start_time = travel.start_time + delay_time
        travel.on_board = travel.on_board + delay_time
        for i in range(0, len(travel.line_time)):
            travel.line_time[i].start = travel.line_time[i].start + delay_time
            travel.line_time[i].end = travel.line_time[i].end + delay_time
        for i in range(0, len(travel.station_times)):
            travel.station_times[i].arrive_train_time = travel.station_times[i].arrive_train_time + delay_time
            travel.station_times[i].passenger_in_train_time = travel.station_times[i].passenger_in_train_time + delay_time
            if travel.station_times[i].leave_time != None:
                travel.station_times[i].leave_time = travel.station_times[i].leave_time + delay_time
        travel.station_time.arrive_train_time = travel.station_time.arrive_train_time + delay_time
        travel.station_time.passenger_in_train_time = travel.station_time.passenger_in_train_time + delay_time

    @staticmethod
    def save_travel(travel: Travel, groups, passengers, stationlist: Stationlist, linelist: Linelist, result: Result, travel_center, train_to_replace=False):
        enable, _, full, _ = Travel_Center.check_line_station(travel, stationlist, linelist, result, travel_center)
        if enable or (full == True and train_to_replace):
            
            stationlist.add_train_leave_time(travel.train, travel.on_board, travel.start_station.id, result)

            for train_in_line in travel.line_time:
                save = linelist.add_new_train_in_line(train_in_line)
                if save:
                    result.save_train_depart(train_in_line.train, train_in_line.start, train_in_line.line_id)

            for train_in_station in travel.station_times[1:len(travel.station_times)-1]:
                stationlist.add_new_train_in_station(train_in_station, None)

            stationlist.add_new_train_in_station(travel.station_time, None, train_to_replace)

            if passengers is not None:
                groups.passengers_arrive(passengers)
                for passenger in passengers:
                    result.save_passenger_board(passenger.id, travel.on_board, travel.train.id)
                    result.save_passenger_detrain(passenger.id, travel.station_time.passenger_in_train_time)
            
            return True
        else:
            return False


    @staticmethod
    def determine_and_save_shortest_travel(travels,groups,passengers,stationlist:Stationlist,linelist:Linelist,result:Result,travel_center):
        save = 0
        if len(travels):
            while not save:
                full_station_list = []
                availables = []
                delay_times = []
                full_end_station = []   #if full_end_station[i]=True, then for travels[i] the end_station is blocked
                                        #blocked = (there are only trains with leave_time=None before the train will arrive)
                
                for travel in travels:
                    available, delay_time, full, full_stations = Travel_Center.check_line_station(travel, stationlist, linelist, result, travel_center)
                    availables.append(available)
                    delay_times.append(delay_time)
                    full_end_station.append(full) #full==1: the end_station is blocked by stopped trains with leave_time=None
                    full_station_list.append(full_stations)

                i=0
                available_run=0
                travel_available = []
                for available in availables:
                    if available:
                        travel_available.append(travels[i])
                        available_run = 1
                    i += 1

                if available_run: 
                    short_time = travel_available[0].station_time.arrive_train_time
                    short_travel = travel_available[0]
                    for travel in travel_available:
                        if short_time > travel.station_time.arrive_train_time:
                            short_time = travel.station_time.arrive_train_time
                            short_travel = travel

                    save = Travel_Center.save_travel(short_travel, groups, passengers, stationlist, linelist, result, travel_center)

                elif 0 not in delay_times and -1 not in delay_times: #travels have to be delayed first, before clearing full stations

                    i=0
                    for travel in travels:
                        Travel_Center.delay_travel(travel, delay_times[i])
                        i += 1   

                elif Travel_Center.full_stations_list_not_empty(full_station_list): #at least one station is blocked on the route
                
                    #free all FULL stations on the route of the shortest travel, so the train of the travel can pass them
                    cleared_stations_ids = []
                    travel_short = None
                    smallest_arrive_time = sys.maxsize
                    t=0
                    i=0
                    for travel in travels:
                        if delay_times[i] == 0 and smallest_arrive_time > travel.station_time.arrive_train_time:
                            travel_short = travel
                            smallest_arrive_time = travel.station_time.arrive_train_time
                            t = i
                        i = i + 1

                    if travel_short != None:
                        for full_station in full_station_list[t]:
                            station_to_clear = full_station[0]
                            arrive_time = full_station[1]
                            if station_to_clear.id in cleared_stations_ids: #prevent clearing a station twice
                                continue
                            Travel_Center.clear_station(station_to_clear,Travel_Center.get_prev_station_in_travel(travel_short,station_to_clear),arrive_time-2,linelist,stationlist,result,travel_center,travel_short.station_times,travel_short.train)
                            cleared_stations_ids.append(station_to_clear.id)
                            break

                else:
                    raise ValueError("Error: no full stations or delayable travels")
                    
        else:
            # error: input is invalid, because no route was found, but all stations have to be connected with each other
            # (so this should never happen)
            raise ValueError("Error: no travels could be found")

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
    def station_is_never_blocked(station, stationlist: Stationlist):
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
    def station_is_in_station_times_list(station, station_times_list):
        for station_time in station_times_list:
            if station.id == station_time.station_id:
                return True
        return False

    @staticmethod
    def get_next_station_in_travel(travel, station):
        neighboor_stations = Travel_Center.get_neighboor_stations(station)
        station_times = travel.station_times
        for i in range(1,len(station_times)):
            if station_times[i-1].station_id == station.id:
                for neighboor_station in neighboor_stations:
                    if station_times[i].station_id == neighboor_station.id:
                        return neighboor_station
        return None

    @staticmethod
    def get_prev_station_in_travel(travel, station):
        neighboor_stations = Travel_Center.get_neighboor_stations(station)
        for i in range(1,len(travel.station_times)):
            if travel.station_times[i].station_id == station.id:
                for neighboor_station in neighboor_stations:
                    if travel.station_times[i-1].station_id == neighboor_station.id:
                        return neighboor_station
        return None

    @staticmethod
    def station_has_more_than_one_free_capcacity(station, stationlist: Stationlist):
        capacities = stationlist.stations[station.id]
        free = 0
        for capacity in capacities:
            if not Stationlist._capacity_is_full(capacity):
                free = free + 1
        return (free >= 2)

    @staticmethod
    def clear_station(end_station, prev_station, arrive_time, linelist:Linelist, stationlist: Stationlist, result: Result,
                      travel_center,stations_to_ignore,train_to_replace=None):
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
        if next_station == None and prev_station != None:
            for neighboor_station in neighboor_stations:
                if neighboor_station.id == prev_station.id:
                    next_station = prev_station
        if next_station == None:
            raise ValueError("clear station error: no station available")  #no neighboor station is free (free = not blocked) and origin station is also not available

        # get the blocking trains in the station (blocking trains = trains in the station with no leave time)
        # a station is only blocked, if all trains in the station have no leave time
        start_times, trains, station = stationlist.read_trains_from_station(end_station.id,False)
        i=0
        for start_time in start_times:
            if start_time < arrive_time:
                start_times[i] = arrive_time
            i = i + 1

        travels = []
        i=0
        for train in trains:
            travels.append(travel_center.time_count_train(end_station, next_station, train,
                                                start_times[i],True))
            i= i + 1
        available = 0
        while not available:
            full_station_list = []
            availables = []
            delay_times = []
            full_end_station = [] #if full_end_station[i]=True, then for travels[i] the end_station is blocked
     
            for travel in travels:
                available_current, delay_time, full, full_stations = Travel_Center.check_line_station(travel, stationlist, linelist, result, travel_center)
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
                    short_time = travel_available[0].station_time.arrive_train_time
                    short_travel = travel_available[0]
                    for travel in travel_available:
                        if short_time > travel.station_time.arrive_train_time:
                            short_time = travel.station_time.arrive_train_time
                            short_travel = travel
            
                    Travel_Center.save_travel(short_travel, None, None, stationlist, linelist, result, travel_center)
                    available = 1
            elif False in full_end_station or 0 not in delay_times: # end_station is for at least one travel free (so not blocked)
                    i = 0
                    for travel in travels:
                        Travel_Center.delay_travel(travel, delay_times[i])
                        i += 1
            elif next_station.id == prev_station.id:
                    short_time = sys.maxsize
                    short_travel = None
                    i=0
                    for travel in travels:
                        if short_time > travel.station_time.arrive_train_time and delay_times[i] == 0:
                            short_time = travel.station_time.arrive_train_time
                            short_travel = travel
                        i = i + 1

                    Travel_Center.save_travel(short_travel, None, None, stationlist, linelist, result, travel_center, train_to_replace)
                    available = 1
            else:
                raise ValueError("clear station error: no station available")  # all neighboor stations are blocked (should actually not happen, because they are checked above)
        return True

    @staticmethod  # move a train to start station
    def train_move_to_start_station(start_station, trains, start_times, start_stations, stationlist: Stationlist, linelist: Linelist,
                                    result: Result, travel_center):
        save = travel_center._train_to_station(start_station, trains, start_times, start_stations, stationlist,
                                               linelist, result, travel_center)
        return save

    @staticmethod
    def _remove_passing_station_trains(start_station,trains, start_times, stationlist: Stationlist): 
        capacities = stationlist.stations[start_station.id]
        i=0
        for train in trains:
            for capacity in capacities:
                for _train_in_station in capacity:
                    if train.id == _train_in_station.train.id:
                        if start_times[i] <= _train_in_station.arrive_train_time:
                            if _train_in_station.arrive_train_time == _train_in_station.passenger_in_train_time:
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

    @staticmethod
    def determine_trains_limit(stations_amount):
        if stations_amount < 50:
            return 50 
        elif stations_amount < 100:
            return 6
        elif stations_amount < 150:
            return 4
        elif stations_amount < 200:
            return 2
        elif stations_amount < 250:
            return 1
        else:
            return 1

    def _train_to_station(self, end_station, trains, start_times, start_stations, stationlist: Stationlist, linelist: Linelist, result: Result, travel_center):
        travels = []

        calling_trains_limit = Travel_Center.determine_trains_limit(len(stationlist.stations))
        if calling_trains_limit > len(trains):
            calling_trains_limit = len(trains)

        for i in range(0, calling_trains_limit):
            start = start_stations[i]
            train = trains[i]
            start_time = start_times[i]
            travels.append(self.time_count_train(start, end_station, train, start_time))

        Travel_Center.determine_and_save_shortest_travel(travels,None,None,stationlist,linelist,result,travel_center)

        return True
