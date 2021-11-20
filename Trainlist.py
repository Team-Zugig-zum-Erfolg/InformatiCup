
class Trainlist:


    trains = []
    
    
    def initial(self, trainlist):
      
        train_number = 1
        self.trains.append([])
        for train in trainlist:
            self.trains.append([]) 
            self.trains[train_number].append(int(train[3])) #Add capacity
            train_number = train_number + 1
        return True    
   
    def add_new_passengers_in_train(self, passengers, start, end, train_number):

        for pa_in_train in self.trains[train_number]:
            if type(pa_in_train) == int:
                continue
            if pa_in_train[1] == start and pa_in_train[2] == end:
                self.trains[train_number][0].extend(passengers)
                return True

        self.trains[train_number].append([passengers,start,end]);
        return True

    def _calculate_capacity_passengers(self, passengers):
        capacity = 0
        for pa in passengers:
            capacity = capacity + pa.get_group_size()	
        return capacity

    def check_capacity(self, new_passengers, start, end, train_number):

        capacity = -1
        used_capacity = -1

        for pa_in_train in self.trains[train_number]:
            if type(pa_in_train) == int:
                capacity = pa_in_train

        for pa_in_train in self.trains[train_number]:
            if type(pa_in_train) == int:
                continue
            if pa_in_train[1] == start and pa_in_train[2] == end:
                if (capacity-self._calculate_capacity_passengers(pa_in_train[0]))>=self._calculate_capacity_passengers(new_passengers):
                    return True
                else:
                    return False
