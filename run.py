from abfahrt import *


def run():
    input_ = Input()
    stations, lines, trains, passengers = input_.from_stdin()
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
        start_time_list, trainlist, available, _, _ = travel_center.check_train_in_station(
            start_station, group_size)

        if not available:
            groups.passengers_arrive(group)
            continue

        route_length = travel_center.time_count_length(
            start_station, end_station)

        train_fastest, train_fastest_start_time = travel_center.get_fastest_train_by_start_times_and_route_length(
            trainlist, start_time_list, route_length)

        travel_fastest = travel_center.time_count_train(
            start_station, end_station, train_fastest, train_fastest_start_time)

        travels = [travel_fastest]

        travel_center.determine_and_save_shortest_travel(
            travels, groups, group)

    print(result.to_output_text())
    return


run()
