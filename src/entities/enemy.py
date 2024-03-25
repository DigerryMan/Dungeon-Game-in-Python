import pygame
import random
from config import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, x:int, y:int):
        self.game = game
        self.groups = self.game.all_sprites, self.game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self.__speed = 7
        self.x_change = 0
        self.y_change = 0

        self.__health = 1
        self.__damage = 1

        self.facing = random.choice(['left', 'right'])
        self.animation_loop = 1
        self.movement_loop = 0
        self.max_travel = random.randint(10,30)

        #WCZYTANIE TEKSTURY DLA MOBA
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(GREEN)
        #self.image.set_colorkey(BLACK)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self._layer = self.rect.bottom
    
    def update(self):
        self.move()
        self.animate()
        self.collide_enemy()

        self.rect.x += self.x_change
        self.rect.y += self.y_change

        self._layer = self.rect.bottom

        self.x_change = 0
        self.y_change = 0

    def move(self):
        if self.facing == 'left':
            self.x_change -= self.__speed
            self.movement_loop -= 1
            if self.movement_loop <= -self.max_travel:
                self.facing = 'right'
        
        if self.facing == 'right':
            self.x_change += self.__speed
            self.movement_loop += 1
            if self.movement_loop >= self.max_travel:
                self.facing = 'left'

    def collide_enemy(self):
        hits = pygame.sprite.spritecollide(self, self.game.player_sprite, False)
        if hits:
            self.game.damage_player(self.__damage)
            #print("enemy: ", self._layer)
            self.game.playing = False

    def get_hit(self, dmg:int):
        self.__health -= dmg
        if self.__health <= 0:
            self.kill()

    def animate(self):
        pass