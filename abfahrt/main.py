from abfahrt import *


def main():
    input_ = Input()

    stations, lines, trains, passengers = input_.from_stdin()

    if not input_.check_input():
        print("INVALID INPUT: Not enough or invalid objects given!")
        return

    result = Result(input_)

    linelist = Linelist(lines)
    stationlist = Stationlist(stations, trains, result)
    travel_center = Travel_Center(trains, stationlist, linelist, result)

    groups = Groups(passengers)

    if not travel_center.check_plan():
        print("INVALID INPUT: Not all stations connected!")
        return

    while len(groups.route) != 0:

        group = groups.get_priority()

        start_station, end_station, group_size = travel_center.check_passengers(
            group)
        start_time_list, trainlist, available, train_capacity_in_station, max_train_capacity = travel_center.check_train_in_station(
            start_station, group_size)

        if not available:
            start_times, trains, start_stations, capacity_enable = travel_center.check_train_not_in_station(
                group_size)
            if capacity_enable:
                travel_center.train_move_to_start_station(
                    start_station, trains, start_times, start_stations, groups)
            else:
                if len(group) == 1:
                    print("INVALID INPUT: capacity of all trains too low!")
                    return
                groups.split_group(
                    group, train_capacity_in_station, max_train_capacity)
            continue

        route_length = travel_center.time_count_length(
            start_station, end_station)

        if not travel_center.check_valid_train_exist_in_stations(groups.max_size):
            start_times, trainlist, start_stations, capacity_enable = travel_center.check_train_not_in_station(
                groups.max_size)
            if capacity_enable:
                travel_center.train_move_to_start_station(
                    start_station, trainlist, start_times, start_stations, groups)
            else:
                print("INVALID INPUT: capacity of all trains too low!")
                return
            continue

        train_fastest, train_fastest_start_time = travel_center.get_fastest_train_by_start_times_and_route_length(
            trainlist, start_time_list, route_length)

        travel_fastest = travel_center.time_count_train(
            start_station, end_station, train_fastest, train_fastest_start_time)
        travels = [travel_fastest]

        travel_center.determine_and_save_shortest_travel(
            travels, groups, group)

    print(result.to_output_text())
    result.to_file_same()
    return
