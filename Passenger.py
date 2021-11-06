from Station import Station

class Passenger:
    ID: int = 0
    start: Station = None
    end: Station = None
    size: int = 0
    arrive_time: int = 0


    def __init__(self) -> None:
        pass
    
    def to_str(self) -> str:
        pass