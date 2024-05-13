from enum import Enum

class PlayerTypes(Enum):
    ISAAC = 'isaac'
    LAZARUS = 'lazarus'
    EVE = 'eve'

    def get_index(self):
        vocabulary = {PlayerTypes.ISAAC: 0, 
                      PlayerTypes.LAZARUS: 1, 
                      PlayerTypes.EVE: 2}
        return vocabulary[self]
    
    def get_all_characters():
        return [PlayerTypes.ISAAC, PlayerTypes.EVE, PlayerTypes.LAZARUS]
    
    def get_all_characters_values():
        return [PlayerTypes.ISAAC.value, PlayerTypes.EVE.value, PlayerTypes.LAZARUS.value]