import math
import pygame
from config import BLACK

class StatBars():
    def __init__(self, game, player):
        self.game = game
        self.player = player
        self.font_path = 'resources/fonts/IsaacGame.ttf'
        self.font = pygame.font.Font(self.font_path, 36)
        self.font_color = BLACK
        self.TILE_SIZE = game.settings.TILE_SIZE
        self.STAT_BARS_HEALTH_SIZE = game.settings.STAT_BARS_HEALTH_SIZE
        self.HEARTS_IN_ROW = 6
        self.HEARTS_STARTING_X = self.TILE_SIZE * 2
        self.HEARTS_STARTING_Y = self.STAT_BARS_HEALTH_SIZE * 0.5

        self.coin = game.image_loader.get_stat_bar_image("coin")
        self.empty_heart = game.image_loader.get_stat_bar_image("empty_heart")
        self.full_heart = game.image_loader.get_stat_bar_image("full_heart")
        self.half_heart = game.image_loader.get_stat_bar_image("half_heart")

        self.full_hearts_cntr = 0
        self.is_half_heart_cntr = 0
        self.empty_hearts_cntr = 0
        self.heart_x = 100
        self.hearts_drawn = 0

    def calculate_hearts(self):
        health = self.player.health
        floor_health = int(health)
        ceil_health = math.ceil(health)
        self.is_half_heart_cntr = int(health >= floor_health + 0.25 and health < ceil_health - 0.25)
        if health <= 0:
            self.is_half_heart_cntr = 0 

        self.full_hearts_cntr = max(floor_health, 0)
        self.empty_hearts_cntr = self.player.max_health - self.full_hearts_cntr
        self.empty_hearts_cntr -= self.is_half_heart_cntr

    def update_and_draw(self, screen):
        self.calculate_hearts()
        self.draw_health_bar(screen)
        self.draw_money(screen)

    def draw_health_bar(self, screen):
        self.heart_x = self.HEARTS_STARTING_X
        self.heart_y = self.HEARTS_STARTING_Y
        self.hearts_drawn = False
        for _ in range(self.full_hearts_cntr):
            self.check_to_draw_second_row_hearts()
            self.draw_and_update_variables(screen, self.full_heart)
        
        if self.is_half_heart_cntr:
            self.check_to_draw_second_row_hearts()
            self.draw_and_update_variables(screen, self.half_heart)
        
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
            self.heart_x = self.HEARTS_STARTING_X

    def draw_money(self, screen):
        pass
        #font = pygame.font.Font(self.font_path, 36)
        #text = font.render(f'Money: {self.player.coins}', True, (255, 255, 255))
        #screen.blit(text, (10, 40))