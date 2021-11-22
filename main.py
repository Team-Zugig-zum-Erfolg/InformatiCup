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
    stations, lines, trains, passengers = input.from_file( "test/test-input-1.txt")

    stationlist = []
    for s in stations:
        stationlist.append(s.to_list())
    linelist = []
    for l in lines:
        linelist.append(l.to_list())
    trainlist = []
    for t in trains:
        trainlist.append(t.to_list())

    travel_center = Travel_Center(stationlist, linelist, trainlist)

    print("test")
    print(stations[0])
    print(stationlist)
    print(linelist)
    print(trainlist)

    return

main()