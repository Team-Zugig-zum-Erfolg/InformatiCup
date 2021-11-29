import math
import sys

from Stationlist import Stationlist
from Linelist import Linelist
from classes.Travel import Travel
from classes.TrainInLine import TrainInLine
from classes.TrainInStation import TrainInStation
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
            for line in line_input_list:
                self.train_line_time_list[train.id].append(
                    math.ceil(line[L_LEN] / train.speed))
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
        on_board = start_time + 1
        add_time = on_board + 1
        for li in range(len(lines)):
            line_time.append(TrainInLine(train.id, add_time,
                                         add_time + self.train_line_time_list[train.id][lines[li]], lines[li]))
            add_time += self.train_line_time_list[train.id][lines[li]]
        station_time = TrainInStation(add_time, add_time + 1, train, None, end_station.id)

        return Travel(start_time, on_board, line_time, station_time, start_station, end_station, train)

    @staticmethod
    def check_line_station(travel: Travel, stationlist: Stationlist, linelist: Linelist):
        line_availables = []
        line_time_changes = []
        for travel_in_line in travel.line_time:
            line_available, line_time_change = linelist.compare_free(travel_in_line)
            line_availables.append(line_available)
            line_time_changes.append(line_time_change)

        station_available, station_time_change = stationlist.compare_free_place(travel.station_time)

        available = True
        station_delay_time = 0
        if not station_available:
            available = False
            station_delay_time = station_time_change - travel.station_time.passenger_out_train_time
            available = False

        delay_time = station_delay_time
        i = 0
        for a in line_availables:
            if not a:
                available = False
                line_delay_time = line_time_changes[i] - travel.line_time[i].start
                if delay_time < line_delay_time:
                    delay_time = line_delay_time
            i += 1

        return [available, delay_time]

    @staticmethod
    def delay_travel(travel: Travel, delay_time):
        travel.start_time = travel.start_time + delay_time
        travel.on_board = travel.on_board + delay_time
        travel.line_time.start = travel.line_time.start + delay_time
        travel.line_time.end = travel.line_time.end + delay_time
        travel.station_time.passenger_out_train_time = travel.station_time.passenger_out_train_time + delay_time
        travel.station_time.passenger_in_train_time = travel.station_time.passenger_in_train_time + delay_time

    @staticmethod
    def save_travel(travel: Travel, groups, passengers, stationlist: Stationlist, linelist: Linelist, result: Result):
        save, delay_time = Travel_Center.check_line_station(travel, stationlist, linelist)
        print("delay")
        print(delay_time)
        if save:
            print("save")
            for line in travel.line_time:
                save = linelist.add_new_train_in_line(line)
                if save:
                    result.save_train_depart(line.train, line.start, line.line_id)
            save = stationlist.add_train_leave_time(travel.train, travel.on_board, travel.start_station.id)
            if passengers is not None:
                groups.passengers_arrive(passengers)
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
        start_times, trains = stationlist.read_trains_from_station(start_station.id)
        Travel_Center._check_capacity(trains, group_size, start_times, None)
        available = False
        if trains is not None:
            available = True
        return start_times, trains, available

    @staticmethod
    def check_train_not_in_station(group_size, stationlist: Stationlist):  # choose train from other station
        start_times, trains, start_stations = Travel_Center._check_trains_in_all_station(stationlist)
        Travel_Center._check_capacity(trains, group_size, start_times, start_stations)
        return start_times, trains, start_stations

    @staticmethod  # move a train to start station
    def train_move_to_start_station(start_station, trains, start_times, start_stations, stationlist, linelist,
                                    result: Result):
        save = Travel_Center._train_to_station(start_station, trains, start_times, start_stations,
                                               stationlist, linelist, result)
        return save

    @staticmethod
    def _check_capacity(trains, group_size, start_times, start_stations):

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
                if i >= len(trains):
                    break

    @staticmethod
    def _check_trains_in_all_station(stationlist: Stationlist):
        trains = []
        start_times = []
        start_stations = []
        for i in range(1, len(stationlist.stations)):
            start_time, train = stationlist.read_trains_from_station(i)
            for t in train:
                start_stations.append(i)
            start_times += start_time
            trains += train
        return start_times, trains, start_stations

    def _train_to_station(self, end_station, trains, start_times, start_stations, stationlist, linelist,
                          result: Result):
        travels = []
        availables = []
        delay_times = []
        for i in len(trains):
            start = start_stations[i]
            train = trains[i]
            start_time = start_times[i]
            travels.append(self.time_count_train(start, end_station, train, start_time))
        while not availables:  # find travels until minimal 1 travel
            # available, linelist, stationlist, travel, delay_time
            for travel in travels:
                available, delay_time = Travel_Center.check_line_station(travel, stationlist,
                                                                         linelist)
                availables.append(available)
                delay_times.appand(delay_time)

            if not availables:
                for travel in travels:
                    Travel_Center.delay_travel(travel)
        travels_available = []
        i = 0
        for available in availables:
            if available:
                travels_available.append(travels[i])
                i += 1
        end_station_time = sys.maxsize
        travel_choose = Travel()

        for travel in travels_available:
            if end_station_time > travel.start_station.passenger_in_train_time:
                end_station_time = travel.start_station
                travel_choose = travel
        save, _ = Travel_Center.save_travel(travel_choose, None, None, stationlist, linelist, result)
        print("save1")
        print(save)
        return save
