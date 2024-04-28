from config import *
from entities.enemy import Enemy
import pygame

from utils.directions import Directions

class Ghost(Enemy):
    def __init__(self, game, x: int, y: int):
        super().__init__(game, x, y, check_block_colisions=False, 
                         is_wandering=False, bullet_decay_sec=3)
        
        #CHANGEABLE STATS
        self._health = 6
        self._speed = 3 * game.settings.SCALE
        self._projectal_speed = 7
        
        #ANIMATION
        self.next_frame_ticks_cd = 10
        self.time = 0

        self.MOB_SIZE = game.settings.MOB_SIZE
        self.img = game.image_loader.get_image("ghost")
        self.images = []
        self.frame = None

        self.which_frame = 0
        self.last_rigth_left_facing = Directions.RIGHT
    
        self.__prepare_images()
        self.image = self.images[0]

        #HITBOX
        self.mask = pygame.mask.from_surface(self.image)

    def __prepare_images(self):
        for x in range(6):
            self.images.append(self.img.subsurface(pygame.Rect(x * self.MOB_SIZE, 0, self.MOB_SIZE, self.MOB_SIZE)))

    def animate(self):
        self.time -= 1
        if self.time <= 0:
            self.time = self.next_frame_ticks_cd 
            self.which_frame += 1
            self.which_frame %= 6

            self.next_frame()

    def next_frame(self):
        if self.facing == Directions.LEFT or self.facing == Directions.RIGHT:
            self.last_rigth_left_facing = self.facing
         
        if self.last_rigth_left_facing == Directions.LEFT:
            self.image = pygame.transform.flip(self.images[self.which_frame], True, False)
        else:
            self.image = self.images[self.which_frame]    

    def correct_layer(self):
        self._layer = 3000
