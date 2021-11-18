from classes import Passenger

class Groups:

    route = []
        
    def initial(self,passengers):

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
                self.route = self.route + 1
            if added == 0:
                self.route.append([passenger])

        return True
            
    def partition(array, start, end, compare_func):

        pivot = array[start]
        low = start + 1
        high = end

        while True:
            while low <= high and compare_func(array[high], pivot):
                high = high - 1

            while low <= high and not compare_func(array[low], pivot):
                low = low + 1

            if low <= high:
                array[low], array[high] = array[high], array[low]
            else:
                break

        array[start], array[high] = array[high], array[start]

        return high
     
    def quick_sort(array, start, end, compare_func):
   
        if start >= end:
            return
        p = partition(array, start, end, compare_func)
        quick_sort(array, start, p-1, compare_func)
        quick_sort(array, p+1, end, compare_func)


    def get_priority(self):
 
        #passenger_list = self #Liste mit den Groups 
        quick_sort(self.route, 0, len(route) - 1, lambda x, y: x.target_round > y.target_round)
    
        for Passenger in route:
            print(Passenger) 

  
    def passengers_arrive(self):
        return
    def print_output(self):
        return


pa1 = Passenger("P1","S1","S2",12,12)
pa2 = Passenger("P2","S1","S2",12,12)


groupstest = Groups()
groupstest.initial([pa1,pa2])



