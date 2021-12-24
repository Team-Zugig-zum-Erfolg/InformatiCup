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
lines = [Line(1,stations[0],stations[1],1,1), Line(2,stations[1],stations[2],1,1), Line(2,stations[2],stations[3],1,1), Line(3,stations[3],stations[4],1,1), Line(4,stations[1],stations[3],1,1) , Line(5,stations[0],stations[2],1,1)]

stationlist = []
for station in stations:
	stationlist.append(station.to_list())

linelist = []
for line in lines:
	linelist.append(line.to_list())

test_linelist = Linelist(linelist)
test_stationlist = Stationlist(stationlist,trains)

test_travelcenter = Travel_Center(stationlist,linelist,trains)
	
class Testing(unittest.TestCase):

	def test_get_stations_by_line(self):
		self.assertEqual(Travel_Center.get_stations_by_line(1), [stations[0] ,stations[1]], [True, -1])
		self.assertEqual(Travel_Center.get_stations_by_line(2), [stations[1], stations[2]], [True, -1])
		self.assertEqual(Travel_Center.get_stations_by_line(3), [stations[2], stations[3]], [True, -1])
		self.assertEqual(Travel_Center.get_stations_by_line(4), [stations[3], stations[4]], [True, -1])
		self.assertEqual(Travel_Center.get_stations_by_line(5), [stations[1], stations[3]], [True, -1])		
	
	def test_find_only_one_line_between_stations(self):
                #(self,start_station_id,end_station_id):   # return [length,[line]]
		self.assertEqual(Travel_Center.find_only_one_line_between_stations(self, 1, 2), [1, [1]])
		self.assertEqual(Travel_Center.find_only_one_line_between_stations(self, 1, 3), [1, [5]])
		self.assertEqual(Travel_Center.find_only_one_line_between_stations(self, 2, 3), [1, [2]])
		self.assertEqual(Travel_Center.find_only_one_line_between_stations(self, 3, 2), [1, [2]])
		self.assertEqual(Travel_Center.find_only_one_line_between_stations(self, 2, 4), [1, [4]])

unittest.main()