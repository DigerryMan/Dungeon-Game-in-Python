import pygame
from config import *
from map.block import Block

class ShopStand(Block):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.image.fill(BROWN)
        self.item = None
        self.price = 0
        self.active = True

    def set_item(self, item, price):
        self.item = item
        self.price = price

    def buy_item(self):
        if self.active:
            if self.game.player.coins >= self.price:
                self.game.player.coins -= self.price
                #self.game.player.inventory.add_item(self.item)
                self.active = False
                self.image.fill(DARK_BROWN)

    def update(self):
        player_pos = pygame.Vector2(self.game.player.rect.centerx, self.game.player.rect.centery)
        shop_pos = pygame.Vector2(self.rect.centerx, self.rect.centery)
        distance = player_pos.distance_to(shop_pos)

        if self.active and distance < self.game.settings.TILE_SIZE * 1.5:
                self.image.fill(RED)
                if self.game.e_pressed:
                    self.buy_item()
            
        else:
            self.image.fill(BROWN)