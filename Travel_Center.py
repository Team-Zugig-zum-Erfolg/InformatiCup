import math
from Stationlist import Stationlist
from Linelist import Linelist
from classes.Travel import Travel
from classes.TrainInLine import TrainInLine
from classes.TrainInStation import TrainInStation



class Travel_Center:
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

    train_line_time_list = []
    LINELIST = []
    STATIONLIST = []
    TRAINLIST = []

    S_LINEPLAN = []

    def __init__(self, stationlist, linelist, trainlist):
        self.train_line_time_list.append([])
        self.LINELIST = linelist;
        self.STATIONLIST = stationlist
        self.TRAINLIST = trainlist
        for train in trainlist:
            self.train_line_time_list.append([])
            for line in linelist:
                self.train_line_time_list[train[self.T_ID]].append(
                    math.ceil(line[self.L_LEN] / train[self.T_SPEED]))
        print(self.train_line_time_list)
        self.S_LINEPLAN.append([])
        self.S_LINEPLAN[0].append([])
        for station in stationlist:
            self.S_LINEPLAN.append([])
            self.S_LINEPLAN[station[self.S_ID]].append([])
            self.S_LINEPLAN[station[self.S_ID]].append([])
            for line in linelist:
                if line[self.L_S_ID_START] == station[self.S_ID]:
                    self.S_LINEPLAN[station[self.S_ID]][0].append(line[self.L_S_ID_END])
                    self.S_LINEPLAN[station[self.S_ID]][1].append(line[self.L_ID])
                elif line[self.L_S_ID_END] == station[self.S_ID]:
                    self.S_LINEPLAN[station[self.S_ID]][0].append(line[self.L_S_ID_START])
                    self.S_LINEPLAN[station[self.S_ID]][1].append(line[self.L_ID])
        print(self.S_LINEPLAN)

    def _get_all_line_station(self, s_station_id, e_station_id, lineplan):
        lineplan = lineplan + [s_station_id]
        if s_station_id == e_station_id:
            return [lineplan]

        lineplans = []
        for node in self.S_LINEPLAN[s_station_id][0]:
            if node not in lineplan:
                newpaths = self.get_all_line_station(node, e_station_id, lineplan)
                for newpath in newpaths:
                    lineplans.append(newpath)
        return lineplans

    def _find_lines(self, s_station_id, e_station_id):
        lineplans = self._get_all_line_station(s_station_id, e_station_id, [])
        lines = []
        print(lineplans)
        j = 0
        for lineplan in lineplans:
            lines.append([])
            for i in range(len(lineplan) - 1):
                for line in self.LINELIST:
                    # print(str(line[self.const_l_station_Id1]) + str(line[self.const_l_station_Id2]) + \
                    # str(lineplan[i]) + str(lineplan[i + 1]))
                    if line[self.L_S_ID_START] == lineplan[i] and line[self.L_S_ID_END] == lineplan[i + 1]:
                        lines[j].append(line[self.L_ID])
                    elif line[self.L_S_ID_END] == lineplan[i] and line[self.L_S_ID_START] == lineplan[i + 1]:
                        lines[j].append(line[self.L_ID])
            j += 1
        return lines

    def find_best_line(self, s_station_id, e_station_id):
        lines = self._find_lines(s_station_id, e_station_id)
        print("end")
        print(lines)
        short_len = 0
        short_line = None
        for line in lines:
            length = 0
            for each in line:
                length += self.LINELIST[each - 1][self.L_LEN]
            if short_len == 0 or short_len > length:
                short_len = length
                short_line = line
        return [short_len, short_line]

    def time_count_train(self, start_station, end_station, train, start_time):
        length, lines = self.find_best_line(start_station, end_station)
        line_time = []
        on_board = start_time + 1
        add_time = on_board + 1
        for l in range(len(lines)):
            line_time.append([])
            line_time[l].append(TrainInLine(train.get_id(), add_time,
                                            add_time + self.train_line_time_list[train.get_id()][lines[l]]), lines[l])
            add_time = add_time + self.train_line_time_list[train.get_id()][lines[l]]
        station_time = TrainInStation(train.get_id(), add_time, end_station, None)

        return Travel(start_time, on_board, line_time, station_time, start_station, end_station, train)

    def check_line_station(travel: Travel, stationlist: Stationlist, linelist: Linelist):
        line_availables = []
        line_time_changes = []
        for line in travel.line_time:
            line_available, line_time_change = linelist.compare_free(line)
            line_availables.append(line_available)
            line_time_changes.append(line_time_change)

        station_available, station_time_change = stationlist.compare_free_place(travel.station_time)

        available = True
        station_delay_time = 0
        if not station_available:
            available = False
            station_delay_time = station_time_change - travel.station_time
            available = False

        delay_time = station_delay_time
        line_delay_time = 0
        i = 0
        for a in line_availables:
            if not a:
                available = False
                line_delay_time = line_time_change[i] - travel.line_time[i]
                if delay_time < line_delay_time:
                    delay_time = line_delay_time
            i += 1

        return [available, linelist, stationlist, travel, delay_time]

    def delay_travel(travel: Travel, delay_time):
        travel.start_time = travel.start_time + delay_time
        travel.on_board = travel.on_board + delay_time
        travel.line_time = travel.line_time + delay_time
        travel.station_time = travel.station_time + delay_time
        travel.start_station = travel.start_station + delay_time
        travel.end_station = travel.end_station + delay_time

        return travel
    def save_travel(travel: Travel, passengers):
        

