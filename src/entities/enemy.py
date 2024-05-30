import pygame
import random
from config import *
from entities.bullet import Bullet
from entities.enemy_collisions import EnemyCollisions
from items.lootables.golden_coin import GoldenCoin
from items.lootables.pickup_heart import PickupHeart
from items.lootables.silver_coin import SilverCoin
from items.stat_items.categories import Categories
from items.stat_items.item import Item
from map.block import Block
from utils.directions import Directions
from abc import ABC, abstractmethod

from utils.image_transformer import ImageTransformer

class Enemy(pygame.sprite.Sprite, ABC):
    is_group_attacked:bool = False
    def __init__(self, game, x:int, y:int, check_block_colisions:bool=True, 
                 is_wandering:bool=True, bullet_decay_sec:float=0):
        #CHANGEABLE STATS
        self._health = 4
        self._damage = 1
        self._collision_damage = 1
        self.size = "Small"
        
        self._speed = (3 + (random.random() * 2 - 1)) * game.settings.SCALE
        self._chase_speed_debuff = 1
        self._projectal_speed = 10
        self._shot_cd = int(2.5 * FPS)
        self._shot_time_left = self._shot_cd

        self._wander_interval = [int(0.7 * FPS), int(1.7 * FPS)]
        self._idle_interval = [int(1.2 * FPS), int(2.5 * FPS)]

        #POSITION
        self.MOB_SIZE = game.settings.MOB_SIZE
        self.x_change = 0
        self.y_change = 0
        
        #SKINS
        self.image = pygame.Surface([self.MOB_SIZE, self.MOB_SIZE])
        self.unchanged_image = self.image.copy()
        self.mask = pygame.mask.from_surface(self.image) 
        self.frame = None
        self.images = []

        #HITBOX
        self.rect = self.image.get_rect()
        self.rect.x = x * game.settings.TILE_SIZE
        self.rect.y = y * game.settings.TILE_SIZE
        self._layer = self.rect.bottom

        # GETTING HIT ANIMATION
        self.hit_time_cd = int(0.1 * FPS)
        self.hit_time = 0     
        self.is_change_of_frame = False  

        #REST
        self.collisions_manager = EnemyCollisions(self, game, check_block_colisions)
        
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

        self.terrain_collisions()
        self.correct_facing()
        self.correct_layer()
        self.check_hit_and_animate()

        self.x_change = 0
        self.y_change = 0

    def terrain_collisions(self):
        self.collisions_manager.terrain_collisions()

    def check_hit_and_animate(self):
        if self.hit_time > 0:
            self.hit_time -= 1
            if self.hit_time == 0:
                self.restore_image_colors()
        self.is_change_of_frame = False
        self.animate()
        if self.is_change_of_frame and self.hit_time > 0:
            self.image = ImageTransformer.change_image_to_more_red(self.unchanged_image)

    def restore_image_colors(self):
        self.image = self.unchanged_image

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
        self.collisions_manager.collide_player()

    def attack(self):
        self._shot_time_left -= 1
        if self._shot_time_left <= 0:
            Bullet(self.game, self.rect.centerx, self.rect.centery, Directions.PLAYER, 
                   self._projectal_speed, False, self._damage, self._bullet_decay_sec)
            self.roll_next_shot_cd()
            self._shot_time_left = self._shot_cd

    def collide_blocks(self, orientation:str):
        self.collisions_manager.collide_blocks(orientation)

    def get_mask_colliding_sprite(self, rect_hits):
        self.collisions_manager.get_mask_colliding_sprite(self, rect_hits)

    def _correct_rounding(self):
        self.x_change += (1 if self.x_change >= 0 else -1)
        self.y_change += (1 if self.y_change >= 0 else -1)

    def roll_facing(self):
        rand = random.choice([self.facing.rotate_clockwise(), self.facing.rotate_counter_clockwise(), self.facing.reverse(), self.facing])
        self.facing = rand

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
        self.play_hit_sound()
        self._health -= dmg
        self._is_wandering = False
        self.group_attacked()
        self.check_if_dead()

        self.hit_time = self.hit_time_cd
        self.image = ImageTransformer.change_image_to_more_red(self.unchanged_image)
    
    def play_hit_sound(self):
        self.play_audio(f"enemyHit{random.randint(1, 3)}")

    def play_audio(self, audio:str):
        self.game.sound_manager.play(audio)

    def check_if_dead(self):
        if self._health <= 0:
            self.start_dying()

    def roll_interval(self, interval):
        return random.randint(interval[0], interval[1])

    def roll_next_shot_cd(self):
        self._shot_cd = random.randint(int(1.5*FPS), int(3*FPS))
            
    def correct_layer(self):
        self._layer = self.rect.bottom

    def correct_low_speed_enemies(self, axis:str):
        if self._speed//2 == 0:
            if axis == 'x':
                self.x_change = self._speed
            if axis == 'y':
                self.y_change = self._speed
    
    def start_dying(self, instant_death=True):
        self._is_dead = True
        self.play_death_sound()
        self.drop_lootable()
        if instant_death:
            self.final_death()
    
    def final_death(self):
        self.kill()

    def drop_lootable(self):
        if DROP_LOOT_EVERYTIME: #FOR TESTING PURPOSES!
            self.room.items.append(Item(self.game, self.rect.centerx, self.rect.centery, Categories.VERY_COMMON, False))
        else: 
            if random.random() < 0.3: #chance to have any drop at all
                if random.random() < 0.7: # chance to have a lootable (coin, heart, etc.)
                    if random.random() < 0.5:
                        self.room.items.append(SilverCoin(self.game, self.rect.centerx, self.rect.centery, False))
                    elif random.uniform(0, 0.5) < 0.3:
                        self.room.items.append(GoldenCoin(self.game, self.rect.centerx, self.rect.centery, False))
                    else:
                        self.room.items.append(PickupHeart(self.game, self.rect.centerx, self.rect.centery, False))
                else:
                    self.room.items.append(Item(self.game, self.rect.centerx, self.rect.centery, Categories.VERY_COMMON, False))

    def draw_additional_images(self, screen):
        pass

    @abstractmethod
    def animate(self):
        pass

    @staticmethod
    def check_group_attacked():
        return Enemy.is_group_attacked

    @staticmethod
    def group_attacked():
        Enemy.is_group_attacked = True
    
    def get_bombed(self):
        self.get_hit(1)

    def play_death_sound(self):
        if self.size == "Large":
            self.game.sound_manager.play(f"Death_Burst_Large_{random.randint(0, 1)}")
        elif self.size == "Small":
            self.game.sound_manager.play(f"Death_Burst_Small_{random.randint(0, 2)}")