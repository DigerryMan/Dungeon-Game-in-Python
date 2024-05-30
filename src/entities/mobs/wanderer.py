import pygame
from entities.enemy import Enemy
from utils.directions import Directions

class Wanderer(Enemy):
    def __init__(self, game, x: int, y: int):
        super().__init__(game, x, y)
        Wanderer.is_group_attacked = False

        self.next_frame_ticks_cd = 3
        self.next_head_frame_cd = 8
        self.time = 0
        self.head_time_left = 0

        self.img_legs = game.image_loader.get_image("legs")
        self.img_head = game.image_loader.get_image("wanderer")
        self.images_legs = []
        self.images_head = []

        self.legs_frame = 0
        self.head_frame = 0
        self.reversed_frame = False
    
        self.prepare_images()
        self.next_frame()

        #HITBOX
        self.mask = pygame.mask.from_surface(self.image)

    def prepare_images(self):
        for y in range(6):
            for x in range(4):
                self.images_legs.append(self.img_legs.subsurface(pygame.Rect(x * self.MOB_SIZE, y * self.MOB_SIZE, self.MOB_SIZE, self.MOB_SIZE)))

        width = self.img_head.get_width() // 6
        for x in range(6):
            img = self.img_head.subsurface(pygame.Rect(x * width, 0, width, width))
            self.images_head.append(pygame.transform.scale(img, (self.MOB_SIZE, self.MOB_SIZE)))

    def animate(self):
        self.reversed_frame = False
        if not self._is_wandering or not self._is_idling:
            self.time -= 1
        else:
            self.image = self.images_legs[0]
            self.unchanged_image = self.image.copy()

        if self.time <= 0:
            self.is_change_of_frame = True
            self.time = self.next_frame_ticks_cd 
            self.legs_frame += 1
            self.legs_frame %= 10

        self.next_frame()

    def next_frame(self):
        legs_frame = self.set_up_legs_frame() 
        self.set_up_head_frame()
        
        self.frame = pygame.Surface((self.MOB_SIZE, self.MOB_SIZE), pygame.SRCALPHA)
        head_frame = self.images_head[self.head_frame]
        body_frame = self.images_legs[legs_frame]
        if self.reversed_frame:
            body_frame = pygame.transform.flip(body_frame, True, False)
        
        self.frame.blit(body_frame, (0, self.MOB_SIZE*0.25))
        self.frame.blit(head_frame, ((self.MOB_SIZE - head_frame.get_width())//2, -3))
        
        self.image = self.frame
        self.unchanged_image = self.image.copy()

    def set_up_legs_frame(self):
        # if up/down
        curr_frame = self.legs_frame
        if self._is_wandering and self._is_idling:
            return 0
        
        if self.facing == Directions.LEFT or self.facing == Directions.RIGHT:
            self.is_change_of_frame = True
            curr_frame += 10
            if self.facing == Directions.LEFT:
                self.reversed_frame = True
        
        return curr_frame
    
    def set_up_head_frame(self):
        self.head_time_left -= 1
        if self.head_time_left <= 0:
            self.is_change_of_frame = True
            self.head_time_left = self.next_head_frame_cd
            self.head_frame += 1
            self.head_frame %= 6

    @staticmethod
    def check_group_attacked():
        return Wanderer.is_group_attacked

    @staticmethod
    def group_attacked():
        Wanderer.is_group_attacked = True