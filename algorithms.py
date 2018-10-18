"""CSC148 Assignment 1 - Algorithms

=== CSC148 Fall 2018 ===
Department of Computer Science,
University of Toronto

=== Module Description ===

This file contains two sets of algorithms: ones for generating new arrivals to
the simulation, and ones for making decisions about how elevators should move.

As with other files, you may not change any of the public behaviour (attributes,
methods) given in the starter code, but you can definitely add new attributes
and methods to complete your work here.

See the 'Arrival generation algorithms' and 'Elevator moving algorithm'
sections of the assignment handout for a complete description of each algorithm
you are expected to implement in this file.
"""
import csv
from enum import Enum
import random
from typing import Dict, List, Optional

from entities import Person, Elevator
###############################################################################
# Arrival generation algorithms
###############################################################################
class ArrivalGenerator:
    """An algorithm for specifying arrivals at each round of the simulation.

    === Attributes ===
    max_floor: The maximum floor number for the building.
               Generated people should not have a starting or target floor
               beyond this floor.
    num_people: The number of people to generate, or None if this is left
                up to the algorithm itself.

    === Representation Invariants ===
    max_floor >= 2
    num_people is None or num_people >= 0
    """
    max_floor: int
    num_people: Optional[int]

    def __init__(self, max_floor: int, num_people: Optional[int]) -> None:
        """Initialize a new ArrivalGenerator.

        Preconditions:
            max_floor >= 2
            num_people is None or num_people >= 0
        """
        self.max_floor = max_floor
        self.num_people = num_people

    def generate(self, round_num: int) -> Dict[int, List[Person]]:
        """Return the new arrivals for the simulation at the given round.

        The returned dictionary maps floor number to the people who
        arrived starting at that floor.

        You can choose whether to include floors where no people arrived.
        """
        raise NotImplementedError


class RandomArrivals(ArrivalGenerator):
    """Generate a fixed number of random people each round.

    Generate 0 people if self.num_people is None.

    For our testing purposes, this class *must* have the same initializer header
    as ArrivalGenerator. So if you choose to to override the initializer, make
    sure to keep the header the same!

    Hint: look up the 'sample' function from random.
    """
    num_people: Optional[int]
    max_floor: int

    def __init__(self, max_floor: int, num_people: Optional[int]) -> None:
        """Initialize a new ArrivalGenerator.

        Preconditions:
            max_floor >= 2
            num_people is None or num_people >= 0
        """
        ArrivalGenerator.__init__(self, max_floor, num_people)

    def generate(self, round_num: int) -> Dict[int, List[Person]]:
        """
        Returns a Dictionary that maps the arriving people to the floor which
            they arrive at during a certain round (:

        round_num: The round which the arrivals are to take place
        """
        if self.num_people is None:
            arrival_amount = random.randint(0, 10)
        else:
            arrival_amount = self.num_people

        mapper = {}
        persons = []
        q = self.max_floor
        for i in range(q):
            mapper[i + 1] = []

        for i in range(arrival_amount + 1):
            r_start = random.randint(1, q)
            r_end = random.randint(1, q)
            if r_start == r_end:
                while r_start == r_end:
                    r_end = random.randint(0, q)
            else:
                for k in mapper:
                    if k == r_start:
                        mapper[k].append(Person(r_start, r_end))
                persons.append(Person(r_start, r_end))
        for g in range(q):
            for z in range(len(persons)):
                if persons[z] == z:
                    mapper[z].append(persons[z])
        return mapper


class FileArrivals(ArrivalGenerator):
    """Generate arrivals from a CSV file.

        arrival_floor: the floor that a Person will be arriving on, dictated by
            the given csv file.
    """

    arrival_round: int
    csv_line: int

    def __init__(self, max_floor: int, filename: str) -> None:
        """Initialize a new FileArrivals algorithm from the given file.

        The num_people attribute of every FileArrivals instance is set to None,
        since the number of arrivals depends on the given file.

        Precondition:
            <filename> refers to a valid CSV file, following the specified
            format and restrictions from the assignment handout.
        """

        self.csv_line = []
        ArrivalGenerator.__init__(self, max_floor, None)

        # We've provided some of the "reading from csv files" boilerplate code
        # for you to help you get started.
        with open(filename) as csvfile:
            reader = csv.reader(csvfile)
            for line in reader:
                # TODO: complete this. <line> is a list of strings corresponding
                # to one line of the original file.
                # You'll need to convert the strings to ints and then process
                # and store them.
                for i in range(len(line)):
                    line[i] = int(line[i])
                self.csv_line.append(line)

    def generate(self, round_num: int) -> Dict[int, List[Person]]:
        mapper = {}
        # maps floor number to person
        # TODO fix the implementation of generate for the csv file /
        # TODO try not to kill yourself when doing this.

        q = self.max_floor
        b = self.csv_line
        for i in range(q):
            mapper[i + 1] = []

        for round_inst in b:
            for c in range(2, len(round_inst), 2):
                if round_inst[0] == round_num:
                    mapper[round_inst[c - 1]].append(Person(round_inst[c - 1],
                                                            round_inst[c]))
        return mapper


###############################################################################
# Elevator moving algorithms
###############################################################################
class Direction(Enum):
    """
    The following defines the possible directions an elevator can move.
    This is output by the simulation's algorithms.

    The possible values you'll use in your Python code are:
        Direction.UP, Direction.DOWN, Direction.STAY
    """
    UP = 1
    STAY = 0
    DOWN = -1


