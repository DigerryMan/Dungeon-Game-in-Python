import random
import pygame
from config import *
from items.stat_items.categories import Categories
from items.stat_items.item import Item
from map.block import Block

class ShopStand(Block):
    def __init__(self, game, x, y):
        super().__init__(game, x, y, is_collidable = False)
        self.content = self.get_random_item()
        self.image = self.content.image
        self.price = 0

    def buy_item(self):
        if self.game.player.coins >= self.price:
            self.game.player.coins -= self.price
            self.game.player.eq.add_item(self.content.item)
            self.game.map.get_current_room().remove_shop_stand(self)
            self.kill()

    def update(self):
        player_pos = pygame.Vector2(self.game.player.rect.centerx, self.game.player.rect.centery)
        shop_pos = pygame.Vector2(self.rect.centerx, self.rect.centery)
        distance = player_pos.distance_to(shop_pos)

        if distance < self.game.settings.TILE_SIZE and self.game.space_pressed:
            self.buy_item()

    def get_random_item(self):
        if random.random() < 0.75:
            self.price = 10
            return Item(self.game, -1000, -1000, Categories.COMMON, drop_animtion = False)
        
        self.price = 30
        return Item(self.game, -1000, -1000, Categories.EPIC, drop_animtion = False)
    
    def draw(self, surface):
        # Rysuj obrazek
        surface.blit(self.image, self.rect)

        # Stwórz powierzchnię z tekstem
        font = pygame.font.Font(None, 24)  # Wybierz czcionkę
        text = font.render(str(self.price), True, (255, 255, 255))  # Stwórz tekst

        # Oblicz pozycję tekstu
        text_pos = self.rect.bottomleft

        # Rysuj tekst
        surface.blit(text, text_pos)