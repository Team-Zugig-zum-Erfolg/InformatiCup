from abfahrt.Stationlist import Stationlist
from abfahrt.Linelist import Linelist
from abfahrt.Input import Input
from abfahrt.Groups import Groups
from abfahrt.Result import Result
from abfahrt.Travel_Center import Travel_Center


def main():
    input_ = Input()
    result = Result()

    stations, lines, trains, passengers = input_.from_stdin()

    linelist = Linelist(lines)
    stationlist = Stationlist(stations, trains, result)
    travel_center = Travel_Center(
        stations, lines, trains, stationlist, linelist, result)

    groups = Groups(passengers)

    if not travel_center.check_plan():
        raise NameError("Not all stations connected!")

    while len(groups.route) != 0:

        group = groups.get_priority()

        start_station, end_station, group_size = travel_center.check_passengers(
            group)
        start_time_list, trainlist, available = travel_center.check_train_in_station(
            start_station, group_size)

        if not available:
            start_times, trains, start_stations, capacity_enable = travel_center.check_train_not_in_station(
                group_size)
            if capacity_enable:
                travel_center.train_move_to_start_station(
                    start_station, trains, start_times, start_stations)
            else:
                if len(group) == 1:
                    raise NameError("Error: Capacity of all trains too low!")
                groups.split_group(group)
            continue

        route_length = travel_center.time_count_length(
            start_station, end_station)

        if not travel_center.check_valid_train_exist_in_stations(groups.max_size):
            start_times, trainlist, start_stations, capacity_enable = travel_center.check_train_not_in_station(
                groups.max_size)
            if capacity_enable:
                travel_center.train_move_to_start_station(
                    start_station, trainlist, start_times, start_stations)
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
