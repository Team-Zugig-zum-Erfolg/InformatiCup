import unittest
# The unittest unit testing framework was originally inspired by JUnit and has a similar flavor as major unit testing frameworks in other languages.
# It supports test automation, sharing of setup and shutdown code for tests, aggregation of tests into collections, and independence of the tests from the reporting framework.(https://docs.python.org/3/library/unittest.html)

from abfahrt.Travel_Center import Travel_Center
from abfahrt.classes.TrainInStation import TrainInStation
from abfahrt.classes.Station import Station
from abfahrt.classes.Train import Train
from abfahrt.classes.Line import Line
from abfahrt.Linelist import Linelist
from abfahrt.Stationlist import Stationlist

__unittest = True

stations = [Station(1, 1), Station(2, 1), Station(
    3, 2),  Station(4, 2), Station(5, 3), Station(6, 3), Station(7,4), Station(8,4), Station(9,4), Station(10,3), Station(11,0), Station(12, 3), Station(13,4), Station(14,4), Station(15,4), Station(16,3), Station(17,1), Station(18, 3), Station(19,4), Station(20,4)]
trains = [Train(1, Station(1, 1), 1, 10), Train(2, Station(3, 2), 1, 10), Train(
    3, Station(5, 3), 1, 10), Train(4, Station(6, 3), 1, 10), Train(5, Station(15, 4), 1, 10)]
lines = [Line(1, stations[0], stations[1], 1, 1), Line(2, stations[1], stations[2], 1, 1), Line(2, stations[2], stations[3], 1, 1), Line(
    3, stations[3], stations[4], 1, 1), Line(4, stations[1], stations[3], 1, 1), Line(5, stations[0], stations[2], 1, 1), Line(
    6, stations[2], stations[4], 1, 1), Line(7, stations[4], stations[5], 1, 1), Line(8, stations[5], stations[6], 1, 1), Line(
    9, stations[5], stations[7], 1, 1), Line(10, stations[5], stations[8], 1, 1), Line(11, stations[8], stations[9], 1, 1), Line(
    12, stations[10], stations[8], 1, 1), Line(13, stations[10], stations[11], 1, 1), Line(14, stations[11], stations[12], 1, 1), Line(
    15, stations[12], stations[13], 1, 1), Line(16, stations[13], stations[4], 1, 1), Line(17, stations[4], stations[6], 1, 1), Line(
    16, stations[6], stations[14], 1, 1), Line(17, stations[14], stations[15], 1, 1), Line(18, stations[15], stations[9], 1, 1), Line(
    19, stations[2], stations[13], 1, 1), Line(20, stations[9], stations[10], 1, 1)]

test_linelist = Linelist(lines)
test_stationlist = Stationlist(stations, trains, None)
test_travelcenter = Travel_Center(
    trains, test_stationlist, test_linelist, None)
test_station_times = [TrainInStation(
    0, 1, trains[0], 1, 1), TrainInStation(6, 1, trains[2], 1, 2), TrainInStation(15, 15, trains[4], 7, 2)]
test_station_times2 = []

