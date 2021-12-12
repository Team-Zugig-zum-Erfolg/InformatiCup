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
import sys
import argparse


def main():

    # init
    parser = argparse.ArgumentParser()
    parser.add_argument('check',type=str,default="",nargs='?',help="test")
    args = parser.parse_args()
    
    input_ = Input()
    
    if args.check == "":
        stations, lines, trains, passengers = input_.from_file("test/input.txt")
    else:
        stations, lines, trains, passengers = input_.from_file("test/"+ args.check)
         

    station_input_list = []
    for s in stations:
        station_input_list.append(s.to_list())

    line_input_list = []
    for li in lines:
        line_input_list.append(li.to_list())


    train_input_list = trains
    result = Result()
   
    linelist = Linelist(line_input_list)
    stationlist = Stationlist(station_input_list, train_input_list, result)
    travel_center = Travel_Center(station_input_list, line_input_list, train_input_list)

    groups = Groups(passengers)

    while len(groups.route) != 0:

        group = groups.get_priority()

        start_station, end_station, group_size = Travel_Center.check_passengers(group)
        start_time_list, trainlist, available = Travel_Center.check_train_in_station(start_station, group_size, stationlist, linelist)

        if not available:
            start_times, trains, start_stations, capacity_enable = Travel_Center.check_train_not_in_station(group_size, stationlist)
            if capacity_enable:
                Travel_Center.train_move_to_start_station(start_station, trains, start_times, start_stations, stationlist, linelist, result, travel_center)
            else: 
                groups.split_group(group)
            continue

        travels = []
        for count in range(len(trainlist)):
            travels.append(travel_center.time_count_train(start_station, end_station, trainlist[count], start_time_list[count]))
        

        Travel_Center.determine_and_save_shortest_travel(travels,groups,group,stationlist,linelist,result,travel_center)
        
        
    print("Stations:"+str(stationlist.stations))
    print("Lines:"+str(linelist.lines))
    print(result.to_output_text())
    result.to_file()
    result.to_file_same()
    return

main()
