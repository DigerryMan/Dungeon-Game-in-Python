import math
import pygame
from config import BLACK
from utils.image_loader import ImageLoader

class StatBars():
    def __init__(self, game, player):
        self.game = game
        self.player = player
        self.font_path = 'resources/fonts/IsaacGame.ttf'
        self.font = pygame.font.Font(self.font_path, 36)
        self.font_color = BLACK

        self.coin = game.image_loader.get_stat_bar_image("coin")
        self.empty_heart = game.image_loader.get_stat_bar_image("empty_heart")
        self.full_heart = game.image_loader.get_stat_bar_image("full_heart")
        self.half_heart = game.image_loader.get_stat_bar_image("half_heart")

        self.full_hearts_cntr = 0
        self.is_half_heart_cntr = 0
        self.empty_hearts_cntr = 0
        self.heart_x = 100

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

    def update(self):
        self.calculate_hearts()
        self.draw_health_bar()
        self.draw_money()

    def draw_health_bar(self):
        self.heart_x = 300
        self.heart_y = 200
        for _ in range(self.full_hearts_cntr):
            self.game.screen.blit(self.full_heart, (self.heart_x, self.heart_y))
            self.heart_x += 50
        
        if self.is_half_heart_cntr:
            self.game.screen.blit(self.half_heart, (self.heart_x, self.heart_y))
            self.heart_x += 50
        
        for _ in range(self.empty_hearts_cntr):
            self.game.screen.blit(self.empty_heart, (self.heart_x, self.heart_y))
            self.heart_x += 50

    def draw_money(self):
        pass
        #font = pygame.font.Font(self.font_path, 36)
        #text = font.render(f'Money: {self.player.coins}', True, (255, 255, 255))
        #self.game.screen.blit(text, (10, 40))