class MovingAlgorithm:
    """An algorithm to make decisions for moving an elevator at each round.
    """

    def move_elevators(self,
                       elevators: List[Elevator],
                       waiting: Dict[int, List[Person]],
                       max_floor: int) -> List[Direction]:
        """Return a list of directions for each elevator to move to.

        As input, this method receives the list of elevators in the simulation,
        a dictionary mapping floor number to a list of people waiting on
        that floor, and the maximum floor number in the simulation.

        Note that each returned direction should be valid:
            - An elevator at Floor 1 cannot move down.
            - An elevator at the top floor cannot move up.
        """
        raise NotImplementedError


class RandomAlgorithm(MovingAlgorithm):
    """A moving algorithm that picks a random direction for each elevator.
    """

    def move_elevators(self,
                       elevators: List[Elevator],
                       waiting: Dict[int, List[Person]],
                       max_floor: int) -> List[Direction]:
        d_list = []
        e = elevators
        m = max_floor

        for _ in range(len(e)):
            d_list.append(None)

        for x in range(len(e)):
            r = random.randint(1, 9)
            if 1 <= r <= 3:
                if e[x].current_floor != m:
                    d_list[x] = Direction.UP
                    e[x].current_floor += 1
                else:
                    r = random.randint(1, 2)
                    if r == 1:
                        d_list[x] = Direction.DOWN
                        e[x].current_floor -= 1
                    else:
                        d_list[x] = Direction.STAY

            elif 4 <= r <= 6:
                d_list[x] = Direction.STAY

            elif 7 <= r <= 9:
                if e[x].current_floor != 1:
                    d_list[x] = Direction.DOWN
                    e[x].current_floor -= 1
                else:
                    r = random.randint(1, 2)
                    if r == 1:
                        d_list[x] = Direction.UP
                        e[x].current_floor += 1
                    else:
                        d_list[x] = Direction.STAY

        return d_list


class PushyPassenger(MovingAlgorithm):
    """A moving algorithm that preferences the first passenger on each elevator.

    If the elevator is empty, it moves towards the *lowest* floor that has at
    least one person waiting, or stays still if there are no people waiting.

    If the elevator isn't empty, it moves towards the target floor of the
    *first* passenger who boarded the elevator.
    """

    def move_elevators(self,
                       elevators: List[Elevator],
                       waiting: Dict[int, List[Person]],
                       max_floor: int) -> List[Direction]:
        # First, check waiting to see the lowest floor with people waiting
        d_list = []
        q = 0
        for el in range(len(elevators)):
            d_list.append(None)

        # the first part, works.
        for le in range(len(elevators)):
            if len(elevators[le].passengers) > 0:
                if elevators[le].passengers[0].target \
                        < elevators[le].current_floor:

                    elevators[le].current_floor -= 1
                    d_list[le] = Direction.DOWN
                elif elevators[le].passengers[0].target \
                        > elevators[le].current_floor:

                    d_list[le] = Direction.UP
                    elevators[le].current_floor += 1

            elif len(elevators[le].passengers) == 0:
                for k, v in waiting.items():
                    if len(v) != 0:
                        q = k
                        continue
                if q > elevators[le].current_floor:
                    elevators[le].current_floor += 1
                    d_list[le] = Direction.UP

                elif q < elevators[le].current_floor:
                    elevators[le].current_floor -= 1
                    d_list[le] = Direction.DOWN

        return d_list


class ShortSighted(MovingAlgorithm):
    """A moving algorithm that preferences the closest possible choice.

    If the elevator is empty, it moves towards the *closest* floor that has at
    least one person waiting, or stays still if there are no people waiting.

    If the elevator isn't empty, it moves towards the closest target floor of
    all passengers who are on the elevator.

    In this case, the order in which people boarded does *not* matter.
    """

    def move_elevators(self,
                       elevators: List[Elevator],
                       waiting: Dict[int, List[Person]],
                       max_floor: int) -> List[Direction]:
        d_list = []
        for el in range(len(elevators)):
            d_list.append(None)

        for num in range(len(elevators)):
            if len(elevators[num].passengers) == 0:
                for k, v in waiting.items():
                    if (elevators[num].current_floor - k) > 1 and len(v) != 0:
                        d_list[num] = Direction.DOWN
                        elevators[num].current_floor -= 1
                    elif (elevators[num].current_floor + k) < max_floor and len(
                            v) != 0:
                        d_list[num] = Direction.UP
                        elevators[num].current_floor += 1
            elif len(elevators[num].passengers) != 0:
                for i in range(len(elevators[num].passengers)):
                    w = []
                    for x in range(elevators[num].passengers):
                        w.append(elevators[num].passengers[x].target)
                        continue

                    pass

            # for n in range(max_floor):
            #     q = elevators[n].current_floor - n
            #     b = elevators[n].current_floor + n
            #     if q >= 1:
            #         if len(waiting[elevators[num].current_floor - n]) != 0:
            #             d_list[num] = Direction.DOWN
            #             elevators[num].current_floor -= 1
            #     elif b <= max_floor:
            #         if len(waiting[elevators[num].current_floor + n]) != 0:
            #             d_list[num] = Direction.UP
            #             elevators[num].current_floor += 1
            else:
                pass
        return d_list


if __name__ == '__main__':
    # Don't forget to check your work regularly with python_ta!
    import python_ta

    python_ta.check_all(config={
        'allowed-io': ['__init__'],
        'extra-imports': ['entities', 'random', 'csv', 'enum'],
        'max-nested-blocks': 4,
        'disable': ['R0201'],
        'max-attributes': 12
    })
