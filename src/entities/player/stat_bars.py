import math
import pygame
from config import BLACK, FPS, ROOM_NUMBER

class StatBars():
    def __init__(self, game, player):
        self.game = game
        self.player = player
        
        self.TILE_SIZE = game.settings.TILE_SIZE
        self.STAT_BARS_HEALTH_SIZE = game.settings.STAT_BARS_HEALTH_SIZE
        self.HEARTS_IN_ROW = 6
        self.hearts_start_x = self.TILE_SIZE
        self.hearts_start_y = self.STAT_BARS_HEALTH_SIZE * 0.5

        self.font_path = 'resources/fonts/IsaacGame.ttf'
        self.font_size_offset = self.get_font_size_offset()
        self.font = pygame.font.Font(self.font_path, int(self.STAT_BARS_HEALTH_SIZE + self.font_size_offset))
        self.font_color = BLACK

        self.coin = game.image_loader.get_stat_bar_image("coin")
        self.coin_x = self.TILE_SIZE // 5
        self.coin_y = int(self.TILE_SIZE * 1.6)
        self.coin_center_y = self.coin_y + self.coin.get_height() // 2

        self.bomb = game.image_loader.get_stat_bar_image("bomb")
        self.bomb_y_offset = self.coin.get_height() + math.ceil(11 * self.game.settings.SCALE)

        self.empty_heart = game.image_loader.get_stat_bar_image("empty_heart")
        self.full_heart = game.image_loader.get_stat_bar_image("full_heart")
        self.one_quarter_heart = game.image_loader.get_stat_bar_image("one_quarter_heart")
        self.half_heart = game.image_loader.get_stat_bar_image("half_heart")
        self.three_quarters_heart = game.image_loader.get_stat_bar_image("three_quarters_heart")

        self.full_hearts_cntr = 0
        self.is_fractional_heart = 0
        self.empty_hearts_cntr = 0
        self.heart_x = 100
        self.hearts_drawn = 0

        self.ceil_health = self.floor_health = 0

        # PROGRESS
        self.MAX_ROOMS_TO_CLEAR = ROOM_NUMBER - 2
        self.current_rooms_cleared = 0

        self.full_bar_image = game.image_loader.get_stat_bar_image("full_bar")
        self.empty_bar_image = game.image_loader.get_stat_bar_image("empty_bar")
        
        self.bar_x_offset = int(5 * self.game.settings.SCALE)
        self.bar_y_offset = int(10 * self.game.settings.SCALE)
        self.bar_width = self.game.image_loader.minimap["background"].get_width() - 2* self.bar_x_offset
        self.bar_height = int(self.full_bar_image.get_height() * self.game.settings.SCALE)
        self.bar_x = self.game.settings.WIN_WIDTH - self.bar_width - self.bar_x_offset
        self.bar_y = self.game.image_loader.minimap["background"].get_height() + self.bar_y_offset
        self.resize_bars()

        # TIME
        self.time_font = pygame.font.Font(self.font_path, int(self.STAT_BARS_HEALTH_SIZE))
        self.time_x, self.time_y = self.prepare_time()
        self.ticks_passed = 0
        self.h = 0
        self.min = 0
        self.sec = 0
        
    def resize_bars(self):
        self.full_bar_image = pygame.transform.scale(self.full_bar_image, (self.bar_width, self.bar_height))
        self.empty_bar_image = pygame.transform.scale(self.empty_bar_image, (self.bar_width, self.bar_height))

    def prepare_time(self):
        test_time = '00:00:00'
        time_width = self.time_font.size(test_time)[0]
        width = self.bar_width + 2 * self.bar_x_offset
        x = self.bar_x - self.bar_x_offset
        x_offset = (width - time_width) // 2
        return x + x_offset, self.bar_y + int(24 * self.game.settings.SCALE)

    def update_and_draw(self, screen):
        self.calculate_hearts_cntrs()
        self.draw_health_bar(screen)
        self.draw_coin(screen)
        self.draw_bomb(screen)
        self.draw_time(screen)
        self.draw_progress(screen)

    def calculate_hearts_cntrs(self):
        health = self.player.health
        self.floor_health = int(health)
        self.ceil_health = math.ceil(health)
        self.is_fractional_heart = int(health > self.floor_health + 0.1 and health < self.ceil_health - 0.1)
        if health <= 0:
            self.is_fractional_heart = False 

        self.full_hearts_cntr = max(self.floor_health, 0) + int(health - self.floor_health >= 0.9)
        self.empty_hearts_cntr = self.player.max_health - self.full_hearts_cntr
        self.empty_hearts_cntr -= self.is_fractional_heart

    def draw_health_bar(self, screen):
        self.heart_x = self.hearts_start_x
        self.heart_y = self.hearts_start_y
        self.hearts_drawn = 0
        for _ in range(self.full_hearts_cntr):
            self.check_to_draw_second_row_hearts()
            self.draw_and_update_variables(screen, self.full_heart)
        
        if self.is_fractional_heart:
            heart_to_draw = None
            health = self.player.health
            if health < self.floor_health + 0.25:
                heart_to_draw = self.one_quarter_heart
            elif health < self.floor_health + 0.63:
                heart_to_draw = self.half_heart
            elif health < self.floor_health + 0.85:
                heart_to_draw = self.three_quarters_heart

            if heart_to_draw is not None: 
                self.check_to_draw_second_row_hearts()
                self.draw_and_update_variables(screen, heart_to_draw)
        
        for _ in range(self.empty_hearts_cntr):
            self.check_to_draw_second_row_hearts()
            self.draw_and_update_variables(screen, self.empty_heart)

    def draw_and_update_variables(self, screen, what_to_draw):
        screen.blit(what_to_draw, (self.heart_x, self.heart_y))
        self.hearts_drawn += 1
        self.heart_x += self.STAT_BARS_HEALTH_SIZE + 4

    def check_to_draw_second_row_hearts(self):
        if self.hearts_drawn % self.HEARTS_IN_ROW == 0:
            self.heart_y += self.STAT_BARS_HEALTH_SIZE
            self.heart_x = self.hearts_start_x

    def get_font_size_offset(self):
        return math.ceil(11 * self.game.settings.SCALE)

    def draw_coin(self, screen):
        text = self.font.render(str(self.player.coins), True, (255, 255, 255))
        screen.blit(self.coin, (self.coin_x, self.coin_y))
        screen.blit(text, (self.coin_x + self.TILE_SIZE//3, self.coin_y))
    
    def draw_bomb(self, screen):
        text = self.font.render(str(self.player.bombs), True, (255, 255, 255))
        screen.blit(self.bomb, (self.coin_x, self.coin_y + self.bomb_y_offset))
        screen.blit(text, (self.coin_x + self.TILE_SIZE//3, self.coin_y + self.bomb_y_offset))

    def draw_progress(self, screen):
        width = self.player.rooms_cleared / self.MAX_ROOMS_TO_CLEAR * self.full_bar_image.get_width()
        height = self.full_bar_image.get_height()
        screen.blit(self.empty_bar_image, (self.bar_x, self.bar_y))
        screen.blit(self.full_bar_image, (self.bar_x, self.bar_y), (0, 0, width, height))

    def draw_time(self, screen):
        self.update_time_values()
        time = f'{self.h // 10}{self.h % 10}:{self.min // 10}{self.min % 10}:{self.sec // 10}{self.sec % 10}'
        text = self.time_font.render(time, True, (255, 255, 255))
        screen.blit(text, (self.time_x, self.time_y))
    
    def update_time_values(self):
        self.ticks_passed += 1
        if self.ticks_passed == FPS:
            self.ticks_passed = 0
            self.sec += 1
            if self.sec == 60:
                self.sec = 0
                self.min += 1
                if self.min == 60:
                    self.min = 0
                    self.h += 1