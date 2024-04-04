class Settings():
    def __init__(self, window_size):
        self.WIN_WIDTH = window_size[0]
        self.WIN_HEIGHT = window_size[1]
        self.TILE_SIZE = self.WIN_WIDTH // 32
        self.MAP_WIDTH = self.WIN_WIDTH // self.TILE_SIZE
        self.MAP_HEIGHT = self.WIN_HEIGHT // self.TILE_SIZE
        self.DIFFICULTY = None