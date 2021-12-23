import unittest, sys, os

path = os.path.abspath(os.getcwd())
sys.path.append(path+'\\..')

from Stationlist import Stationlist
from Linelist import Linelist
from classes.Line import Line
from classes.Train import Train
from classes.Station import Station
from classes.TrainInStation import TrainInStation
from Travel_Center import Travel_Center

__unittest = True


stations = [Station(1,1), Station(2,1), Station(3,2),  Station(4,2), Station(5,3), Station(6,3)]
trains = [Train(1,Station(1,1),1,10), Train(2,Station(3,2),1,10), Train(3,Station(5,3),1,10), Train(4,Station(6,3),1,10)]
lines = [Line(1,stations[0],stations[1],1,1)]

stationlist = []
for station in stations:
        stationlist.append(station.to_list())

linelist = []
for line in lines:
        linelist.append(line.to_list())

test_linelist = Linelist(linelist)
test_stationlist = Stationlist(stationlist,trains)

test_travelcenter = Travel_Center(stationlist,linelist,trains)

test_stationlist.stations[1][0].append(TrainInStation(0,1,trains[0],1,2))
test_stationlist.stations[2][0].append(TrainInStation(4,4,trains[1],None,2))
test_stationlist.stations[3][0].append(TrainInStation(4,5,trains[2],5,2))
	
class Testing(unittest.TestCase):

	def test_get_stations_by_line(self):
		self.assertEqual(Travel_Center.get_stations_by_line(1),[stations[0],stations[1]])

unittest.main()