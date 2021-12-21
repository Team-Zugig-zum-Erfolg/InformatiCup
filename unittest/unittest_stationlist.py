import unittest, sys, os

path = os.path.abspath(os.getcwd())
sys.path.append(path+'\\..')

from Stationlist import Stationlist
from classes.Train import Train
from classes.Station import Station
from classes.TrainInStation import TrainInStation

__unittest = True

stations = [Station(1,1), Station(2,1), Station(3,2), Station(3,2), Station(4,2), Station(5,3), Station(6,3)]
trains = [Train(1,Station(1,1),1,10), Train(2,Station(3,2),1,10), Train(3,Station(5,3),1,10), Train(4,Station(6,3),1,10)]]

stationlist = []

for station in stations:
        stationlist.append(station.to_list())

test_stationlist = Stationlist(stationlist,trains)

test_stationlist.stations[2][0].append(TrainInStation(0,1,trains[0],1,2))
test_stationlist.stations[2][0].append(TrainInStation(4,4,trains[1],None,2))
test_stationlist.stations[1][0].append(TrainInStation(4,5,trains[0],5,2))
	
class Testing(unittest.TestCase):

	def test_between_two_trains(self):
		self.assertEqual(test_stationlist.compare_free_place(TrainInStation(3,3,trains[2],4,2)),[False,-1])
		self.assertEqual(test_stationlist.compare_free_place(TrainInStation(3,3,trains[2],3,2)),[True,-1])
		self.assertEqual(test_stationlist.compare_free_place(TrainInStation(2,3,trains[2],3,2)),[True,-1])

		
	def test_delay_time(self):
		self.assertEqual(test_stationlist.compare_free_place(TrainInStation(3,3,trains[1],4,1)),[False,6])
		self.assertEqual(test_stationlist.compare_free_place(TrainInStation(3,3,trains[1],3,1)),[True,-1])
				
unittest.main()
