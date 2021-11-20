from typing import List
from classes.Station import Station
from classes.Line import Line
from classes.Passenger import Passenger
from classes.Train import Train
from Input import Input
from Stationlist import Stationlist
from Linelist import Linelist
from Trainlist import Trainlist
from Groups import Groups
from Travel_Center import Travel_Center

class Algo:

	input_manager = None
	stationlist_manager = None
	linelist_manager = None
	trainlist_manager = None
	groups_manager = None
	travel_center = None

	def __init__(self):
		self.input_manager = Input()
		self.stationlist_manager = Stationlist()
		self.linelist_manager = Linelist()
		self.trainlist = Trainlist()
		self.groups_manager = Groups()
		self.travel_center = Travel_Center()


	def _get_fastest_train_with_valid_capacity(self,route_data_list,passengers):
  
		train_max_fast = None
		end_time_min = 100000000 # -> inf
  
  
		for route_data in route_data_list:
			if route_data[1] == -1: #there is no route for this train, so ignore this train (happens very uncommon)
				continue
			elif not self.travel_center.check_capacity_train(route_data[0],route_data[1],route_data[2],passengers):
				continue
			if route_data[2] < end_time_min: #is this the fastest route with this train, in contrast to the other trains
				end_time_min = route_data[2]
				train_max_fast = route_data[0]
        
		return [train_max_fast,end_time_min]
  

	def run(self):
		self.input_manager.from_file("test/test-input-1.txt") #including station, lines and etc. from a file
    
  
    
		stationlist = self.input_manager.output_stationlist()
		linelist = self.input_manager.output_linelist()
		trainlist = self.input_manager.output_trainlist()
		passengerlist = self.input_manager.output_passengerlist()

		self.travel_center.initial(stationlist,linelist,trainlist)

		self.groups_manager.initial(passengerlist)

    
		while self.groups_manager.get_priority():
			group_with_prio = self.groups_manager.get_priority() #passenger group with the highest prio
			start_station = group_with_prio[0].get_start_station()
			end_station = group_with_prio[0].get_end_station()
      
			if self.travel_center.callable_trains(start_station):
      
				trains_available = self.travel_center.callable_trains(start_station) #trains_available[n] = [train1:class Train,....]
        
				route_data_list = [] #list, which conatins the the route data calculated by travel_center.determine_route()
        
				for train in trains_available:

					#travel_center.determine_route(train,start,end) -> [train:class Train,start_time:int,end_time:int]
					route_data_list.append(self.travel_center.determine_route(train,start_station,end_station))
                                        
				#self._get_fastest_train_with_valid_capacity(route_data_list,group_with_prio) -> [train_fastest:class Train,earliest_end_time:int]
				train_fastest_and_time = self._get_fastest_train_with_valid_capacity(route_data_list,group_with_prio)
        
				if train_fastest_and_time[0] != None: #if there is a train with enough capacity
          
					self.travel_center.save_route(train_fastest_and_time[0],start_station,end_station,group_with_prio)
        
					#if the ending station (where the passengers arrived and the train stays now) is full, check the capacities of the neighbor or other stations, where this train can move away, to not block other trains, which want to pass this station
					travel_center.optimize_full_station(train_fastest_and_time[0],end_station) 
        
					#remove passenger group from Groups
					self.groups_manager.passengers_arrive(group_with_prio)
          
					continue
      
      
				trains_callable_not_in_move = self.travel_center.callable_trains_not_in_move(start_station) #trains_callable_not_in_move = [[train1:class Train,station:class Station],....]  
				trains_callable_in_move = self.travel_center.callable_trains_in_move(start_station,end_station) #trains_callable_in_move = [[train1:class Train,station:class Station],....]
          
				route_data_list_not_move = []
				route_data_list_move = []    
          
				for train_and_time in trains_callable_not_in_move:
					route_data_list_not_move.append(self.travel_center.determine_route(train_and_time[0],train_and_time[1],end_station))
          
				for train_and_time in trains_callable_in_move:
					route_data_list_move.append(self.travel_center.determine_route(train_and_time[0],train_and_time[1],end_station))

				#self._get_fastest_train_with__valid_capacity(route_data_list,group_with_prio) -> [train_fastest:class Train,earliest_end_time:int]
				train_fastest_and_time_not_move = self._get_fastest_train_with_valid_capacity(route_data_list_not_move,group_with_prio)

				#self._get_fastest_train_with_capacity(route_data_list,group_with_prio) -> [train_fastest:class Train,earliest_end_time:int]
				train_fastest_and_time_move = self._get_fastest_train_with_valid_capacity(route_data_list_move,group_with_prio)    

				if train_fastest_and_time_not_move[0] != None and train_max_fastest_and_time_move[0] != None: #if train in and also not in move are available for calling             

					if train_fastest_and_time_not_move[1] < train_fastest_and_time_move[1]:
						self.travel_center.call_train_not_in_move(train_fastest_and_time_not_move[0],start_station,end_station)
					else:
						self.travel_center.call_train_in_move(train_fastest_and_time_move[0],start_station,end_station)

				elif train_fastest_and_time_not_move[0] != None: #if only trains not in move are available for calling			

					self.travel_center.call_train_not_in_move(train_fastest_and_time_not_move[0],start_station,end_station,group_with_prio)

				elif train_fastest_and_time_move[0] != None: #if only trains in move are available for calling

					self.travel_center.call_train_in_move(train_fastest_and_time_move[0],start_station,end_station,group_with_prio)
                                
				else: #no train available (because no train has enough capacity for the current group of passengers)

					#split the current group of passengers (Groups will usually sort the list of passenger groups again) and continue
					self.groups_manager.split_group(group_with_prio)
					continue
                                
      
			#if the ending station (where the passengers arrived) is full, check the capacities of the neighbor or other stations, where this train can move away, to not             block other trains, which want to pass this station
			self.travel_center.optimize_full_station(train_fastest_and_time_not_move[0],end_station)         

			#remove passenger group from Groups
			self.groups_manager.passengers_arrive(group_with_prio)

		#In class Result, generate the whole plan and output it
      
algo = Algo()
algo.run()

print(algo._get_fastest_train_with_valid_capacity([[Train(1,Station(2,20),4,10),10,20],[Train(2,Station(2,20),4,10),10,20]],[Passenger(1,Station(2,20),Station(4,20),20,10)]))

