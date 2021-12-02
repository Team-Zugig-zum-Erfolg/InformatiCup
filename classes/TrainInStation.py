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
