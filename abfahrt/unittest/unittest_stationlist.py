import unittest

from abfahrt.classes.TrainInStation import TrainInStation
from abfahrt.classes.Station import Station
from abfahrt.classes.Train import Train
from abfahrt.Stationlist import Stationlist


__unittest = True

stations = [Station(1, 1), Station(2, 1), Station(
    3, 2),  Station(4, 2), Station(5, 3), Station(6, 3)]
trains = [Train(1, Station(1, 1), 1, 10), Train(2, Station(3, 2), 1, 10), Train(
    3, Station(5, 3), 1, 10), Train(4, Station(6, 3), 1, 10)]


test_stationlist = Stationlist(stations, trains, None)

test_stationlist.stations[1][0].append(TrainInStation(0, 1, trains[0], 1, 2))
test_stationlist.stations[2][0].append(
    TrainInStation(4, 4, trains[1], None, 2))
test_stationlist.stations[3][0].append(TrainInStation(4, 5, trains[2], 5, 2))


class Testing_Stationlist(unittest.TestCase):

	def test_between_two_trains(self):
		self.assertEqual(test_stationlist.compare_free_place(TrainInStation(3,3,trains[2],4,2)), [False,-1])
		self.assertEqual(test_stationlist.compare_free_place(TrainInStation(3,3,trains[2],3,2)), [True,-1])
		self.assertEqual(test_stationlist.compare_free_place(TrainInStation(2,3,trains[2],3,2)), [True,-1])
		self.assertEqual(test_stationlist.compare_free_place(TrainInStation(4,3,trains[1],2,1)), [False,-1])
		self.assertEqual(test_stationlist.compare_free_place(TrainInStation(1,7,trains[0],3,1)), [False,-1])
		self.assertEqual(test_stationlist.compare_free_place(TrainInStation(4,4,trains[3],5,3)), [True,-1])
		self.assertEqual(test_stationlist.compare_free_place(TrainInStation(1,7,trains[3],5,3)), [True,-1])
		self.assertEqual(test_stationlist.compare_free_place(TrainInStation(2,7,trains[3],6,3)), [True,-1])
		self.assertEqual(test_stationlist.compare_free_place(TrainInStation(3,99,trains[3],4,1)), [False,-1])
		self.assertEqual(test_stationlist.compare_free_place(TrainInStation(2,2,trains[3],6,1)), [False,-1])
		self.assertEqual(test_stationlist.compare_free_place(TrainInStation(-1,7,trains[0],3,1)), [False,-1])
		self.assertEqual(test_stationlist.compare_free_place(TrainInStation(-1,7,trains[0],-1,-1)), [True,-1])
		self.assertEqual(test_stationlist.compare_free_place(TrainInStation(0,1,trains[3],1,1)), [False,-1])
		self.assertEqual(test_stationlist.compare_free_place(TrainInStation(0,2,trains[2],1,1)), [False,-1])		
		self.assertEqual(test_stationlist.compare_free_place(TrainInStation(3,3,trains[2],2,1)), [False,-1])	
		self.assertEqual(test_stationlist.compare_free_place(TrainInStation(2,7,trains[3],7,3)), [True,-1])
		self.assertEqual(test_stationlist.compare_free_place(TrainInStation(2,7,trains[3],100,3)), [True,-1])
		self.assertEqual(test_stationlist.compare_free_place(TrainInStation(2,7,trains[3],1000000,3)), [True,-1])
		self.assertEqual(test_stationlist.compare_free_place(TrainInStation(3,1,trains[2],5,2)), [False,-1])		
		self.assertEqual(test_stationlist.compare_free_place(TrainInStation(3,3,trains[1],7,1)), [False,-1])	

   		#def _train_in_station_is_free(front_train_leave_time, back_train_in_station: TrainInStation, in_station_time,leave_station_time):
	def test_train_in_station_is_free(self):
		                                                           # arrive_train_time, passenger_in_train_time, train, leave_time, station_id
		self.assertEqual(test_stationlist._train_in_station_is_free(5, (5, 3, trains[0], 10, 1), 3, 11), False)
		self.assertEqual(test_stationlist._train_in_station_is_free(7, (6, 3, trains[0], 7, 1), 3, 7), False)
		self.assertEqual(test_stationlist._train_in_station_is_free(7, (7, 3, trains[0], 7, 1), 3, 7), False)
		self.assertEqual(test_stationlist._train_in_station_is_free(None, (7, 3, trains[0], 7, 1), 3, 7), False)
		self.assertEqual(test_stationlist._train_in_station_is_free(13, (7, 3, trains[0], 7, 1), 3, 7), False)
		self.assertEqual(test_stationlist._train_in_station_is_free(13, (13, 3, trains[1], 13, 3), 3, 13), False)
		self.assertEqual(test_stationlist._train_in_station_is_free(4, (7, 3, trains[0], 7, 1), 3, 7), False)
		self.assertEqual(test_stationlist._train_in_station_is_free(13, (7, 3, trains[0], 7, 1), 3, 7), False)
		#self.assertEqual(test_stationlist._train_in_station_is_free(1, (13, 3, trains[1], 13, 3), 3, 13)," front_train_leave_time < in_station_time and back_train_in_station.arrive_train_time > leave_station_time")
		self.assertEqual(test_stationlist._train_in_station_is_free(8, (7, 3, trains[2], 13, 80), 3, 12), False)

	def test_train_leave_time(self):
		
		#train_leave_time(train_in_station: TrainInStation):
		self.assertEqual(test_stationlist.train_leave_time(TrainInStation(3,3,trains[2],4,2)), 4)	
		self.assertEqual(test_stationlist.train_leave_time(TrainInStation(3,3,trains[2],3,2)), 3)
		self.assertEqual(test_stationlist.train_leave_time(TrainInStation(2,3,trains[2],3,2)), 3)
		self.assertEqual(test_stationlist.train_leave_time(TrainInStation(4,3,trains[1],2,1)), 2)
		self.assertEqual(test_stationlist.train_leave_time(TrainInStation(1,7,trains[0],3,1)), 3)
		self.assertEqual(test_stationlist.train_leave_time(TrainInStation(4,4,trains[3],5,3)), 5)
		self.assertEqual(test_stationlist.train_leave_time(TrainInStation(2,7,trains[3],6,3)), 6)
		self.assertEqual(test_stationlist.train_leave_time(TrainInStation(2,7,trains[3],1000000, 3)), 1000000)
		self.assertEqual(test_stationlist.train_leave_time(TrainInStation(2,7,trains[3],100,3)), 100)
		self.assertEqual(test_stationlist.train_leave_time(TrainInStation(-1,7,trains[0],-1,-1)), -1)
		self.assertEqual(test_stationlist.train_leave_time(TrainInStation(-1,7,trains[0],None,-1)), 7)

unittest.main()
