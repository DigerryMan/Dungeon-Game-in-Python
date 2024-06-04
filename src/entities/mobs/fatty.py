import pygame

from entities.mobs.wanderer import Wanderer
from utils.directions import Directions


class Fatty(Wanderer):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self._health = 10
        self._damage = 0.5
        self._speed = 2 * game.settings.SCALE
        self._collision_damage = 1
        self.size = "Large"

        self.img = game.image_loader.mobs["fatty"]

        self.images_legs = []
        self.images_head = []
        self.__prepare_images()

        self.legs_frame = len(self.images_legs) - 1
        self.head_frame = 0
        self.reversed_frame = False
        self.next_frame_ticks_cd = 4
        self.next_head_frame_cd = 14
        self.next_frame()

    def __prepare_images(self):
        x_offset, y_offset = 11, 45
        y = 2

        w, h = 41, 41
        for x in range(8):
            img = self.img.subsurface(
                pygame.Rect(x * 64 + x_offset, y * 64 + y_offset, w, h)
            )
            self.images_legs.append(
                pygame.transform.scale(img, (self.MOB_SIZE, self.MOB_SIZE))
            )
        y = 3
        for x in range(4):
            img = self.img.subsurface(
                pygame.Rect(x * 64 + x_offset, y * 64 + y_offset, w, h)
            )
            self.images_legs.append(
                pygame.transform.scale(img, (self.MOB_SIZE, self.MOB_SIZE))
            )
        y = 0
        for x in range(8):
            img = self.img.subsurface(
                pygame.Rect(x * 64 + x_offset, y * 64 + y_offset, w, h)
            )
            self.images_legs.append(
                pygame.transform.scale(img, (self.MOB_SIZE, self.MOB_SIZE))
            )
        y = 1
        for x in range(4):
            img = self.img.subsurface(
                pygame.Rect(x * 64 + x_offset, y * 64 + y_offset, w, h)
            )
            self.images_legs.append(
                pygame.transform.scale(img, (self.MOB_SIZE, self.MOB_SIZE))
            )

        for x in range(6):
            img = self.img.subsurface(pygame.Rect(x * 32, 0, 32, 28))
            self.images_head.append(
                pygame.transform.scale(
                    img, (int(self.MOB_SIZE * 0.8), int(0.8 * self.MOB_SIZE))
                )
            )

    def next_frame(self):
        legs_frame = self.set_up_legs_frame()
        self.set_up_head_frame()

        self.frame = pygame.Surface(
            (self.MOB_SIZE, self.MOB_SIZE * 1.1), pygame.SRCALPHA
        )
        head_frame = self.images_head[self.head_frame]
        body_frame = self.images_legs[legs_frame]
        if self.reversed_frame:
            body_frame = pygame.transform.flip(body_frame, True, False)

        x_body = (self.MOB_SIZE - body_frame.get_width()) // 2
        self.frame.blit(body_frame, (x_body, self.MOB_SIZE * 0.2))
        x_head = (self.MOB_SIZE - head_frame.get_width()) // 2
        self.frame.blit(head_frame, (x_head, -4))

        self.image = self.frame
        self.unchanged_image = self.image.copy()

    def set_up_legs_frame(self):
        curr_frame = self.legs_frame
        if self._is_wandering and self._is_idling:
            return 11

        if self.facing == Directions.LEFT or self.facing == Directions.RIGHT:
            self.is_change_of_frame = True
            curr_frame += 12
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
