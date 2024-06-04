import pygame

from config import BLOCK_LAYER
from utils.directions import Directions


class Door(pygame.sprite.Sprite):
    types = {
        "boss_door": {"name": "boss_door", "frames": 11},
        "shop_door": {"name": "shop_door", "frames": 12},
        "wood_door": {"name": "wood_door", "frames": 19},
        "dark_door": {"name": "dark_door", "frames": 13},
        "red_door": {"name": "red_door", "frames": 13},
    }

    def __init__(self, game, x, y, direction: Directions, level, door_type: str = None):
        self.is_open = False
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.doors, self.game.collidables
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.direction = direction

        self.x = x * game.settings.TILE_SIZE
        self.y = y * game.settings.TILE_SIZE

        self.door_type = self.select_doortype_based_on_level_and_doortype(
            level, door_type
        )

        self.animation_frames = Door.types[self.door_type]["frames"]
        self.images = [
            game.image_loader.doors[f"{Door.types[self.door_type]['name']}_{i}"].copy()
            for i in range(self.animation_frames)
        ]
        self.image = self.images[0]
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.width = self.rect.width
        self.height = self.rect.height

        if direction == Directions.UP:
            x_offset = (self.rect.width - self.game.settings.TILE_SIZE) // 2
            self.rect.x -= x_offset
            self.x = self.rect.x
            mask = pygame.Surface(
                (self.rect.width, self.rect.height - self.rect.height // 2.25)
            )
            self.mask = pygame.mask.from_surface(mask)

        elif direction == Directions.DOWN:
            for i in range(self.animation_frames):
                self.images[i] = pygame.transform.rotate(self.images[i], 180)

            x_offset = (self.rect.width - self.game.settings.TILE_SIZE) // 2
            self.rect.x -= x_offset
            self.x = self.rect.x
            removed_hitbox = self.rect.copy()
            removed_hitbox = pygame.Surface(
                (removed_hitbox.width, removed_hitbox.height // 5)
            )
            mask = pygame.mask.from_surface(removed_hitbox)
            self.mask.erase(mask, (0, 0))

        elif direction == Directions.LEFT:
            for i in range(self.animation_frames):
                self.images[i] = pygame.transform.rotate(self.images[i], 90)

            mask = pygame.Surface(
                (self.rect.width - self.rect.width // 2.5, self.rect.height)
            )
            self.mask = pygame.mask.from_surface(mask)

        elif direction == Directions.RIGHT:
            for i in range(self.animation_frames):
                self.images[i] = pygame.transform.rotate(self.images[i], -90)

            self.rect.x -= self.rect.width * 0.2
            removed_hitbox = self.rect.copy()
            removed_hitbox = pygame.Surface(
                (removed_hitbox.width // 2.5, removed_hitbox.height)
            )
            mask = pygame.mask.from_surface(removed_hitbox)
            self.mask.erase(mask, (0, 0))

        self.image = self.images[0]

        self.time_per_frame = 1
        self.timer = 0
        self.current_frame = 0
        self.reverse_animation = False

    def update(self):
        if self.is_open:
            self.collide()

        if self.timer > 0:
            self.timer -= 1
            if self.timer % self.time_per_frame == 0:
                self.next_frame()

    def next_frame(self):
        if not self.reverse_animation:
            self.current_frame += 1

        else:
            self.current_frame -= 1

        self.image = self.images[self.current_frame]

    def animate_closing(self):
        self.timer = self.time_per_frame * (self.animation_frames - 1)
        self.current_frame = self.animation_frames - 1
        self.reverse_animation = True
        self.game.sound_manager.play_if_not_playing("doorClose")

    def animate_opening(self):
        self.timer = self.time_per_frame * (self.animation_frames - 1)
        self.current_frame = 0
        self.reverse_animation = False
        self.game.sound_manager.play_if_not_playing("doorOpen")

    def collide(self):
        hits = pygame.sprite.spritecollide(self, self.game.player_sprite, False)
        if hits:
            mask_hits = pygame.sprite.spritecollide(
                self, self.game.player_sprite, False, pygame.sprite.collide_mask
            )
            if mask_hits:
                self.game.render_next_room(self.direction)

    def open(self):
        self.is_open = True
        self.animate_opening()

    def select_doortype_based_on_level_and_doortype(self, level, door_type):
        if door_type is not None:
            return door_type

        match level:
            case 1 | 2 | 3 | 4:
                return "wood_door"
            case 5 | 6:
                return "dark_door"
            case 7:
                return "red_door"
            case _:
                return "wood_door"
