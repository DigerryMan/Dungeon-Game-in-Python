class Settings:
    def __init__(self, window_size):
        self.WIN_WIDTH = window_size[0]
        self.WIN_HEIGHT = window_size[1]

        self.SCALE = self.WIN_WIDTH / 1920

        self.TILE_SIZE = self.WIN_WIDTH // 16
        self.PLAYER_SIZE = int(self.TILE_SIZE * 0.8)
        self.MOB_SIZE = int(self.TILE_SIZE * 0.85)
        self.STAT_BARS_HEALTH_SIZE = self.TILE_SIZE * 0.33

        self.BULLET_SIZE = int(self.SCALE * 40)

        self.MAP_WIDTH = self.WIN_WIDTH // self.TILE_SIZE
        self.MAP_HEIGHT = self.WIN_HEIGHT // self.TILE_SIZE
        self.DIFFICULTY = None
