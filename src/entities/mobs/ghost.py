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

        self.images = []
        self.img = game.image_loader.mobs["ghost"]
        self.__prepare_images()
        self.image = self.images[0]
        self.unchanged_image = self.image.copy()

        #HITBOX
        self.rect = self.images[0].get_rect()
        self.rect.x = x * game.settings.TILE_SIZE
        self.rect.y = y * game.settings.TILE_SIZE
        self._layer = self.rect.bottom

        self.which_frame = 0
        self.facing = Directions.DOWN
        self.frame_direction_offset = 0
        
        #HITBOX
        self.mask = pygame.mask.from_surface(self.image)

    def __prepare_images(self):
        for y in range(3):
            for x in range(4):
                img_help = self.img.subsurface(pygame.Rect(x * 48, y * 48, 48, 48))
                self.images.append(pygame.transform.scale(img_help, (self.MOB_SIZE, self.MOB_SIZE)))
    
    def animate_alive(self):
        self.time -= 1
        if self.time <= 0:
            self.time = self.next_frame_ticks_cd 
            self.which_frame += 1
            self.which_frame %= 4
            self.next_frame()

    def next_frame(self):
        self.is_change_of_frame = True
        if self.facing == Directions.LEFT:
            self.frame_direction_offset = 8
            self.image = pygame.transform.flip(self.images[self.which_frame + self.frame_direction_offset], True, False)
        elif self.facing == Directions.RIGHT:
            self.frame_direction_offset = 8
            self.image = self.images[self.which_frame + self.frame_direction_offset] 
        elif self.facing == Directions.DOWN:
            self.frame_direction_offset = 0
            self.image = self.images[self.which_frame + self.frame_direction_offset]
        else:
            self.frame_direction_offset = 4
            self.image = self.images[self.which_frame + self.frame_direction_offset]   
        
        self.unchanged_image = self.image.copy()
            
    def correct_layer(self):
        self._layer = 3000
