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
        self.jump_time = 1000
        self.jump_cd = 1500
        self.jump_start_time = 0
        self.jump_end_time = -self.jump_cd - 1
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
            print(self.prepare_atack)

    def find_possible_moves(self, now):
        possible_moves = []
        for jump in self.possible_jumps:
            new_x = self.x + jump[0] 
            new_y = self.y + jump[1]
            if self.is_valid_move(new_x, new_y):
                possible_moves.append((new_x, new_y))
        
        if possible_moves:
            self.new_jump_x, self.new_jump_y = random.choice(possible_moves)
            possible_moves.clear()
        
        self.jump_start_time = now
        self.is_jumping = True
        

    def is_valid_move(self, x, y):
        # '#' walls
        if x <= 0 or x >= MAP_WIDTH - 1 or y <= 0  or y >= MAP_HEIGHT - 1:
            return False
        if self.room_layout[y][x] == 'B' or self.room_layout[y][x] == '#' or self.room_layout[y][x] == 'D': 
            return False
        return True
    
    def attack(self):
        if self.prepare_atack:
            self.prepare_atack = False
            Bullet(self.game, self.rect.centerx, self.rect.centery, Directions.LEFT, 
                   speed=self._projectal_speed, is_friendly=False, dmg=1, time_decay_in_seconds=2.5)
            
            Bullet(self.game, self.rect.centerx, self.rect.centery, Directions.RIGHT, 
                   speed=self._projectal_speed, is_friendly=False, dmg=1, time_decay_in_seconds=2.5)
            
            Bullet(self.game, self.rect.centerx, self.rect.centery, Directions.UP, 
                   speed=self._projectal_speed, is_friendly=False, dmg=1, time_decay_in_seconds=2.5)
            
            Bullet(self.game, self.rect.centerx, self.rect.centery, Directions.DOWN, 
                   speed=self._projectal_speed, is_friendly=False, dmg=1, time_decay_in_seconds=2.5)
    
    