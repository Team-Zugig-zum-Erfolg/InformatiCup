import unittest, sys, os

path = os.path.abspath(os.getcwd())
sys.path.append(path+'\\..')

from Stationlist import Stationlist
from classes.Train import Train
from classes.Station import Station
from classes.TrainInStation import TrainInStation

__unittest = True

stations = [Station(1,1), Station(2,1), Station(3,2),  Station(4,2), Station(5,3), Station(6,3)]
trains = [Train(1,Station(1,1),1,10), Train(2,Station(3,2),1,10), Train(3,Station(5,3),1,10), Train(4,Station(6,3),1,10)]

stationlist = []

for station in stations:
        stationlist.append(station.to_list())

test_stationlist = Stationlist(stationlist,trains)

test_stationlist.stations[1][0].append(TrainInStation(0,1,trains[0],1,2))
test_stationlist.stations[2][0].append(TrainInStation(4,4,trains[1],None,2))
test_stationlist.stations[3][0].append(TrainInStation(4,5,trains[2],5,2))
	
class Testing(unittest.TestCase):

	def test_between_two_trains(self):
		self.assertEqual(test_stationlist.compare_free_place(TrainInStation(3,3,trains[2],4,2)),[False,-1])
		self.assertEqual(test_stationlist.compare_free_place(TrainInStation(3,3,trains[2],3,2)),[True,-1])
		self.assertEqual(test_stationlist.compare_free_place(TrainInStation(2,3,trains[2],3,2)),[True,-1])
		self.assertEqual(test_stationlist.compare_free_place(TrainInStation(4,3,trains[1],2,1)),[False,-1])
		self.assertEqual(test_stationlist.compare_free_place(TrainInStation(1,7,trains[0],3,1)),[False,-1])
		self.assertEqual(test_stationlist.compare_free_place(TrainInStation(4,4,trains[3],5,3)),[True,-1])
		self.assertEqual(test_stationlist.compare_free_place(TrainInStation(1,7,trains[3],5,3)),[True,-1])
		self.assertEqual(test_stationlist.compare_free_place(TrainInStation(2,7,trains[3],6,3)),[True,-1])
		self.assertEqual(test_stationlist.compare_free_place(TrainInStation(3,99,trains[3],4,1)),[False,-1])
		self.assertEqual(test_stationlist.compare_free_place(TrainInStation(2,2,trains[3],6,1)),[False,-1])
		self.assertEqual(test_stationlist.compare_free_place(TrainInStation(-1,7,trains[0],3,1)),[False,-1])
		self.assertEqual(test_stationlist.compare_free_place(TrainInStation(-1,7,trains[0],-1,-1)),[True,-1])
		self.assertEqual(test_stationlist.compare_free_place(TrainInStation(0,1,trains[3],1,1)),[False,-1])
		self.assertEqual(test_stationlist.compare_free_place(TrainInStation(0,2,trains[2],1,1)),[False,-1])		
		self.assertEqual(test_stationlist.compare_free_place(TrainInStation(3,3,trains[2],2,1)),[False,-1])	
		self.assertEqual(test_stationlist.compare_free_place(TrainInStation(2,7,trains[3],7,3)),[True,-1])
		self.assertEqual(test_stationlist.compare_free_place(TrainInStation(2,7,trains[3],100,3)),[True,-1])
		self.assertEqual(test_stationlist.compare_free_place(TrainInStation(2,7,trains[3],1000000,3)),[True,-1])
		self.assertEqual(test_stationlist.compare_free_place(TrainInStation(3,1,trains[2],5,2)),[False,-1])		
		self.assertEqual(test_stationlist.compare_free_place(TrainInStation(3,3,trains[1],7,1)),[False,-1])	

unittest.main()
