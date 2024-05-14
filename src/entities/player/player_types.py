from enum import Enum

class PlayerTypes(Enum):
    ISAAC = 'isaac'
    LAZARUS = 'lazarus'
    EVE = 'eve'

    def get_index(self):
        #order of integers has to be the same as in get_all_characters() for death animation to work properly
        vocabulary = {PlayerTypes.ISAAC: 0, 
                      PlayerTypes.LAZARUS: 1, 
                      PlayerTypes.EVE: 2} 
        return vocabulary[self]
    
    def get_all_characters():
        return [PlayerTypes.ISAAC, PlayerTypes.LAZARUS, PlayerTypes.EVE]
    
    def get_all_characters_values(): #
        return [PlayerTypes.ISAAC.value, PlayerTypes.LAZARUS.value, PlayerTypes.EVE.value]
    
    def get_player_stats(self):
        #values are (max_health, dmg, speed)
        player_stats ={
            PlayerTypes.ISAAC: (4, 1, 8),

            #PlayerTypes.LAZARUS: (3, 0.8, 10),
            # FOR TESTING 
            PlayerTypes.LAZARUS: (20, 100, 12),
            PlayerTypes.EVE: (3, 1.5, 7)
        }
        
        return player_stats.get(self, (None, None, None)) 