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
    # init
    input_ = Input()
    stations, lines, trains, passengers = input_.from_file("test/test-input-1.txt")

    station_input_list = []
    for s in stations:
        station_input_list.append(s.to_list())
    line_input_list = []
    for li in lines:
        line_input_list.append(li.to_list())
    train_input_list = trains
    result = Result()
    # for t in trains:
    # train_input_list.append(t.to_list())

    linelist = Linelist(line_input_list)
    stationlist = Stationlist(station_input_list, train_input_list)
    travel_center = Travel_Center(station_input_list, line_input_list, train_input_list)

    groups = Groups(passengers)
    while len(groups.route) != 0:

        group = groups.get_priority()

        start_station, end_station, group_size = Travel_Center.check_passengers(group)

        start_time_list, trainlist, available = Travel_Center.check_train_in_station(start_station, group_size,
                                                                                     stationlist, linelist)

        if not available:
            start_times, trains, start_stations_for_trains, capacity_enable = Travel_Center.check_train_not_in_station(
                group_size, stationlist)
            if not capacity_enable:
                groups.split_group(group)
                continue
            train_move = travel_center.train_move_to_start_station(start_station, trains, start_times,
                                                                   start_stations_for_trains, stationlist, linelist,
                                                                   result)
            if not train_move:
                groups.split_group(group)
            continue
        travels = []
        for count in range(len(trainlist)):
            travels.append(travel_center.time_count_train(start_station, end_station, trainlist[count],
                                                          start_time_list[count]))
        save = 0

        if len(travels):
            while not save:

                availables = []
                delay_times = []
                for travel in travels:
                    available, delay_time = Travel_Center.check_line_station(travel, stationlist, linelist)
                    availables.append(available)
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
                    print("available_run")
                    print(available_run)
                    short_time = travel_available[0].station_time.passenger_out_train_time
                    short_travel = travel_available[0]
                    for travel in travel_available:
                        if short_time > travel.station_time.passenger_out_train_time:
                            short_time = travel.station_time.passenger_out_train_time
                            short_travel = travel
                    print("save")
                    print(save)
                    save, delay_time = Travel_Center.save_travel(short_travel, groups, group,
                                                                 stationlist, linelist, result)

                else:
                    i = 0
                    for travel in travels:
                        Travel_Center.delay_travel(travel, delay_times[i])
                        i += 1
        else:
            groups.split_group(group)

    groups.print_output()
    print(result.to_output_text())
    return


main()