class Testing_Travel_Center(unittest.TestCase):

    "Unittest-Testcases for class Travel_Center"

    def test_get_stations_by_line(self):
        """
        Testcases for get_stations_by_line()
        """
        self.assertEqual(test_travelcenter.get_stations_by_line(1), [
                         stations[0], stations[1]])
        self.assertEqual(test_travelcenter.get_stations_by_line(2), [
                         stations[1], stations[2]])
        self.assertEqual(test_travelcenter.get_stations_by_line(3), [
                         stations[2], stations[3]])
        self.assertEqual(test_travelcenter.get_stations_by_line(4), [
                         stations[3], stations[4]])
        self.assertEqual(test_travelcenter.get_stations_by_line(5), [
                         stations[1], stations[3]])
        self.assertEqual(test_travelcenter.get_stations_by_line(6), [
                         stations[0], stations[2]])
        self.assertEqual(test_travelcenter.get_stations_by_line(7), [
                         stations[2], stations[4]])
        self.assertEqual(test_travelcenter.get_stations_by_line(8), [
                         stations[4], stations[5]])
        self.assertEqual(test_travelcenter.get_stations_by_line(9), [
                         stations[5], stations[6]])
        self.assertEqual(test_travelcenter.get_stations_by_line(10), [
                         stations[5], stations[7]])
        self.assertEqual(test_travelcenter.get_stations_by_line(11), [
                         stations[5], stations[8]])
        self.assertEqual(test_travelcenter.get_stations_by_line(12), [
                         stations[8], stations[9]]) 
        self.assertEqual(test_travelcenter.get_stations_by_line(13), [
                        stations[10], stations[8]])  
        self.assertEqual(test_travelcenter.get_stations_by_line(14), [
                        stations[10], stations[11]])    
        self.assertEqual(test_travelcenter.get_stations_by_line(15), [
                        stations[11], stations[12]]) 
        self.assertEqual(test_travelcenter.get_stations_by_line(16), [
                        stations[12], stations[13]])    
        self.assertEqual(test_travelcenter.get_stations_by_line(17), [
                        stations[13], stations[4]])  
        self.assertEqual(test_travelcenter.get_stations_by_line(18), [
                        stations[4], stations[6]])        
        self.assertEqual(test_travelcenter.get_stations_by_line(19), [
                        stations[6], stations[14]])  
        self.assertEqual(test_travelcenter.get_stations_by_line(20), [
                        stations[14], stations[15]])  

    def test_find_only_one_line_between_stations(self):
        """
        Testcases for find_only_one_line_between_stations()
        """
        self.assertEqual(
            test_travelcenter.find_only_one_line_between_stations(1, 2), [1, [1]])
        self.assertEqual(
            test_travelcenter.find_only_one_line_between_stations(1, 3), [1, [5]])
        self.assertEqual(
            test_travelcenter.find_only_one_line_between_stations(2, 3), [1, [2]])
        self.assertEqual(
            test_travelcenter.find_only_one_line_between_stations(3, 2), [1, [2]])
        self.assertEqual(
            test_travelcenter.find_only_one_line_between_stations(2, 4), [1, [4]])
        self.assertEqual(
            test_travelcenter.find_only_one_line_between_stations(4, 2), [1, [4]])
        self.assertEqual(
            test_travelcenter.find_only_one_line_between_stations(4, 2), [1, [4]])
        self.assertEqual(
            test_travelcenter.find_only_one_line_between_stations(3, 4), [1, [2]])
        self.assertEqual(
            test_travelcenter.find_only_one_line_between_stations(4, 5), [1, [3]])
        self.assertEqual(
            test_travelcenter.find_only_one_line_between_stations(5, 6), [1, [7]])

        self.assertEqual(
            test_travelcenter.find_only_one_line_between_stations(6, 7), [1, [8]])
        self.assertEqual(
            test_travelcenter.find_only_one_line_between_stations(6, 9), [1, [10]])
        self.assertEqual(
            test_travelcenter.find_only_one_line_between_stations(6, 8), [1, [9]])
        self.assertEqual(
            test_travelcenter.find_only_one_line_between_stations(6, 5), [1, [7]])
        self.assertEqual(
            test_travelcenter.find_only_one_line_between_stations(4, 3), [1, [2]])
        self.assertEqual(
            test_travelcenter.find_only_one_line_between_stations(5, 4), [1, [3]])
        self.assertEqual(            
            test_travelcenter.find_only_one_line_between_stations(9, 6), [1, [10]])
        self.assertEqual(            
            test_travelcenter.find_only_one_line_between_stations(8, 6), [1, [9]])
        self.assertEqual(
            test_travelcenter.find_only_one_line_between_stations(7, 6), [1, [8]])
        self.assertEqual(
            test_travelcenter.find_only_one_line_between_stations(4, 3), [1, [2]])
        self.assertEqual(
            test_travelcenter.find_only_one_line_between_stations(9, 10), [1, [11]])
        
        self.assertEqual(
            test_travelcenter.find_only_one_line_between_stations(10, 11), [1, [20]])
        self.assertEqual(
            test_travelcenter.find_only_one_line_between_stations(9, 11), [1, [12]])
        self.assertEqual(
            test_travelcenter.find_only_one_line_between_stations(3, 14), [1, [19]])
        self.assertEqual(
            test_travelcenter.find_only_one_line_between_stations(13, 14), [1, [15]])
        self.assertEqual(
            test_travelcenter.find_only_one_line_between_stations(12, 13), [1, [14]])
        self.assertEqual(
            test_travelcenter.find_only_one_line_between_stations(11, 12), [1, [13]])
        self.assertEqual(
            test_travelcenter.find_only_one_line_between_stations(14, 5), [1, [16]])
        self.assertEqual(
            test_travelcenter.find_only_one_line_between_stations(7, 5), [1, [17]])
        self.assertEqual(
            test_travelcenter.find_only_one_line_between_stations(7, 15), [1, [16]])
        self.assertEqual(
            test_travelcenter.find_only_one_line_between_stations(15, 16), [1, [17]])
        self.assertEqual(
            test_travelcenter.find_only_one_line_between_stations(16, 10), [1, [18]])

        self.assertEqual(
            test_travelcenter.find_only_one_line_between_stations(11, 10), [1, [20]])
        self.assertEqual(
            test_travelcenter.find_only_one_line_between_stations(11, 9), [1, [12]])
        self.assertEqual(
            test_travelcenter.find_only_one_line_between_stations(14, 3), [1, [19]])
        self.assertEqual(
            test_travelcenter.find_only_one_line_between_stations(14, 13), [1, [15]])
        self.assertEqual(
            test_travelcenter.find_only_one_line_between_stations(13, 12), [1, [14]])
        self.assertEqual(
            test_travelcenter.find_only_one_line_between_stations(12, 11), [1, [13]])
        self.assertEqual(
            test_travelcenter.find_only_one_line_between_stations(5, 14), [1, [16]])
        self.assertEqual(
            test_travelcenter.find_only_one_line_between_stations(5, 7), [1, [17]])
        self.assertEqual(
            test_travelcenter.find_only_one_line_between_stations(15, 7), [1, [16]])
        self.assertEqual(
            test_travelcenter.find_only_one_line_between_stations(16, 15), [1, [17]])
        self.assertEqual(
            test_travelcenter.find_only_one_line_between_stations(10, 16), [1, [18]])
       
    def test_station_is_never_blocked(self):
        """
        Testcases for station_is_never_blocked()
        """
        self.assertEqual(test_travelcenter.station_is_never_blocked(
            stations[0]), False)
        self.assertEqual(test_travelcenter.station_is_never_blocked(
            stations[1]), True)
        self.assertEqual(test_travelcenter.station_is_never_blocked(
            stations[2]), True)
        self.assertEqual(test_travelcenter.station_is_never_blocked(
            stations[3]), True)
        self.assertEqual(test_travelcenter.station_is_never_blocked(
            stations[4]), True)
        self.assertEqual(test_travelcenter.station_is_never_blocked(
            stations[5]), True)
        self.assertEqual(test_travelcenter.station_is_never_blocked(
            stations[6]), True)
        self.assertEqual(test_travelcenter.station_is_never_blocked(
            stations[7]), True)
        self.assertEqual(test_travelcenter.station_is_never_blocked(
            stations[8]), True)
        self.assertEqual(test_travelcenter.station_is_never_blocked(
            stations[9]), True)
        self.assertEqual(test_travelcenter.station_is_never_blocked(
            stations[10]), False)
        self.assertEqual(test_travelcenter.station_is_never_blocked(
            stations[11]), True)
        self.assertEqual(test_travelcenter.station_is_never_blocked(
            stations[12]), True)
        self.assertEqual(test_travelcenter.station_is_never_blocked(
            stations[13]), True)
        self.assertEqual(test_travelcenter.station_is_never_blocked(
            stations[14]), True)
        self.assertEqual(test_travelcenter.station_is_never_blocked(
            stations[15]), True)
        self.assertEqual(test_travelcenter.station_is_never_blocked(
            stations[16]), True)
        self.assertEqual(test_travelcenter.station_is_never_blocked(
            stations[17]), True)
        self.assertEqual(test_travelcenter.station_is_never_blocked(
            stations[18]), True)
        self.assertEqual(test_travelcenter.station_is_never_blocked(
            stations[19]), True)

    def test_station_is_in_station_times_list(self):
        """
        Testcases for station_is_in_station_times_list()
        """
        self.assertEqual(
            test_travelcenter.station_is_in_station_times_list(stations[0], test_station_times), True) 
        self.assertEqual(
            test_travelcenter.station_is_in_station_times_list(stations[1], test_station_times), True)      
        self.assertEqual(
            test_travelcenter.station_is_in_station_times_list(stations[1], test_station_times), True)       
        self.assertEqual(
            test_travelcenter.station_is_in_station_times_list(stations[2], test_station_times), False)
        self.assertEqual(
            test_travelcenter.station_is_in_station_times_list(stations[3], test_station_times), False)
        self.assertEqual(
            test_travelcenter.station_is_in_station_times_list(stations[4], test_station_times), False)
        self.assertEqual(
            test_travelcenter.station_is_in_station_times_list(stations[5], test_station_times), False)
        self.assertEqual(
            test_travelcenter.station_is_in_station_times_list(stations[6], test_station_times), False)
        self.assertEqual(
            test_travelcenter.station_is_in_station_times_list(stations[7], test_station_times), False)
        self.assertEqual(
            test_travelcenter.station_is_in_station_times_list(stations[8], test_station_times), False)
        self.assertEqual(
            test_travelcenter.station_is_in_station_times_list(stations[9], test_station_times), False)
        self.assertEqual(
            test_travelcenter.station_is_in_station_times_list(stations[10], test_station_times), False)
        self.assertEqual(
            test_travelcenter.station_is_in_station_times_list(stations[11], test_station_times), False)
        self.assertEqual(
            test_travelcenter.station_is_in_station_times_list(stations[12], test_station_times), False)
        self.assertEqual(
            test_travelcenter.station_is_in_station_times_list(stations[13], test_station_times), False)
        self.assertEqual(
            test_travelcenter.station_is_in_station_times_list(stations[14], test_station_times), False)
        self.assertEqual(
            test_travelcenter.station_is_in_station_times_list(stations[15], test_station_times), False)
        self.assertEqual(
            test_travelcenter.station_is_in_station_times_list(stations[16], test_station_times), False)
        self.assertEqual(
            test_travelcenter.station_is_in_station_times_list(stations[17], test_station_times), False)
        self.assertEqual(
            test_travelcenter.station_is_in_station_times_list(stations[18], test_station_times), False)
        self.assertEqual(
            test_travelcenter.station_is_in_station_times_list(stations[19], test_station_times), False)

















