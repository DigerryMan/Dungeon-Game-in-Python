import pygame
from config import *

class Bomb(pygame.sprite.Sprite):
    def __init__(self, game, x, y, rotate = False):
        self.game = game
        self.image_type = "bomb"
        self.image = game.image_loader.bombs[self.image_type + "0"].copy()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.explosion_radius = self.game.settings.TILE_SIZE * 2

        self.x = x
        self.y = y

        self.groups = game.all_sprites, game.attacks, game.entities
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.rotate = rotate

        self.frames = 4
        self.time_per_frame = 10
        self.current_frame = 0
        self.timer = 0

        self.next_frame()

        self.exploded = False

    def next_frame(self):
        self.current_frame = (self.current_frame + 1) % self.frames

        if self.rotate:
            self.image = pygame.transform.flip(self.game.image_loader.bombs[f"{self.image_type}{self.current_frame}"].copy(), True, False)

        else:
            self.image = self.game.image_loader.bombs[f"{self.image_type}{self.current_frame}"].copy()

    def explode(self):
        self.image_type = "bomb_explosion"
        self._layer = 10000
        self.frames = 12
        self.current_frame = 0
        self.time_per_frame = 5
        self.image = self.game.image_loader.bombs[f"{self.image_type}{self.current_frame}"].copy()
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y - self.game.settings.TILE_SIZE // 1.5)
        self.check_collisions()
        self.game.sound_manager.play("explosion")

    def check_collisions(self):
        for group in [self.game.player_sprite, self.game.enemies, self.game.blocks]:
            for sprite in group:
                distance = ((sprite.rect.centerx - self.rect.centerx)**2 + (sprite.rect.centery - self.rect.centery)**2)**0.5
                if distance <= self.explosion_radius:
                    sprite.get_bombed()

    def update(self):
        self.timer += 1
        if self.timer % self.time_per_frame == 0:
            self.next_frame()

        if self.timer >= 100 and not self.exploded:
            self.explode()
            self.exploded = True

        if self.exploded and self.timer == 100 + self.frames * self.time_per_frame:
            self.kill()