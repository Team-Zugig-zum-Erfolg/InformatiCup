"""
    This is Linelist for managing the lines
"""
from typing import List
# This module provides runtime support for type hints. The most fundamental support consists of the types Any, Union, Callable, TypeVar, and Generic. For a full specification, please see PEP 484. For a simplified introduction to type hints, see PEP 483. (https://docs.python.org/3/library/typing.html)
from typing import Tuple
# These can be used as types in annotations using [], each having a unique syntax. (https://docs.python.org/3/library/typing.html)

from abfahrt.classes.Train import Train
from abfahrt.classes.Line import Line
from abfahrt.classes.TrainInLine import TrainInLine


class Linelist:

    def __init__(self, lines: List[Line]):
        """
        Initializing Linelist
        """
        self.lines = []  # the lines with capacities
        linelist = []
        for line in lines:
            linelist.append(line.to_list())
        line_number = 1
        self.lines.append([])
        for line in linelist:
            self.lines.append([])
            for i in range(0, line[4]):
                self.lines[line_number].append([])
            line_number = line_number + 1

    def compare_free(self, train_in_line: TrainInLine) -> bool:
        """
        Checks if the given TrainInLine object can inserted into the line

        Args:
            train_in_line (TrainInLine): the TrainInLine object

        Returns:
            bool: True, if the TrainInLine object can be inserted, else False
        """
        earliest_leave_time = -1
        line_capacities = self.lines[train_in_line.line_id]

        for capacity in line_capacities:
            if len(capacity) == 0:
                return [True, -1]

        ends = []
        for capacity in line_capacities:
            if train_in_line.end <= capacity[0].start:
                return [True, -1]
            for train_pos in range(len(capacity) - 1):
                if capacity[train_pos].end <= train_in_line.start and train_in_line.end <= capacity[train_pos+1].start:
                    return [True, -1]
                elif Linelist._train_in_line_between(capacity[train_pos], capacity[train_pos + 1], train_in_line.start, train_in_line.end) == True:
                    if capacity[train_pos].end > train_in_line.start:
                        ends.append(capacity[train_pos].end)

            if capacity[-1].end > train_in_line.start:
                ends.append(capacity[-1].end)
            else:
                return [True, -1]

        cpa_end = ends[0]
        for end in ends:
            if cpa_end > end:
                cpa_end = end
        earliest_leave_time = cpa_end
        return [False, earliest_leave_time]

    @staticmethod
    def _train_in_line_between(front_train_in_line: TrainInLine, back_train_in_line: TrainInLine, start: int, end: int) -> bool:
        """
        Checks if a given time range is free/can be inserted between two TrainInLine objects

        Args:
            front_train_in_line (TrainInLine): first TrainInLine object
            back_train_in_line (TrainInLine): second TrainInLine object
            start (int): start of time range
            end (int): end of time range

        Returns:
            bool: True, if the time range is free/possible, else False
        """
        dis = back_train_in_line.start - front_train_in_line.end
        dis_needed = end - start
        return dis_needed <= dis

    def add_new_train_in_line(self, train_in_line: TrainInLine) -> bool:
        """
        Inserts a TrainInLine object into the right/best fitting capacity of the line

        Args:
            train_in_line (TrainInLine): the TrainInLine object

        Returns:
            bool: True, if inserting was successful, else False
        """
        capacity_number = 0
        for capacity in self.lines[train_in_line.line_id]:
            if len(capacity) == 0:
                self.lines[train_in_line.line_id][capacity_number].append(
                    train_in_line)
                self.lines[train_in_line.line_id][capacity_number].sort(
                    key=lambda x: x.start)
                return True
            if train_in_line.end <= capacity[0].start:
                self.lines[train_in_line.line_id][capacity_number].append(
                    train_in_line)
                self.lines[train_in_line.line_id][capacity_number].sort(
                    key=lambda x: x.start)
                return True
            for train_pos in range(len(capacity) - 1):
                if capacity[train_pos].end <= train_in_line.start and train_in_line.end <= capacity[train_pos+1].start:
                    self.lines[train_in_line.line_id][capacity_number].append(
                        train_in_line)
                    self.lines[train_in_line.line_id][capacity_number].sort(
                        key=lambda x: x.start)
                    return True
            if capacity[-1].end <= train_in_line.start:
                self.lines[train_in_line.line_id][capacity_number].append(
                    train_in_line)
                self.lines[train_in_line.line_id][capacity_number].sort(
                    key=lambda x: x.start)
                return True
            capacity_number += 1

        return False

    def read_trains_from_line(self, line_number: int) -> List[Train]:
        """
        Restrieves the trains from a line

        Args:
            line_number (int): id of the line

        Returns:
            List[Train]: trains in the line
        """
        trains = []
        for capacity in self.lines[line_number]:
            for train_in_line in capacity:
                if train_in_line.train not in trains:
                    trains.append(train_in_line.train)
        return trains
