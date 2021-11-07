from Station import Station

class Passenger:
    ID: int = 0
    start: Station = None
    end: Station = None
    size: int = 0
    board_time: int = 0
    arrive_time: int = 0
    train: str = ""


    def __init__(self) -> None:
        pass
    
    def to_str(self) -> str:
        return "[Passenger:P" + str(self.ID) + "]\n" + str(self.board_time) + " Board " + self.train + "\n" + str(self.arrive_time)+ " Detrain\n"
