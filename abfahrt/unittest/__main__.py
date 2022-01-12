import unittest
# The unittest unit testing framework was originally inspired by JUnit and has a similar flavor as major unit testing frameworks in other languages.
# It supports test automation, sharing of setup and shutdown code for tests, aggregation of tests into collections, and independence of the tests from the reporting framework.(https://docs.python.org/3/library/unittest.html)

from abfahrt.unittest.unittest_linelist import Testing_Linelist
from abfahrt.unittest.unittest_stationlist import Testing_Stationlist
from abfahrt.unittest.unittest_travelcenter import Testing_Travel_Center

__unittest = True

unittest.TestCase.shortDescription = lambda x: None

if __name__ == '__main__':
    unittest.main()
