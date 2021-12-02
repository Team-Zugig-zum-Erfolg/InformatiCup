class TrainInLine:
    def __init__(self, train, start, end, line_id):
        self.train = train
        self.start = start
        self.end = end
        self.line_id = line_id

    def __repr__(self):
        output = ",".join([str(self.train), str(self.start), str(self.end), str(self.line_id)])
        return output
        
