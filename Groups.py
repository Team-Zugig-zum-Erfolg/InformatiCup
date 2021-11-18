from typing import List
from classes.Station import Station
from classes.Line import Line
from classes import Passenger

class Groups:

    route = []
    
    def initial(self,passengers):

        if type(passenger) != list:
            return False
        for passenger in passengers:
            route_number = 0
            added = 0
            for route_searched in route:
                if route_searched[0].getStartStation() == passenger.getStartStation() and route_searched[0].getEndStation() == passenger.getEndStation():
                    route[route_number].append(passenger)
                    added = 1
                    break
                route = route + 1
            if added == 0:
                route.append([passenger])

        return True
            
    def get_priority(self):
        return
    def passengers_arrive(self):
        return
    def print_output(self):
        return
