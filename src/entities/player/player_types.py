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
    
    def get_player_stats(self):
        #values are (max_health, dmg, speed)
        player_stats ={
            PlayerTypes.ISAAC: (4, 1, 8),
            PlayerTypes.LAZARUS: (3, 0.8, 10),
            PlayerTypes.EVE: (2, 1.5, 7)
        }
        
        return player_stats.get(self, (None, None, None)) 