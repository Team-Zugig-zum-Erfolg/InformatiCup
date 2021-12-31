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

lineplans = []


stationlist = []
for station in stations:
	stationlist.append(station.to_list())

linelist = []
for line in lines:
	linelist.append(line.to_list())

test_linelist = Linelist(linelist)
test_stationlist = Stationlist(stationlist,trains)
test_stationlist_times = test_stationlist


test_travelcenter = Travel_Center(stationlist,linelist,trains)
	
class Testing(unittest.TestCase):

	def test_get_stations_by_line(self):
		self.assertEqual(Travel_Center.get_stations_by_line(1), [stations[0] ,stations[1]])
		self.assertEqual(Travel_Center.get_stations_by_line(2), [stations[1], stations[2]])
		self.assertEqual(Travel_Center.get_stations_by_line(3), [stations[2], stations[3]])
		self.assertEqual(Travel_Center.get_stations_by_line(4), [stations[3], stations[4]])
		self.assertEqual(Travel_Center.get_stations_by_line(5), [stations[1], stations[3]])
	   #self.assertEqual(Travel_Center.get_stations_by_line(None)) Wrong input data is inposible 
	
	def test_find_only_one_line_between_stations(self):
				#(self,start_station_id,end_station_id):   # return [length,[line]]
		self.assertEqual(Travel_Center.find_only_one_line_between_stations(self, 1, 2), [1, [1]])
		self.assertEqual(Travel_Center.find_only_one_line_between_stations(self, 1, 3), [1, [5]])
		self.assertEqual(Travel_Center.find_only_one_line_between_stations(self, 2, 3), [1, [2]])
		self.assertEqual(Travel_Center.find_only_one_line_between_stations(self, 3, 2), [1, [2]])
		self.assertEqual(Travel_Center.find_only_one_line_between_stations(self, 2, 4), [1, [4]])
		self.assertEqual(Travel_Center.find_only_one_line_between_stations(self, 4, 2), [1, [4]])

	#def test__get_all_line_station(self):
 #_get_all_line_station(self, s_station_id, e_station_id, lineplan):
	#	self.assertEqual(Travel_Center._get_all_line_station(self, 1, 2, linelist), [1, [4]])
	
	def test_find_lines(self):
		self.assertEqual(Travel_Center._find_lines(self, 1, 2), [[1]])
		self.assertEqual(Travel_Center._find_lines(self, 1, 3), [[5]])
		self.assertEqual(Travel_Center._find_lines(self, 2, 3), [[2]])
		self.assertEqual(Travel_Center._find_lines(self, 3, 2), [[2]])
		self.assertEqual(Travel_Center._find_lines(self, 2, 4), [[4]])
		self.assertEqual(Travel_Center._find_lines(self, 4, 2), [[4]])
	
	#def test_find_best_lines(self):
	#	self.assertEqual(Travel_Center.find_best_line(self, 1, 2), [1, [1]])
	#	self.assertEqual(Travel_Center.find_best_line(self, 1, 3), [1, [1]])
	#	#find_best_line(self, s_station_id, e_station_id):	
	
	#def test_time_count_length(self):
	#	self.assertEqual(Travel_Center.time_count_length(self, 1, 3), [1, [1]])

	def test_station_is_never_blocked(self):
	#station_is_never_blocked(station, stationlist: Stationlist):
		self.assertEqual(Travel_Center.station_is_never_blocked(stations[0], test_stationlist), False)
		self.assertEqual(Travel_Center.station_is_never_blocked(stations[1], test_stationlist), True)
		self.assertEqual(Travel_Center.station_is_never_blocked(stations[2], test_stationlist), True)
		self.assertEqual(Travel_Center.station_is_never_blocked(stations[3], test_stationlist), True)
		self.assertEqual(Travel_Center.station_is_never_blocked(stations[4], test_stationlist), True)
		self.assertEqual(Travel_Center.station_is_never_blocked(stations[5], test_stationlist), True)


	def test__check_capacity(self):
		#def _check_capacity(trains, group_size, start_times, start_stations):
		self.assertEqual(Travel_Center._check_capacity(trains, 15, 3, stations ), False)
 

	#find_best_line(self, s_station_id, e_station_id):







unittest.main()


'''   
	def test_station_is_in_station_times_list(self):
		self.assertEqual(Travel_Center.station_is_in_station_times_list(stations[0], test_stationlist_times), False)
		self.assertEqual(Travel_Center.station_is_in_station_times_list(stations[1], test_stationlist_times), True)
		self.assertEqual(Travel_Center.station_is_in_station_times_list(stations[2], test_stationlist_times), True)
		self.assertEqual(Travel_Center.station_is_in_station_times_list(stations[3], test_stationlist_times), True)
		self.assertEqual(Travel_Center.station_is_in_station_times_list(stations[4], test_stationlist_times), True)
		self.assertEqual(Travel_Center.station_is_in_station_times_list(stations[5], test_stationlist_times), True)
'''   