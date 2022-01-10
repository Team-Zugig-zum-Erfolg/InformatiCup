class Station:

    id: int = 0
    capacity: int = 0

    def __init__(self, id: int, capacity: int):
        """
        Creating a station

        Args:
            id (int): id
            capacity (int): capacity
        """
        self.id = id
        self.capacity = capacity

    def to_list(self) -> list:
        """
        Convert to list

        Returns:
          list: list of parameters
        """
        return [self.id, self.capacity]

    def to_str_input(self) -> str:
        """
        This method is used for input, generate information of one passenger

        Returns:
            output: string of information
        """
        output = " ".join([self.get_id_str(), str(self.capacity)])
        return output

    def get_id_str(self) -> str:
        """
        Get the str(id) with S

        Returns:
            str: string of information
        """
        out = "S" + str(self.id)
        return out

    def get_id(self):
        """
        Get the id of the station

        Returns:
            int: id of the station
        """
        return self.id

    def set_id(self, id: int):
        """
        Set the id of the station

        Args:
            id (int): id to set

        Returns:
            bool: True, if sucessful set, else False
        """
        if type(id) != int:
            return False
        self.id = id
        return True

    def get_capacity(self):
        """
        Get capacity of the station

        Returns:
            int: capacity of the station
        """
        return self.capacity

    def set_capacity(self, capacity: int):
        """
        Set the capacity of the station

        Args:
            capacity (int): capacity to set

        Returns:
            bool: True, if successful, else False
        """
        if type(capacity) != int:
            return False
        self.capacity = capacity
        return True

    def __repr__(self):
        """
        Representing the station as string

        Returns:
            str: station as string
        """
        output = " ".join([self.get_id_str(), str(self.get_capacity())])
        return output

    def __eq__(self, other):
        """
        Compare the station with an other station

        Args:
            other (Station): other station to compare

        Returns:
            bool: True, if equal, else False
        """
        if (isinstance(other, Station)):
            return self.id == other.id and self.capacity == other.capacity
        return False
