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
    groupe_to_many = 0
    while len(groups.route) != 0:
        print("-------------------------------------------------------------")
        if groupe_to_many == 0:
            group = groups.get_priority()
            print("group:"+str(group))
        else:
            print("too many")
            print("group:"+str(group))
            group.pop(len(group) - 1)
        start_station, end_station, group_size = Travel_Center.check_passengers(group)
        print("start_station:"+start_station.get_id_str())
        print("end_station:"+end_station.get_id_str())
        print("")
        start_time_list, trainlist, available = Travel_Center.check_train_in_station(start_station, group_size, stationlist, linelist)
        print("start_time_list:")
        print(start_time_list)
        print("trainlist:")
        print(trainlist)
        if not available:
            print("no train available at station:")
            start_times, trains, start_stations = Travel_Center.check_train_not_in_station(group_size, stationlist)
            print(Travel_Center.check_train_not_in_station(group_size, stationlist))
            print(start_stations)
            Travel_Center.train_move_to_start_station(start_station, trains, start_times, start_stations, stationlist, linelist, result, travel_center)
            continue
        travels = []
        for count in range(len(trainlist)):
            travels.append(travel_center.time_count_train(start_station, end_station, trainlist[count],
                                                          start_time_list[count]))


        for travel in travels:
            print("Station time: "+str(travel.station_time))
            print("Line time: "+str(travel.line_time))
          
            
            
        save = 0
        
        if len(travels):
            while not save:
                print("check travels:")
                print("------------------")
                availables = []
                delay_times = []
                for travel in travels:
                    available, delay_time = Travel_Center.check_line_station(travel, stationlist, linelist)
                    availables.append(available)
                    delay_times.append(delay_time)
                    print("delay_time: "+str(delay_time))
                    print("------------------")
                i = 0
                available_run = 0
                travel_available = []
                print(availables)
                for available in availables:
                    if available:
                        print(i)
                        travel_available.append(travels[i])
                        available_run = 1
                    i += 1

                if available_run:
                    print("save travel")
                    short_time = travel_available[0].station_time.passenger_out_train_time
                    short_travel = travel_available[0]
                    for travel in travel_available:
                        if short_time > travel.station_time.passenger_out_train_time:
                            short_time = travel.station_time.passenger_out_train_time
                            short_travel = travel
                    save, delay_time = Travel_Center.save_travel(short_travel, groups, group,
                                                                 stationlist, linelist, result)
                    
                    
                    
                else:
                    i = 0
                    print("delay travel")
                    print(travels)
                    for travel in travels:
                        Travel_Center.delay_travel(travel, delay_times[i])
                        i += 1
            groupe_to_many = 0
        else:
            groupe_to_many = 1

    i = 0
    for station in stationlist.stations:
        print("S"+str(i)+""+str(station))
        i += 1

    i = 0
    for line in linelist.lines:
        print("L"+str(i)+""+str(line))
        i += 1
        

    groups.print_output()
    print(result.to_output_text())
    return


main()
