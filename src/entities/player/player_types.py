from enum import Enum

class PlayerTypes(Enum):
    ISAAC = 'player'
    RED_HEAD = 'lazarus'
    WOMAN = 'eve'

    def get_index(self):
        vocabulary = {PlayerTypes.ISAAC: 0, 
                      PlayerTypes.RED_HEAD: 1, 
                      PlayerTypes.WOMAN: 2}
        return vocabulary[self]