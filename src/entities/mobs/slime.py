import random
import pygame
from config import *
from entities.bullet import Bullet
from entities.enemy import Enemy
from utils.directions import Directions

class Slime(Enemy):
    def __init__(self, game, x: int, y: int):
        super().__init__(game, x, y, check_block_colisions=False, 
                         is_wandering=False, bullet_decay_sec=3)

        #CHANGEABLE STATS
        self._health = 6
        self._projectal_speed = 6
        
        self.t = random.random() * 0.5 + 0.8 #time of jump in sec
        self.jump_time = int(self.t * FPS) 
        self.jump_cd = int((random.random() * 0.8 + 1.2) * FPS)
        self._jump_range = 3 # has to be min 2

        #SKINS
        self.MOB_SIZE = game.settings.MOB_SIZE
        self.img = game.image_loader.get_image('slime')
        self.frame = self.img.subsurface(pygame.Rect(0, 0, 32, 32))
        self.frame = pygame.transform.scale(self.frame, (self.MOB_SIZE, self.MOB_SIZE))
        self.image = self.frame
        self.mask = pygame.mask.from_surface(self.image)
        self.frame_x = 0
        self.frame_y = 0
        self.animation_time = [0.95, 0.9, 0.8, 0.7, 0.5, 0.25, 0.18, 0.1]
        self.prepare_animation_time()

        #POSITION
        self.x = x
        self.y = y

        #MOVES
        self.room_layout = self.game.map.get_current_room().get_block_layout()
        self.possible_jumps = [(x_i, y_j) for x_i in range(-self._jump_range, self._jump_range + 1) 
                               for y_j in range(-self._jump_range, self._jump_range + 1)]
        self.correct_possible_jumps()

        #JUMPING
        self.is_jumping = False
        self.jump_time_left = 0
        self.next_jump_time_left = 0
        self.is_jumping_left = False

        self.new_jump_x = x
        self.new_jump_y = y
        self.old_jump_x = x
        self.old_jump_y = y

        #FOR Y CALCULATIONS
        self.z = 0
        self.v_x = 0
        self.tg = 0

        #REST
        self.prepare_atack = False

    def prepare_animation_time(self):
        for index, value in enumerate(self.animation_time):
            self.animation_time[index] = int(value * self.jump_time)

    def correct_possible_jumps(self):
        self.possible_jumps.remove((0, 0))
         #remove diagonal jumps
        for y in range(1, self._jump_range + 1):
            self.possible_jumps.remove((0, y))
            self.possible_jumps.remove((0, -y))
        
         #remove 1 block jumps
        for y in range(-1, 2):
            self.possible_jumps.remove((-1, y))
            self.possible_jumps.remove((1, y))
        

    def move(self):
        if self.is_jumping:
            self.jump()
        else:
            self.next_jump_time_left -= 1
            if self.next_jump_time_left <= 0:
                self.find_possible_moves()
                self.is_jumping = True
                self.jump_time_left = self.jump_time
    
    def jump(self):
        self.jump_time_left -= 1
        if self.jump_time_left <= 0: #end of jump
            self.x = self.new_jump_x
            self.y = self.new_jump_y
            self.rect.x = self.new_jump_x * self.game.settings.TILE_SIZE
            self.rect.y = self.new_jump_y * self.game.settings.TILE_SIZE

            self.next_jump_time_left = self.jump_cd            
            self.is_jumping = False
            self.prepare_atack = True

        else: #jump
            elapsed_time_sec = (self.jump_time - self.jump_time_left) / FPS
            y = self.calculate_current_y(elapsed_time_sec)
            x = self.old_jump_x + self.v_x * elapsed_time_sec
            self.rect.x = int(x * self.game.settings.TILE_SIZE) 
            self.rect.y = int(y * self.game.settings.TILE_SIZE)

    def find_possible_moves(self):
        possible_moves = []
        for jump in self.possible_jumps:
            new_x = self.x + jump[0] 
            new_y = self.y + jump[1]
            if self.is_valid_move(new_x, new_y):
                possible_moves.append((new_x, new_y))
        
        if possible_moves:
            self.old_jump_x, self.old_jump_y = self.new_jump_x, self.new_jump_y
            self.new_jump_x, self.new_jump_y = random.choice(possible_moves)
            if self.new_jump_x < self.old_jump_x:
                self.is_jumping_left = True
            else:
                self.is_jumping_left = False
            self.calculate_parabolic_jump()
        
    def calculate_parabolic_jump(self):
        self.z = self.new_jump_x - self.old_jump_x
        self.v_x = self.z / (self.t)
        self.tg = ((self.new_jump_y - self.old_jump_y) - 0.5 * 9.81 * (self.t) ** 2) / (self.v_x * (self.t))

    def calculate_current_y(self, t:float):
        return self.old_jump_y + self.v_x * t * self.tg + 0.5 * 9.81 * t ** 2

    def is_valid_move(self, x, y):
        # '#' walls
        if x <= 0 or x >= self.game.settings.MAP_WIDTH - 1 or y <= 0  or y >= self.game.settings.MAP_HEIGHT - 1:
            return False
        return (self.room_layout[y][x] not in WALL_MARKS) and (self.room_layout[y][x] != 'C')

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
    
    def correct_layer(self):
        if self.is_jumping:
            self._layer = self.rect.bottom + 2500
        else:
            self._layer = self.rect.bottom
    
    def animate(self):
        if self.is_jumping:
            if self.jump_time_left in self.animation_time:
                self.frame_x += 1
                if self.frame_x > 3:
                    self.frame_x = 0
                    self.frame_y += 1
                
                self.frame = self.img.subsurface(pygame.Rect(self.frame_x * 32, self.frame_y * 32, 32, 32))
                self.frame = pygame.transform.scale(self.frame, (self.MOB_SIZE, self.MOB_SIZE))
                
                if self.is_jumping_left:
                    self.frame = pygame.transform.flip(self.frame, True, False)
                
                self.image = self.frame
                self.mask = pygame.mask.from_surface(self.image)
        else:
            print("halo")
            self.frame_x = 0
            self.frame_y = 0