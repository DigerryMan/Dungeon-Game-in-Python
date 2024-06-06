from enum import Enum


class PlayerTypes(Enum):
    ISAAC = "isaac"
    LAZARUS = "lazarus"
    EVE = "eve"
    TAINTED = "tainted"

    def get_index(self):
        vocabulary = {PlayerTypes.ISAAC: 0, PlayerTypes.LAZARUS: 1, PlayerTypes.EVE: 2, PlayerTypes.TAINTED: 3}
        return vocabulary[self]

    def get_all_characters():
        return [PlayerTypes.ISAAC, PlayerTypes.LAZARUS, PlayerTypes.EVE, PlayerTypes.TAINTED]

    def get_all_characters_values(): 
        return [
            PlayerTypes.ISAAC.value,
            PlayerTypes.LAZARUS.value,
            PlayerTypes.EVE.value,
            PlayerTypes.TAINTED.value
        ]

    def get_player_stats(self):
        # values are (max_health, dmg, speed)
        player_stats = {
            PlayerTypes.ISAAC: (6, 1, 9),
            PlayerTypes.LAZARUS: (5, 0.8, 10),
            PlayerTypes.EVE: (5, 1.5, 8),
            PlayerTypes.TAINTED: (30, 3, 12),
        }

        return player_stats.get(self, (None, None, None))
