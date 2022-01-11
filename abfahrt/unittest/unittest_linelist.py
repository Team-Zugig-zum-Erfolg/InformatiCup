import unittest
import sys
import os

from abfahrt.Linelist import Linelist
from abfahrt.classes.Train import Train
from abfahrt.classes.Station import Station
from abfahrt.classes.Line import Line
from abfahrt.classes.TrainInLine import TrainInLine

__unittest = True

stations = [Station(1, 1), Station(2, 2), Station(3, 1)]
lines = [Line(1, stations[0], stations[2], 2, 1), Line(
    2, stations[2], stations[1], 2, 1), Line(3, stations[0], stations[1], 2, 1)]
trains = [Train(1, stations[0], 1, 10), Train(2, stations[1], 1, 10), Train(
    3, stations[2], 1, 10), Train(4, stations[1], 1, 10)]

test_linelist = Linelist(lines)

test_linelist.lines[1][0].append(TrainInLine(trains[0], 0, 1, 1))
test_linelist.lines[1][0].append(TrainInLine(trains[1], 4, 5, 1))


class Testing_Linelist(unittest.TestCase):

    "Unittest-Testcases for class Linelist"

    def test_compare_free(self):
        """
        Testcases for compare_free_place()
        """
        self.assertEqual(test_linelist.compare_free(
            TrainInLine(trains[2], 2, 2, 1)), [True, -1])
        self.assertEqual(test_linelist.compare_free(
            TrainInLine(trains[3], 4, 5, 1)), [False, 5])
        self.assertEqual(test_linelist.compare_free(
            TrainInLine(trains[1], 1, 1, 1)), [True, -1])
        self.assertEqual(test_linelist.compare_free(
            TrainInLine(trains[0], 1, 4, 3)), [True, -1])
        self.assertEqual(test_linelist.compare_free(
            TrainInLine(trains[1], 2, 10, 2)), [True, -1])
        self.assertEqual(test_linelist.compare_free(
            TrainInLine(trains[2], 4, 1, 3)), [True, -1])
        self.assertEqual(test_linelist.compare_free(
            TrainInLine(trains[3], 1, 9, 1)), [False, 5])
        self.assertEqual(test_linelist.compare_free(
            TrainInLine(trains[1], 2, 8, 2)), [True, -1])
        self.assertEqual(test_linelist.compare_free(
            TrainInLine(trains[1], 7, 3, 1)), [True, -1])
        self.assertEqual(test_linelist.compare_free(
            TrainInLine(trains[1], 5, 3, 3)), [True, -1])
