from abfahrt.classes.Station import Station


class Line:

    id: int = 0
    start: Station = None
    end: Station = None
    capacity: int = 0
    length: float = 0.0

    def __init__(self, id: int, start: Station, end: Station, length: float, capacity: int):
        """
        Creating a Line

        Args:
           id (int): id
           start (Station): first station to connect
           end (Station): second station to connect
           length (float): length
           capacity (int): capacity
        """
        self.id = id
        self.start = start
        self.end = end
        self.capacity = capacity
        self.length = length

    def to_list(self) -> list:
        """
        Convert to list

        Returns:
            list: a list of values
        """
        return [self.id, self.start.id, self.end.id, self.length, self.capacity]

    def to_str_input(self):
        """
        This method is used for input, generate information of one line

        Returns:
            str: string of information
        """
        output = " ".join([self.get_id_str(), self.start.get_id_str(
        ), self.end.get_id_str(), str(self.length), str(self.capacity)])
        return output

    def get_id_str(self) -> str:
        """
        Get the str(id)

        Returns:
            str: string of id
        """
        out = "L" + str(self.id)
        return out

    def get_id(self):
        """
        Get the int(id)

        Returns:
            int: int of id
        """
        return self.id

    def set_id(self, id_line: str):
        """
        Set id of line

        Args:
            id_line (str): string of id 

        Returns:
            bool: id_line is not from type string?, true = Type string, false = Type int
        """
        if type(id_line) != str:
            return False
        self.id = id_line
        return True

    def get_capacity(self):
        """
        Get capazity of line

        Returns:
            int: int of capacity
        """
        return self.capacity

    def set_capacity(self, capacity: int):
        """
        Set capacity of line

        Args:
            capacity (int): int capacity 

        Returns:
            bool: capacity is not from type int?, true = Type int, false = Type is false
        """
        if type(capacity) != int:
            return False
        self.capacity = capacity
        return True

    def get_start(self):
        """
        Get start station of line

        Returns:
            start (Station): first station to connect
        """
        return self.start

    def set_start(self, start: Station):
        """
        Set start station

        Args:
            start (Station): first station to connect

        Returns:
            bool: start is instance of Station?, true = Type is correct, false = Type is false
        """
        if (isinstance(start, Station) == False):
            return False
        self.start = start
        return True

    def get_end(self):
        """
        Get end station of line

        Returns:
            end (Station): end station to connect
        """
        return self.end

    def set_end(self, end: Station):
        """
        Set end station

        Args:
            end (Station): end station to connect

        Returns:
            bool: end is instance of Station?, true = Type is correct, false = Type is false
        """
        if (isinstance(end, Station) == False):
            return False
        self.end = end
        return True

    def get_length(self):
        """
        Get length of line

        Returns:
            float: float of length
        """
        return self.length

    def set_length(self, length: float):
        """
        Set length of line

        Args:
            length (float): float of length 

        Returns:
            bool: length is not from type float?, true = Type float, false = Type is false
        """
        if type(length) != float:
            return False
        self.length = length
        return True

    def __repr__(self):
        """
        Representation of object Line ( can be used for print)

        Returns:
            string: string from object
        """
        out = self.to_str_input()
        return out

    def __eq__(self, other):
        """
        Check if both lines are equal

        Args:
            other (Line): pther line

        Returns:
            bool: other is equal to Line?, true = Type is correct, false = Type is false
        """
        if (isinstance(other, Line)):
            return self.id == other.id and self.capacity == other.capacity and self.length == other.length and self.start == other.start and self.end == other.end
        return False
