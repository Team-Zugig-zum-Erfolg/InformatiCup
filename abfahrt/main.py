from abfahrt.Stationlist import Stationlist
from abfahrt.Linelist import Linelist
from abfahrt.Input import Input
from abfahrt.Groups import Groups
from abfahrt.Result import Result
from abfahrt.Travel_Center import Travel_Center


def main():
    input_ = Input()

    stations, lines, trains, passengers = input_.from_stdin()

    station_input_list = []
    for s in stations:
        station_input_list.append(s.to_list())

    line_input_list = []
    for li in lines:
        line_input_list.append(li.to_list())

    train_input_list = trains
    result = Result()

    linelist = Linelist(line_input_list)
    stationlist = Stationlist(station_input_list, train_input_list)
    travel_center = Travel_Center(
        station_input_list, line_input_list, train_input_list)

    groups = Groups(passengers)

    while len(groups.route) != 0:

        group = groups.get_priority()

        start_station, end_station, group_size = travel_center.check_passengers(
            group)
        start_time_list, trainlist, available = travel_center.check_train_in_station(
            start_station, group_size, stationlist, linelist)

        if not available:
            start_times, trains, start_stations, capacity_enable = travel_center.check_train_not_in_station(
                group_size, stationlist)
            if capacity_enable:
                travel_center.train_move_to_start_station(
                    start_station, trains, start_times, start_stations, stationlist, linelist, result)
            else:
                if len(group) == 1:
                    raise NameError("Error: Capacity of all trains too low!")
                groups.split_group(group)
            continue

        route_length = travel_center.time_count_length(
            start_station, end_station)

        train_fastest = trainlist[0]
        train_fastest_start_time = start_time_list[0]
        time_all_smallest = start_time_list[0] + \
            route_length/trainlist[0].speed

        for count in range(len(trainlist)):
            time_all = start_time_list[count] + \
                route_length/trainlist[count].speed
            if time_all < time_all_smallest:
                time_all_smallest = time_all
                train_fastest = trainlist[count]
                train_fastest_start_time = start_time_list[count]

        travel_fastest = travel_center.time_count_train(
            start_station, end_station, train_fastest, train_fastest_start_time)
        travels = [travel_fastest]

        travel_center.determine_and_save_shortest_travel(
            travels, groups, group, stationlist, linelist, result)

    print(result.to_output_text())
    result.to_file_same()
    return
