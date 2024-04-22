import random
import pygame
from config import *
from entities.enemy import Enemy
from utils.directions import Directions

class Maggot(Enemy):
    def __init__(self, game, x, y, moving_clockwise=random.choice([True, False])):
        super().__init__(game, x, y, False)
        #CHANGEABLE STATS
        self._health = 4
        self._speed = 3
        self._random_dir_change_cd = int(2 * FPS)
        
        #SKIN
        self.x_frame = 0
        self.y_frame = 0
        self.reversed_frame = False
        
        self.next_frame_ticks_cd = 5
        self.time = self.next_frame_ticks_cd

        self.MOB_SIZE = game.settings.MOB_SIZE
        self.img = game.image_loader.get_image("maggot")
        self.frame = self.img.subsurface(pygame.Rect(self.x_frame, 0, 32, 32))
        self.scaled_frame = pygame.transform.scale(self.frame, (self.MOB_SIZE, self.MOB_SIZE))
        self.image.blit(self.scaled_frame, (0, 0, self.MOB_SIZE, self.MOB_SIZE))

        #REST
        self.moving_clockwise = moving_clockwise
        self._change_of_direction_time_left = self._random_dir_change_cd
                
    def move(self):
        self.wall_collision()
        self.random_change_of_direction()
        if self.facing == Directions.LEFT:
            self.x_change -= self._speed

        if self.facing == Directions.RIGHT:
            self.x_change += self._speed
        
        if self.facing == Directions.UP:
            self.y_change -= self._speed

        if self.facing == Directions.DOWN:
            self.y_change += self._speed
        
    def attack(self):
        pass

    def wall_collision(self):
        hits = pygame.sprite.spritecollide(self, self.game.collidables, False)

        if hits:
            if self.facing == Directions.LEFT:
                self.rect.x = hits[0].rect.right 

            elif self.facing == Directions.RIGHT:
                self.rect.x = hits[0].rect.left - self.game.settings.MOB_SIZE

            elif self.facing == Directions.UP:
                self.rect.y = hits[0].rect.bottom

            elif self.facing == Directions.DOWN:
                self.rect.y = hits[0].rect.top - self.game.settings.MOB_SIZE

            self.rotate_facing()
            
    def random_change_of_direction(self):
        self._change_of_direction_time_left -= 1
        if self._change_of_direction_time_left <= 0:
            self.roll_rotation_cd(int(0.4 * FPS), int(2.2 * FPS))
            self._change_of_direction_time_left = self._random_dir_change_cd
            
            self.rotate_facing()

    def rotate_facing(self):
        if self.moving_clockwise:
            self.facing = self.facing.rotate_clockwise()
        else:
            self.facing = self.facing.rotate_counter_clockwise()

        
    def roll_rotation_cd(self, mini:int, maxi:int):
        self._random_dir_change_cd = random.randint(mini, maxi)

    def next_frame(self):
        self.x_frame = (self.x_frame + 1) % 4
        self.set_y_frame() 
        self.frame = self.img.subsurface(pygame.Rect(self.x_frame * 32, self.y_frame * 32, 32, 32))
        if self.reversed_frame:
            self.frame = pygame.transform.flip(self.frame, True, False)
        
        self.image = pygame.transform.scale(self.frame, (self.MOB_SIZE, self.MOB_SIZE))


    def set_y_frame(self):
        self.reversed_frame = False
        if self.facing == Directions.LEFT:
            self.y_frame = 0
            self.reversed_frame = True
        elif self.facing == Directions.RIGHT:
            self.y_frame = 0
        elif self.facing == Directions.UP:
            self.y_frame = 1
        elif self.facing == Directions.DOWN:
            self.y_frame = 2
    
    def animate(self):
        self.time -= 1
        if self.time <= 0:
            self.time = self.next_frame_ticks_cd
            self.next_frame()
    