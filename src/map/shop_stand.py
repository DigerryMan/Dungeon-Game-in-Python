import random
import pygame
from items.stat_items.categories import Categories
from items.stat_items.item import Item
from map.block import Block

class ShopStand(Block):
    def __init__(self, game, x, y):
        super().__init__(game, x, y, is_collidable = False)
        self.content = self.get_random_item()
        self.image = self.content.image

        self.font_path = 'resources/fonts/IsaacGame.ttf'
        self.font = pygame.font.Font(self.font_path, 40)
        self.font_color = (255, 255, 255)
        self.text_pos = (self.rect.left, self.rect.bottom)
        self.text = self.font.render(str(self.price), True, self.font_color)

    def buy_item(self):
        if self.game.player.coins >= self.price:
            self.game.player.coins -= self.price
            self.game.player.eq.add_item(self.content.item)
            self.game.map.get_current_room().remove_shop_stand(self)
            self.kill()

        else:
            self.game.sound_manager.play("error")

    def update(self):
        player_pos = pygame.Vector2(self.game.player.rect.centerx, self.game.player.rect.centery)
        shop_pos = pygame.Vector2(self.rect.centerx, self.rect.centery)
        distance = player_pos.distance_to(shop_pos)

        if distance < self.game.settings.TILE_SIZE and self.game.space_pressed:
            self.buy_item()

    def get_random_item(self):
        if random.random() < 0.75:
            self.price = 25
            return Item(self.game, -1000, -1000, Categories.COMMON, drop_animation = False)
        
        self.price = 60
        return Item(self.game, -1000, -1000, Categories.EPIC, drop_animation = False)
    
    def draw(self):
        self.game.screen.blit(self.image, self.rect)
        self.game.screen.blit(self.text, self.text_pos)