import pygame
import random
from config import *
from entities.bullet import Bullet
from utils.directions import Directions

class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, x:int, y:int, check_block_colisions:bool=True):
        self.game = game
        self.groups = self.game.all_sprites, self.game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self._speed = 3
        self.x_change = 0
        self.y_change = 0
        self._check_block_colisions = check_block_colisions

        self._health = 1
        self._damage = 1
        self._collision_damage = 1
        self._attack_speed = 800
        self._last_attack = pygame.time.get_ticks()

        self.facing = random.choice([Directions.LEFT, Directions.RIGHT])
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
        self.collide_player()
        self.attack()

        self.rect.x += self.x_change
        if self._check_block_colisions:
            self.collide_blocks('x')

        self.rect.y += self.y_change
        if self._check_block_colisions:
            self.collide_blocks('y')
        
        self.change_facing()
        self.animate()

        self._layer = self.rect.bottom

        self.x_change = 0
        self.y_change = 0

    def move(self):
        player_vector = pygame.math.Vector2(self.game.get_player_rect().center)
        enemy_vector = pygame.math.Vector2(self.rect.center)

        distance = self.get_vector_distance(player_vector, enemy_vector)
        direction = None

        if distance > 0:
            direction = (player_vector - enemy_vector).normalize()
        else:
            direction = pygame.math.Vector2()
        
        velocity = direction * self._speed

        self.x_change = velocity.x
        self.y_change = velocity.y
        self._correct_rounding()
        
    def _correct_rounding(self):
        if self.x_change < 0:
            self.x_change = self.x_change - 1
        else:
            self.x_change = self.x_change + 1

        if self.y_change < 0:
            self.y_change = self.y_change - 1
        else:
            self.y_change = self.y_change + 1

    def change_facing(self):
        y_abs = abs(self.y_change)
        x_abs = abs(self.x_change)

        x_bigger_impact = x_abs >= y_abs
        if x_bigger_impact:
            if self.x_change < 0:
                self.facing = Directions.LEFT
            else:
                self.facing = Directions.RIGHT
        else:
            if self.y_change < 0:
                self.facing = Directions.UP
            else:
                self.facing = Directions.DOWN 

    def get_vector_distance(self, vector1, vector2):
        return (vector1 - vector2).magnitude()

    def collide_player(self):
        hits = pygame.sprite.spritecollide(self, self.game.player_sprite, False)
        if hits:
            self.game.damage_player(self._collision_damage)
            self.game.playing = False

    def collide_blocks(self, orientation:str):
        hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
        if hits:
            if orientation == 'x':
                if self.x_change > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                if self.x_change < 0:
                    self.rect.x = hits[0].rect.right

            if orientation == 'y':
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom

    def get_hit(self, dmg:int):
        self._health -= dmg
        if self._health <= 0:
            self.kill()
    
    def attack(self):
        pass
            
    def animate(self):
        pass
            
        