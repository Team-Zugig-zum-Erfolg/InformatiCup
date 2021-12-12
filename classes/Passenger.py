from typing import List
from classes.Station import Station


class Passenger:
    # Passagiere: str(ID) str(Startbahnhof) str(Zielbahnhof) int(Gruppengröße) int(Ankunftszeit)

    id: int = 0
    start_station: Station = None
    end_station: Station = None
    group_size: int = 0
    target_time: int = 0

    action_board_time: int = 0
    action_arrive_time: int = 0
    action_train: str = ""

    history: List[str] = []

    def __init__(self, id: int, start_station: Station, end_station: Station, group_size: int, target_time: int):
        self.id = id
        self.start_station = start_station
        self.end_station = end_station
        self.group_size = group_size
        self.target_time = target_time
        self.history = []

    def to_list(self):
        return [self.id, self.start_station.id, self.end_station.id, self.group_size, self.target_time]

    def to_str_input(self) -> str:
        output = " ".join([self.get_id_str(), self.start_station.get_id_str(
        ), self.end_station.get_id_str(), str(self.group_size), str(self.target_time)])
        return output

    def to_str_output(self) -> str:
        # return "[Passenger:P" + str(self.ID) + "]\n" + str(self.board_time) + " Board " + self.train + "\n" + str(self.arrive_time)+ " Detrain\n"
        output = "\n".join(self.history)
        return output

    def add_board(self, time: int, train_id: int):
        out = str(time) + " " + "Board" + " T" + str(train_id)
        # print(f"passenger [{self.id}] add board",out)
        self.history.append(out)

    def add_detrain(self, time: int):
        out = str(time) + " " + "Detrain"
        # print(f"passenger [{self.id}] add detrain",out)
        self.history.append(out)

    def merge(self, passenger):
        self.history += passenger.history

    def get_id_str(self) -> str:
        ''' get id with P in a string '''
        out = "P" + str(self.id)
        return out

    def get_id(self):
        return self.id

    def set_id(self, id_passenger: int):
        self.id = id_passenger
        return True

    def get_start_station(self):
        return self.start_station

    def set_start_station(self, start_station):
        if type(start_station) != str:
            return False
        self.start_station = start_station
        return True

    def get_end_station(self):
        return self.end_station

    def set_end_station(self, end):
        if type(end) != list or len(end) != 2:
            return False
        self.end_station = end
        return True

    def get_group_size(self):
        return self.group_size

    def set_group_size(self, size):
        if type(size) != int:
            return False
        self.group_size = size
        return True

    def set_target_round(self, target_round):
        if type(target_round) != int:
            return False
        self.target_time = target_round
        return True

    def get_target_round(self):
        return self.target_time

    def __repr__(self):
        output = " ".join([self.get_id_str(), self.get_start_station().get_id_str(
        ), self.get_end_station().get_id_str(), str(self.get_group_size()), str(self.get_target_round())])
        return output
