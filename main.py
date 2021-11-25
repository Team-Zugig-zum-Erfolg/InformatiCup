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
    '''trainlist = []
    for t in trains:
        #trainlist.append(t.to_list())
        pass'''
    trainlist = [[1, 3, 1.18571, 7], [2, 5, 2.94952, 6],
                 [3, 1, 3.37228, 9], [4, 2, 2.23773, 8], [5, None, 1.16584, 9],
                 [6, 2, 3.50270, 5], [7, 5, 1.46495, 9], [8, None, 3.79408, 6],
                 [9, 1, 3.52201, 6], [10, None, 2.90067, 7]]

    print("test")
    print(stationlist)
    print(linelist)
    print(trainlist)

    travel_center = Travel_Center(stationlist, linelist, trainlist)



    return

main()