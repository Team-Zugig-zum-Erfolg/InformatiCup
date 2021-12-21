from classes.TrainInLine import TrainInLine
from classes.TrainInStation import TrainInStation

class Travel:
    def __init__(self, start_time, on_board, line_time, station_time: TrainInStation, start_station,
                 end_station, train, station_times, length):
        self.start_time = start_time
        self.on_board = on_board
        self.line_time = line_time
        self.station_time = station_time
        self.start_station = start_station
        self.end_station = end_station
        self.train = train
        self.station_times = station_times
        self.length = length

    def __repr__(self):

        output = ",".join([str(self.start_time),str(self.on_board),str(self.start_station.get_id_str()),str(self.end_station.get_id_str()),str(self.train.get_id_str())])
        return output
