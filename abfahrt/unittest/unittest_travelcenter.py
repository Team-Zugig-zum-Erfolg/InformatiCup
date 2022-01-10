import unittest

from abfahrt.Travel_Center import Travel_Center
from abfahrt.classes.TrainInStation import TrainInStation
from abfahrt.classes.Station import Station
from abfahrt.classes.Train import Train
from abfahrt.classes.Line import Line
from abfahrt.Linelist import Linelist
from abfahrt.Stationlist import Stationlist

__unittest = True


stations = [Station(1, 1), Station(2, 1), Station(
    3, 2),  Station(4, 2), Station(5, 3), Station(6, 3)]
trains = [Train(1, Station(1, 1), 1, 10), Train(2, Station(3, 2), 1, 10), Train(
    3, Station(5, 3), 1, 10), Train(4, Station(6, 3), 1, 10)]
lines = [Line(1, stations[0], stations[1], 1, 1), Line(2, stations[1], stations[2], 1, 1), Line(2, stations[2], stations[3], 1, 1), Line(
    3, stations[3], stations[4], 1, 1), Line(4, stations[1], stations[3], 1, 1), Line(5, stations[0], stations[2], 1, 1)]

lineplans = []


test_linelist = Linelist(lines)
test_stationlist = Stationlist(stations, trains, None)


test_travelcenter = Travel_Center(
    trains, test_stationlist, test_linelist, None)


class Testing_Travel_Center(unittest.TestCase):

    def test_get_stations_by_line(self):
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
   # self.assertEqual(test_travelcenter.get_stations_by_line(None)) Wrong input data is inposible

    def test_find_only_one_line_between_stations(self):
        # (self,start_station_id,end_station_id):   # return [length,[line]]
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

    # def test_find_best_lines(self):
    #	self.assertEqual(test_travelcenter.find_best_line(self, 1, 2), [1, [1]])
    #	self.assertEqual(test_travelcenter.find_best_line(self, 1, 3), [1, [1]])
    #	#find_best_line(self, s_station_id, e_station_id):

    # def test_time_count_length(self):
    #	self.assertEqual(test_travelcenter.time_count_length(self, 1, 3), [1, [1]])

    def test_station_is_never_blocked(self):
        # station_is_never_blocked(station, stationlist: Stationlist):
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