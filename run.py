from abfahrt import *


def run():
    input_ = Input()
    result = Result()
    stations, lines, trains, passengers = input_.from_stdin()

    linelist = Linelist(lines)
    stationlist = Stationlist(stations, trains)
    travel_center = Travel_Center(stations, lines, trains)

    groups = Groups(passengers)

    if not travel_center.check_plan():
        raise NameError("Not all stations connected!")

    while len(groups.route) != 0:

        group = groups.get_priority()

        start_station, end_station, group_size = travel_center.check_passengers(
            group)
        start_time_list, trainlist, available = travel_center.check_train_in_station(
            start_station, group_size, stationlist, linelist)

        if not available:
            groups.route.remove(group)
            continue

        route_length = travel_center.time_count_length(
            start_station, end_station)

        train_fastest, train_fastest_start_time = travel_center.get_fastest_train_by_start_times_and_route_length(
            trainlist, start_time_list, route_length)

        travel_fastest = travel_center.time_count_train(
            start_station, end_station, train_fastest, train_fastest_start_time)

        travels = [travel_fastest]

        travel_center.determine_and_save_shortest_travel(
            travels, groups, group, stationlist, linelist, result)

    print(result.to_output_text())
    result.to_file_same()
    return


run()
