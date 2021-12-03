from Stationlist import Stationlist
from Linelist import Linelist
from Input import Input
from Groups import Groups
from Result import Result
from classes.Travel import Travel
from classes.TrainInLine import TrainInLine
from classes.TrainInStation import TrainInStation
from Travel_Center import Travel_Center
from classes import Train
from classes import Station


def main():
    # init
    input_ = Input()
    stations, lines, trains, passengers = input_.from_file("test/test_other.txt")

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

        start_time_list, trainlist, available = Travel_Center.check_train_in_station(start_station, group_size, stationlist, linelist)

        if not available:

            start_times, trains, start_stations = Travel_Center.check_train_not_in_station(group_size, stationlist)
            if len(trains) != 0:
                #print("group_size:"+str(group_size))
                #print("trains:"+str(trains))
                #print("start_station:"+str(start_stations))
                #print("group:"+str(group))
                Travel_Center.train_move_to_start_station(start_station, trains, start_times, start_stations, stationlist, linelist, result, travel_center)

            else:
                
                #if no train is available, then the passengers group size is too big
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
                full_end_station = [] #if full_end_station[i]=True, then for travels[i] the end_station is blocked (there are only trains with leave_time=None before the train will arrive)
                for travel in travels:
                    available, delay_time, full = Travel_Center.check_line_station(travel, stationlist, linelist)
                    availables.append(available)
                    delay_times.append(delay_time)
                    full_end_station.append(full) #full==1: the end_station is blocked by stopped trains with leave_time=None
                    

                i = 0
                available_run = 0
                travel_available = []

                for available in availables:
                    if available:
                        travel_available.append(travels[i])
                        available_run = 1
                    i += 1

                if available_run:

                    short_time = travel_available[0].station_time.passenger_out_train_time
                    short_travel = travel_available[0]
                    for travel in travel_available:
                        if short_time > travel.station_time.passenger_out_train_time:
                            short_time = travel.station_time.passenger_out_train_time
                            short_travel = travel

                    save, delay_time = Travel_Center.save_travel(short_travel, groups, group, stationlist, linelist, result)

                    #stationlist.stations[2][0].append(TrainInStation(6,7,Train(3,Station(1,2),2,3),None,2))#!!!!!!only for testing!!!!!!!! (simulate a full station)

                    #if the arrived train then blocks other trains, because he stops at the end_station, move the train to another station (clear the end_station)
                    if Travel_Center.train_is_blocking_other_train_in_station(end_station,short_travel.train,stationlist):
                        
                        cleared = Travel_Center.clear_station_with_specific_train(end_station,short_travel.train,short_travel.station_time.passenger_out_train_time,linelist,stationlist,result,travel_center)
 
                        if cleared == False:
                            raise ValueError("Clearing station failed: No free station for clearing available!")

                elif False in full_end_station: #end_station is for at least one travel free (so not blocked)

                    #print(stationlist.stations)
                    #print(travel)
                    i = 0
                    for travel in travels:
                        Travel_Center.delay_travel(travel, delay_times[i])
                        i += 1
                        
                else: #end_station is blocked for all possible travels, so the end_station has to be cleared

                    smallest_arrive_time = travels[0].station_time.passenger_out_train_time + delay_times[0]
                    i=0
                    #calculate the smallest time, when to move a stopped train out of the blocked station
                    for travel in travels:
                        if (travels[i].station_time.passenger_out_train_time + delay_times[i]) < smallest_arrive_time:
                            smallest_arrive_time = travels[i].station_time.passenger_out_train_time + delay_times[i]
                        i += 1
                  
                    cleared = travel_center.clear_station(end_station,start_station,smallest_arrive_time-2,linelist,stationlist,result,travel_center)    
                    
                    if cleared == False:
                        raise ValueError("Clearing station failed: No free station for clearing available!")
                    
                    
        else:
            #error: input is invalid, because no route was found, but all stations have to be connected with each other (so this should never happen)
            pass
        
    print("Stations:"+str(stationlist.stations))
    print("Lines:"+str(linelist.lines))
    print(result.to_output_text())
    return


main()
