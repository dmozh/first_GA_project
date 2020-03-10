from enum import Enum


class SelectionsTypes(Enum):
    RANK = 1
    TOURNAMENT = 2
    TRUNCATIONS = 3


class ModeWork(Enum):
    CYCLICAL = 1
    STEPS = 2


class Recombination(Enum):
    ONE_POINTER = 1
    TWO_POINTER = 2
    UNIFORM = 3