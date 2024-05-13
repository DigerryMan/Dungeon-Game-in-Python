from config import MAP_RANGE
from map.exploration_status import ExplorationStatus

class Minimap():
    def __init__(self, map):
        self.map = map
        self.minimap = [[ExplorationStatus.UNKNOWN for _ in range(MAP_RANGE)] for _ in range(MAP_RANGE)]
        self.load_images()
        self.load_positions()


    def load_images(self):
        self.background = self.map.game.image_loader.minimap["background"].copy()

        self.room_images = {
            ExplorationStatus.UNDISCOVERED: self.map.game.image_loader.minimap["undiscovered_room"].copy(),
            ExplorationStatus.DISCOVERED: self.map.game.image_loader.minimap["discovered_room"].copy(),
            ExplorationStatus.CURRENT: self.map.game.image_loader.minimap["current_room"].copy()
        }
        self.shop_icon = self.map.game.image_loader.minimap["shop_icon"].copy()
        self.boss_icon = self.map.game.image_loader.minimap["boss_icon"].copy()

    def load_positions(self):
        screen_width = self.map.game.settings.WIN_WIDTH
        self.positions = {}
        self.positions["background"] = (screen_width - self.background.get_width(), 0)
    
        room_icon_width = self.room_images[ExplorationStatus.UNDISCOVERED].get_width()
        room_icon_height = self.room_images[ExplorationStatus.UNDISCOVERED].get_height()

        start_x = self.positions["background"][0] + (self.background.get_width() - 5 * room_icon_width) // 2
        start_y = self.positions["background"][1] + (self.background.get_height() - 5 * room_icon_height) // 2

        self.positions["rooms"] = [[(start_x + j * room_icon_width, start_y + i * room_icon_height) for j in range(5)] for i in range(5)]

    def update_minimap(self):
        row, col = self.map.current_position
        self.minimap[row][col] = ExplorationStatus.CURRENT

        d_row = [-1, 1, 0, 0]
        d_col = [0, 0, -1, 1]

        for i in range(4):
            new_row = row + d_row[i]
            new_col = col + d_col[i]

            if new_row >= 0 and new_row < MAP_RANGE and new_col >= 0 and new_col < MAP_RANGE:
                if self.minimap[new_row][new_col] == ExplorationStatus.UNKNOWN:
                    self.minimap[new_row][new_col] = ExplorationStatus.UNDISCOVERED

                elif self.minimap[new_row][new_col] == ExplorationStatus.CURRENT:
                    self.minimap[new_row][new_col] = ExplorationStatus.DISCOVERED

    def draw(self, screen):
        screen.blit(self.background, self.positions["background"])

        left_row, left_col, right_row, right_col = self.get_bounds_to_draw()

        for i in range(left_row, right_row):
            for j in range(left_col, right_col):
                room = self.map.room_map[i][j]
                if room is not None:
                    if self.minimap[i][j] == ExplorationStatus.UNDISCOVERED:
                        screen.blit(self.room_images[ExplorationStatus.UNDISCOVERED], self.positions["rooms"][i - left_row][j - left_col])
                    elif self.minimap[i][j] == ExplorationStatus.DISCOVERED:
                        screen.blit(self.room_images[ExplorationStatus.DISCOVERED], self.positions["rooms"][i - left_row][j - left_col])
                    elif self.minimap[i][j] == ExplorationStatus.CURRENT:
                        screen.blit(self.room_images[ExplorationStatus.CURRENT], self.positions["rooms"][i - left_row][j - left_col])

                    if room.room_type == "shop" and self.minimap[i][j] != ExplorationStatus.UNKNOWN:
                        screen.blit(self.shop_icon, self.positions["rooms"][i - left_row][j - left_col])
                    elif room.room_type == "boss" and self.minimap[i][j] != ExplorationStatus.UNKNOWN:
                        screen.blit(self.boss_icon, self.positions["rooms"][i - left_row][j - left_col])

    def get_bounds_to_draw(self):
        current_row, current_col = self.map.current_position

        left_row = max(0, current_row - 2)
        left_col = max(0, current_col - 2)
        right_row = min(MAP_RANGE, current_row + 3)
        right_col = min(MAP_RANGE, current_col + 3)

        if current_row - left_row < 2:
            right_row = min(MAP_RANGE, right_row + (2 - (current_row - left_row)))
        if current_col - left_col < 2:
            right_col = min(MAP_RANGE, right_col + (2 - (current_col - left_col)))
        if right_row - current_row < 3:
            left_row = max(0, left_row - (3 - (right_row - current_row)))
        if right_col - current_col < 3:
            left_col = max(0, left_col - (3 - (right_col - current_col)))

        return left_row, left_col, right_row, right_col