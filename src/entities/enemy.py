import pygame
import random
from config import *
from entities.bullet import Bullet
from items.lootables.golden_coin import GoldenCoin
from items.lootables.pickup_heart import PickupHeart
from items.lootables.silver_coin import SilverCoin
from items.stat_items.categories import Categories
from items.stat_items.item import Item
from map.block import Block
from utils.directions import Directions
from abc import ABC, abstractmethod

class Enemy(pygame.sprite.Sprite, ABC):
    is_group_attacked:bool = False
    def __init__(self, game, x:int, y:int, check_block_colisions:bool=True, 
                 is_wandering:bool=True, bullet_decay_sec:float=0):
        #CHANGEABLE STATS
        self._health = 4
        self._damage = 1
        self._collision_damage = 1
        
        self._speed = (3 + (random.random() * 2 - 1)) * game.settings.SCALE
        self._chase_speed_debuff = 1
        self._projectal_speed = 10
        self._shot_cd = int(2.5 * FPS)
        self._shot_time_left = self._shot_cd

        self._wander_interval = [int(0.7 * FPS), int(1.7 * FPS)]
        self._idle_interval = [int(1.2 * FPS), int(2.5 * FPS)]

        #POSITION
        self.width = game.settings.MOB_SIZE
        self.height = game.settings.MOB_SIZE
        self.x_change = 0
        self.y_change = 0
        
        #SKINS
        self.image = pygame.Surface([self.width, self.height])
        self.animation_loop = 1
        self.mask = pygame.mask.from_surface(self.image) 

        #HITBOX
        self.rect = self.image.get_rect()
        self.rect.x = x * game.settings.TILE_SIZE
        self.rect.y = y * game.settings.TILE_SIZE
        self._layer = self.rect.bottom
     
        #REST
        self._check_block_colisions = check_block_colisions
        self.facing = random.choice([Directions.LEFT, Directions.RIGHT])

        self._is_wandering = is_wandering
        self._wander_time = self.roll_interval(self._wander_interval)
        self._wander_time_left = self._wander_time
        
        self._idle_time = self.roll_interval(self._idle_interval)
        self._is_idling = self._is_wandering
        self._idle_time_left = self._idle_time

        self._bullet_decay_sec = bullet_decay_sec

        self._is_dead = False
        self.game = game
        self.room = game.map.get_current_room()
        self.groups = self.game.all_sprites, self.game.enemies, self.game.entities
        pygame.sprite.Sprite.__init__(self, self.groups)
   

    def update(self):
        self.move()
        self.collide_player()
        if not self._is_wandering:
            self.attack()

        self.rect.x += self.x_change
        if self._check_block_colisions:
            self.collide_blocks('x')

        self.rect.y += self.y_change
        if self._check_block_colisions:
            self.collide_blocks('y')
        
        self.correct_facing()
        self.correct_layer()
        self.animate()

        self.x_change = 0
        self.y_change = 0

    def move(self):
        if not self._is_dead:
            if self._is_wandering:
                self.wander()
            else:
                self.move_because_of_player() 
        
    def wander(self):
        if self._is_idling:
            if not self.check_group_attacked():
                self.idle()
            else:
                self._is_idling = False
                self._is_wandering = False
        
        else:
            self._wander_time_left -= 1
            if self._wander_time_left <= 0:
                self._is_idling = True
                self._wander_time = self.roll_interval(self._wander_interval)
                self._wander_time_left = self._wander_time
            
            else:
                if self.facing == Directions.LEFT:
                    self.x_change = -self._speed//2

                elif self.facing == Directions.RIGHT:
                    self.x_change = self._speed//2
                    self.correct_low_speed_enemies("x")

                elif self.facing == Directions.UP:
                    self.y_change = -self._speed//2

                elif self.facing == Directions.DOWN:
                    self.y_change = self._speed//2
                    self.correct_low_speed_enemies("y")
                
    def idle(self):
        self._idle_time_left -= 1
        if self._idle_time_left <= 0:
            self._is_idling = False
            self.roll_facing()
            self._idle_time = self.roll_interval(self._idle_interval)
            self._idle_time_left = self._idle_time

    def move_because_of_player(self, chase:bool=True):
        player_vector = pygame.math.Vector2(self.game.get_player_rect().center)
        enemy_vector = pygame.math.Vector2(self.rect.center)

        distance = (player_vector - enemy_vector).magnitude()
        if distance > 3:
            direction = None

            if distance > 0:
                direction = (player_vector - enemy_vector).normalize()
            else:
                direction = pygame.math.Vector2()
            
            speed = self._speed
            if not chase:
                direction.rotate_ip(180)
                speed = self._speed * self._chase_speed_debuff

            velocity = direction * speed
            
            self.x_change = velocity.x
            self.y_change = velocity.y
            self._correct_rounding()
            self.correct_facing()

    def collide_player(self):
        rect_hits = pygame.sprite.spritecollide(self, self.game.player_sprite, False)
        if rect_hits:
            mask_hits = self.get_mask_colliding_sprite(rect_hits)
            if mask_hits:
                self.game.damage_player(self._collision_damage)
                if self._is_wandering:
                    self._is_wandering = False
                    self.group_attacked()

    def attack(self):
        self._shot_time_left -= 1
        if self._shot_time_left <= 0:
            Bullet(self.game, self.rect.centerx, self.rect.centery, Directions.PLAYER, 
                   self._projectal_speed, False, self._damage, self._bullet_decay_sec)
            self.roll_next_shot_cd()
            self._shot_time_left = self._shot_cd

    def collide_blocks(self, orientation:str):
        rect_hits = pygame.sprite.spritecollide(self, self.game.collidables, False)
        if rect_hits:
            mask_hits = self.get_mask_colliding_sprite(rect_hits)
            if mask_hits:
                if orientation == 'x':
                    self.rect.x -= self.x_change

                if orientation == 'y':
                    self.rect.y -= self.y_change

    def get_mask_colliding_sprite(self, rect_hits):
        for sprite in rect_hits:
            if isinstance(sprite, Block): #done in order to prevent mobs from getting blocked by rough blocks
                block_surface = pygame.Surface((sprite.rect.width, sprite.rect.height))
                block_mask = pygame.mask.from_surface(block_surface)
                offset_x = sprite.rect.x - self.rect.x
                offset_y = sprite.rect.y - self.rect.y
                if self.mask.overlap(block_mask, (offset_x, offset_y)):
                    return sprite
                
            if pygame.sprite.collide_mask(self, sprite):
                return sprite

    def _correct_rounding(self):
        if self.x_change < 0:
            self.x_change = self.x_change - 1
        else:
            self.x_change = self.x_change + 1

        if self.y_change < 0:
            self.y_change = self.y_change - 1
        else:
            self.y_change = self.y_change + 1

    def roll_facing(self):
        rand = random.randint(1, 4)
        if rand == 1:
            self.facing = self.facing.rotate_clockwise()

        elif rand == 2:
            self.facing = self.facing.rotate_counter_clockwise()
           
        elif rand == 3:
            self.facing = self.facing.reverse()

    def correct_facing(self):
        y_abs = abs(self.y_change)
        x_abs = abs(self.x_change)

        if(x_abs >= y_abs):
            if self.x_change < 0:
                self.facing = Directions.LEFT
            elif self.x_change > 0:
                self.facing = Directions.RIGHT
        else:
            if self.y_change < 0:
                self.facing = Directions.UP
            elif self.y_change > 0:
                self.facing = Directions.DOWN 

    def get_hit(self, dmg:int):
        self._health -= dmg
        self._is_wandering = False
        self.group_attacked()
        self.check_if_dead()
    
    def check_if_dead(self):
        if self._health <= 0:
            self.start_dying()

    def roll_interval(self, interval):
        return random.randint(interval[0], interval[1])

    def roll_next_shot_cd(self):
        self._shot_cd = random.randint(int(1.5*FPS), int(3*FPS))

    @abstractmethod
    def animate(self):
        pass
            
    def correct_layer(self):
        self._layer = self.rect.bottom

    def correct_low_speed_enemies(self, axis:str):
        if self._speed//2 == 0:
            if axis == 'x':
                self.x_change = self._speed
            if axis == 'y':
                self.y_change = self._speed
    
    def start_dying(self):
        self._is_dead = True
        self.kill()
        self.drop_lootable()

    def drop_lootable(self):
        if random.random() < 0.3: #chance to have any drop at all
            if random.random() < 0.7: # chance to have a lootable (coin, heart, etc.)
                if random.random() < 0.5:
                    self.room.items.append(SilverCoin(self.game, self.rect.centerx, self.rect.centery, drop_animtion = False))
                elif random.uniform(0, 0.5) < 0.3:
                    self.room.items.append(GoldenCoin(self.game, self.rect.centerx, self.rect.centery, drop_animtion = False))
                else:
                    self.room.items.append(PickupHeart(self.game, self.rect.centerx, self.rect.centery, drop_animtion = False))
            else:
                self.room.items.append(Item(self.game, self.rect.centerx, self.rect.centery, Categories.VERY_COMMON, drop_animtion = False))

    @abstractmethod
    def draw_additional_images(self, screen):
        pass

    @staticmethod
    def check_group_attacked():
        return Enemy.is_group_attacked

    @staticmethod
    def group_attacked():
        Enemy.is_group_attacked = True
    
        
