import random
import pygame
from config import *
from entities.bullet import Bullet
from entities.enemy import Enemy
from utils.directions import Directions

class Slime(Enemy):
    def __init__(self, game, x: int, y: int):
        super().__init__(game, x, y, check_block_colisions=False, 
                         is_wandering=False,bullet_decay_sec=3)

        #CHANGEABLE STATS
        self._health = 6
        self._speed = 2
        self._projectal_speed = 6
        self.jump_range = 3

        #SKINS
        self.image.fill(ORANGE)

        #POSITION
        self.x = x
        self.y = y

        self.room_layout = self.game.map.get_current_room().get_block_layout()
        self.possible_jumps = [(i,j) for i in range(-self.jump_range, self.jump_range) 
                               for j in range(-self.jump_range, self.jump_range)]
        self.possible_jumps.remove((0,0))

        self.is_jumping = False
        self.new_jump_x = x
        self.new_jump_y = y
        self.old_jump_x = x
        self.old_jump_y = y
        self.jump_time = 1000
        self.jump_cd = 1500
        self.jump_start_time = 0
        self.jump_end_time = -self.jump_cd - 1
        self.jump_height = 0
        self.horizontal_speed = 0
        self.vertical_speed = 0
        self.prepare_atack = False


    def move(self):
        now = pygame.time.get_ticks()
        if self.is_jumping:
            self.jump(now)
        elif now - self.jump_end_time > self.jump_cd:
            self.find_possible_moves(now)
    
    def jump(self, now):
        if now - self.jump_start_time > self.jump_time:
            self.x = self.new_jump_x
            self.y = self.new_jump_y
            self.rect.x = self.new_jump_x * TILE_SIZE
            self.rect.y = self.new_jump_y * TILE_SIZE
            
            self.jump_end_time = now
            self.is_jumping = False
            self.prepare_atack = True
        else:
            elapsed_time = (now - self.jump_start_time) / 1000
            y = self.old_jump_y + self.vertical_speed * elapsed_time - 0.5 * 9.81 * elapsed_time ** 2
            x = self.old_jump_x + (elapsed_time * 1000 / self.jump_time) * (self.new_jump_x - self.old_jump_x)
           
            self.rect.x = int(x * TILE_SIZE)
            self.rect.y = int(y * TILE_SIZE)
    
     

    def find_possible_moves(self, now):
        possible_moves = []
        for jump in self.possible_jumps:
            new_x = self.x + jump[0] 
            new_y = self.y + jump[1]
            if self.is_valid_move(new_x, new_y):
                possible_moves.append((new_x, new_y))
        
        if possible_moves:
            self.old_jump_x, self.old_jump_y = self.new_jump_x, self.new_jump_y
            self.new_jump_x, self.new_jump_y = random.choice(possible_moves)
            self.calculate_parabolic_jump()
        
        self.jump_start_time = now
        self.is_jumping = True
    
    def calculate_parabolic_jump(self):
        self.jump_height = abs(self.old_jump_y - self.new_jump_y)
        self.vertical_speed = 2 * self.jump_height / self.jump_time / 1000
        self.horizontal_speed = (self.new_jump_x - self.old_jump_x) / self.jump_time / 1000

    def is_valid_move(self, x, y):
        # '#' walls
        if x <= 0 or x >= MAP_WIDTH - 1 or y <= 0  or y >= MAP_HEIGHT - 1:
            return False
        return not self.room_layout[y][x] in WALL_MARKS

    
    def attack(self):
        if self.prepare_atack:
            self.prepare_atack = False
            Bullet(self.game, self.rect.centerx, self.rect.centery, Directions.LEFT, 
                   speed=self._projectal_speed, is_friendly=False, dmg=1, 
                   time_decay_in_seconds=self._bullet_decay_sec)
            
            Bullet(self.game, self.rect.centerx, self.rect.centery, Directions.RIGHT, 
                   speed=self._projectal_speed, is_friendly=False, dmg=1, 
                   time_decay_in_seconds=self._bullet_decay_sec)
            
            Bullet(self.game, self.rect.centerx, self.rect.centery, Directions.UP, 
                   speed=self._projectal_speed, is_friendly=False, dmg=1, 
                   time_decay_in_seconds=self._bullet_decay_sec)
            
            Bullet(self.game, self.rect.centerx, self.rect.centery, Directions.DOWN, 
                   speed=self._projectal_speed, is_friendly=False, dmg=1, 
                   time_decay_in_seconds=self._bullet_decay_sec)
    
    