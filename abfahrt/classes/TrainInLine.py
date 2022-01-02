from abfahrt.classes.Train import Train
from abfahrt.classes.Line import Line


class TrainInLine:
    def __init__(self, train: Train, start: int, end: int, line_id: int):
        self.train = train
        self.start = start
        self.end = end
        self.line_id = line_id

    def __repr__(self):
        output = ",".join(
            ["T"+str(self.train), str(self.start), str(self.end), str(self.line_id)])
        return output

    def __eq__(self, other):
        if (isinstance(other, TrainInLine)):
            return self.train == other.train and self.start == other.start and self.end == other.end and self.line_id == other.line_id
        return False
