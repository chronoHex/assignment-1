"""CSC148 Assignment 1 - People and Elevators

=== CSC148 Fall 2018 ===
Department of Computer Science,
University of Toronto

=== Module description ===
This module contains classes for the two "basic" entities in this simulation:
people and elevators. We have provided basic outlines of these two classes
for you; you are responsible for implementing these two classes so that they
work with the rest of the simulation.

You may NOT change any existing attributes, or the interface for any public
methods we have provided. However, you can (and should) add new attributes,
and of course you'll have to implement the methods we've provided, as well
as add your own methods to complete this assignment.

Finally, note that Person and Elevator each inherit from a kind of sprite found
in sprites.py; this is to enable their instances to be visualized properly.
You may not change sprites.py, but are responsible for reading the documentation
to understand these classes, as well as the abstract methods your classes must
implement.
"""
from __future__ import annotations
from typing import List
from sprites import PersonSprite, ElevatorSprite


class Elevator(ElevatorSprite):
    """An elevator in the elevator simulation.

    Remember to add additional documentation to this class docstring
    as you add new attributes (and representation invariants).

    === Attributes ===
    passengers: A list of the people currently on this elevator
    capacity: An int describing the amount of people that can be on one elevator
    current_floor: An int describing the current floor that the elevator is
        currently on.
    === Representation invariants ===
    """
    passengers: List[Person]
    capacity: int
    current_floor: int

    def __init__(self, capacity) -> None:
        ElevatorSprite.__init__(self)
        self.capacity = capacity
        self.current_floor = 1
        self.passengers = []

    def fullness(self) -> float:
        # print(self.passengers)
        raw_amount = (len(self.passengers)) / self.capacity
        # print("passengers" , len(self.passengers))
        rounded = round(raw_amount, 1)
        print("rounded", rounded)
        # print("after rounded", len(self.passengers))
        return rounded


class Person(PersonSprite):
    """A person in the elevator simulation.

    === Attributes ===
    start: the floor this person started on
    target: the floor this person wants to go to
    wait_time: the number of rounds this person has been waiting
    current: the floor this person is currently on

    === Representation invariants ===
    start >= 1
    target >= 1
    wait_time >= 0
    current >= 1
    """
    start: int
    target: int
    wait_time: int
    current: int
    anger_level: int

    def __init__(self, start, target) -> None:
        self.wait_time = 0
        self.start = start
        self.target = target
        self.anger_level = 0
        PersonSprite.__init__(self, )

    def get_anger_level(self) -> int:
        """Return this person's anger level.

        A person's anger level is based on how long they have been waiting
        before reaching their target floor.
            - Level 0: waiting 0-2 rounds
            - Level 1: waiting 3-4 rounds
            - Level 2: waiting 5-6 rounds
            - Level 3: waiting 7-8 rounds
            - Level 4: waiting >= 9 rounds
        """
        self.anger_level = 0
        if 0 <= self.wait_time <= 2:
            self.anger_level = 0
        elif 3 <= self.wait_time <= 4:
            self.anger_level = 1
        elif 5 <= self.wait_time <= 6:
            self.anger_level = 2
        elif 7 <= self.wait_time <= 8:
            self.anger_level = 3
        elif self.wait_time >= 9:
            self.anger_level = 4

        return self.anger_level


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['sprites'],
        'max-nested-blocks': 4
    })
