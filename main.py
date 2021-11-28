from Stationlist import Stationlist
from Linelist import Linelist
from Input import Input
from Groups import Groups
from Result import Result
from classes.Travel import Travel
from classes.TrainInLine import TrainInLine
from classes.TrainInStation import TrainInStation
from Travel_Center import Travel_Center


def main():
    input = Input()
    stations, lines, trains, passengers = input.from_file("test/test-input-1.txt")

    station_input_list = []
    for s in stations:
        station_input_list.append(s.to_list())
    line_input_list = []
    for l in lines:
        line_input_list.append(l.to_list())
    '''train_input_list = []
    for t in trains:
        #train_input_list.append(t.to_list())
        pass'''
    train_input_list = [[1, 3, 1.18571, 7], [2, 5, 2.94952, 6],
                        [3, 1, 3.37228, 9], [4, 2, 2.23773, 8], [5, None, 1.16584, 9],
                        [6, 2, 3.50270, 5], [7, 5, 1.46495, 9], [8, None, 3.79408, 6],
                        [9, 1, 3.52201, 6], [10, None, 2.90067, 7]]

    print("test")
    '''print(stationlist)
    print(linelist)
    print(trainlist)'''
    linelist = Linelist(line_input_list)
    stationlist = Stationlist(station_input_list)
    travel_center = Travel_Center(station_input_list, line_input_list, train_input_list)
    groups = Groups(passengers)
    start_station, end_station = travel_center.check_passengers(groups.get_priority())
    start_time_list, trainlist = check_train_instation = start_station
    for count in len(trainlist):
        travellist = travel_center.time_count_train(start_station, end_station, start_time_list[count],
                                                    trainlist[count])

    availables = []
    delay_times = []
    travels = []
    for travel in travellist:
        available, linelist, stationlist, travel, delay_time = travel_center.check_line_station(travel, stationlist,
                                                                                                linelist)
        availables.append(available)
        travels.append(travel)
        delay_times.append(delay_time)
    i = 0
    available_run = 0
    travel_available = []
    for available in availables:
        if available:
            travel_available.append(travels[i])
            available_run = 1
        i += 1

    if available_run:
        short_time = travel_available[0].end_station
        short_travel = travel_available[0]
        for travel in travel_available:
            if short_time > travel.end_station:
                short_time = travel.end_station
                short_travel = travel
    else:
        for i in range(len(travels)):
            travels[i] = travel_center.delay_travel(travels[i], delay_times[i])

    save, groups, delay_time, stationlist, linelist = travel_center.save_travel(short_travel, groups, stationlist, linelist)

    return


main()
