from enum import Enum, auto


class ExplorationStatus(Enum):
    UNKNOWN = auto()
    UNDISCOVERED = auto()
    DISCOVERED = auto()
    CURRENT = auto()
