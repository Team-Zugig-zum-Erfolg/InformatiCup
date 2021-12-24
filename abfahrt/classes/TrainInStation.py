class TrainInStation:
    def __init__(self, passenger_out_train_time, passenger_in_train_time, train, leave_time, station_id):
        self.passenger_out_train_time = passenger_out_train_time
        self.passenger_in_train_time = passenger_in_train_time
        self.train = train
        self.leave_time = leave_time
        self.station_id = station_id

    def __repr__(self):
        output = ",".join([str(self.passenger_out_train_time),str(self.passenger_in_train_time),str(self.train.get_id_str()),str(self.leave_time)])
        return output
    
    def __eq__(self, other):
        if (isinstance(other, TrainInStation)):
            return self.train == other.train and self.passenger_out_train_time == other.passenger_out_train_time and self.passenger_in_train_time == other.passenger_in_train_time and self.leave_time == other.leave_time and self.station_id == other.station_id
        return False
