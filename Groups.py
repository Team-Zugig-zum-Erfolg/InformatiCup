from typing import List
from classes.Station import Station
from classes.Line import Line
from classes import Passenger

class Groups:

    route = []

    def __init__(self,passengers):

        if type(passengers) != list:
            return False
        for passenger in passengers:
            route_number = 0
            added = 0
            for route_searched in self.route:
                if route_searched[0].get_start_station() == passenger.get_start_station() and route_searched[0].get_end_station() == passenger.get_end_station():
                    self.route[route_number].append(passenger)
                    added = 1
                    break
                route_number = route_number + 1
            if added == 0:
                self.route.append([passenger])

    def _get_min_target_round(self,group):

        min = -1
        for pa in group:
            if min == -1:
                min = pa.get_target_round()
                continue
            if pa.get_target_round() < min:
                min = pa.get_target_round()
        return min

    def get_priority(self):

        if len(self.route) == 0:
        
            return None

        self.route.sort(key=self._get_min_target_round)
        return self.route[0]

    def passengers_arrive(self,group):

        self.route.remove(group)
        return

    def split_group(self,group):

        self.route.remove(group)

        length = len(group)
        middle_index = length // 2

        first_group = group[:middle_index]
        second_group = group[middle_index:]
        if len(first_group) != 0:
            self.route.append(first_group)
        if len(second_group) != 0:
            self.route.append(second_group)
        return

    def print_output(self):
        return
