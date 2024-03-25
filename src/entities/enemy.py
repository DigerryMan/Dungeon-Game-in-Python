import pygame
import random
from config import *
from entities.bullet import Bullet

class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, x:int, y:int):
        self.game = game
        self.groups = self.game.all_sprites, self.game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self._speed = 7
        self.x_change = 0
        self.y_change = 0

        self._health = 1
        self._damage = 1
        self._attack_speed = 800
        self._last_attack = pygame.time.get_ticks()

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
        self.attack()

        self.rect.x += self.x_change
        self.rect.y += self.y_change

        self._layer = self.rect.bottom

        self.x_change = 0
        self.y_change = 0

    def move(self):
        if self.facing == 'left':
            self.x_change -= self._speed
            self.movement_loop -= 1
            if self.movement_loop <= -self.max_travel:
                self.facing = 'right'
        
        if self.facing == 'right':
            self.x_change += self._speed
            self.movement_loop += 1
            if self.movement_loop >= self.max_travel:
                self.facing = 'left'

    def collide_enemy(self):
        hits = pygame.sprite.spritecollide(self, self.game.player_sprite, False)
        if hits:
            self.game.damage_player(self._damage)
            self.game.playing = False

    def get_hit(self, dmg:int):
        self._health -= dmg
        if self._health <= 0:
            self.kill()
    
    def attack(self):
        now = pygame.time.get_ticks()
        if now - self._last_attack > self._attack_speed:
            self._last_attack = now
            Bullet(self.game, self.rect.centerx, self.rect.centery, 'left', False, self._damage)
            Bullet(self.game, self.rect.centerx, self.rect.centery, 'right', False, self._damage)
            
    def animate(self):
        pass
            
        