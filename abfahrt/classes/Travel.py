from typing import List
from typing import Tuple

from abfahrt.classes.Station import Station
from abfahrt.classes.TrainInLine import TrainInLine
from abfahrt.classes.TrainInStation import TrainInStation
from abfahrt.classes.Train import Train


class Travel:
    def __init__(self, start_time: int, on_board: int, line_time: List[TrainInLine], station_time: TrainInStation, start_station: Station,
                 end_station: Station, train: Train, station_times: List[TrainInStation], length: int):
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
        output = ",".join([str(self.start_time), str(self.on_board), str(
            self.start_station.get_id_str()), str(self.end_station.get_id_str()), str(self.train.get_id_str())])
        return output
