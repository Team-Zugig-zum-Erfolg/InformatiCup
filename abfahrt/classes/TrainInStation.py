from abfahrt.classes.Train import Train
from abfahrt.classes.Station import Station


class TrainInStation:
    def __init__(self, arrive_train_time, passenger_in_train_time, train:Train, leave_time, station_id:Station):
        self.arrive_train_time = arrive_train_time
        self.passenger_in_train_time = passenger_in_train_time
        self.train = train
        self.leave_time = leave_time
        self.station_id = station_id

    def __repr__(self):
        output = ",".join([str(self.arrive_train_time), str(self.passenger_in_train_time), str(
            self.train.get_id_str()), str(self.leave_time), str(self.station_id)])
        return output

    def __eq__(self, other):
        if (isinstance(other, TrainInStation)):
            return self.train == other.train and self.arrive_train_time == other.arrive_train_time and self.passenger_in_train_time == other.passenger_in_train_time and self.leave_time == other.leave_time and self.station_id == other.station_id
        return False
