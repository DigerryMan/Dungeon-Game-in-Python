import pygame

from entities.bullet import Bullet
from entities.mobs.ghost import Ghost
from utils.directions import Directions


class FriendlyGhost(Ghost):
    def __init__(self, game, x, y, reversed_moves=False):
        super().__init__(game, x, y)
        self._damage = 1
        self._speed = 3 * game.settings.SCALE
        self._projectal_speed = 10
        self._reversed_moves = reversed_moves
        self._shot_time_left = self._shot_cd

        # ANIMATION
        self.img = game.image_loader.mobs["friendly_ghost"]
        self.__prepare_images()
        self.image = self.images[0]

        self.next_frame_ticks_cd = 10
        self.time = 0
        self.which_frame = 0
        self.is_moving = False

        self.shot_animation_cd = 10
        self.shot_animation_left = 0

        # HITBOX
        self.mask = pygame.mask.from_surface(self.image)

        # REST
        self.groups = game.all_sprites, game.entities
        self.remove(game.enemies)

    def __prepare_images(self):
        self.images.clear()
        mob_size = self.MOB_SIZE // 2
        for y in range(3):
            img_help = self.img.subsurface(
                pygame.Rect(0, y * 32, 40, 32)
            )
            self.images.append(
                pygame.transform.scale(img_help, (mob_size, mob_size))
            )

    def attack(self):
        if self.game.enemies:
            self._shot_time_left -= 1
            if self._shot_time_left <= 0:
                self.shot_animation_left = self.shot_animation_cd
                Bullet(
                    self.game,
                    self.rect.centerx,
                    self.rect.centery,
                    Directions.ENEMY,
                    self._projectal_speed,
                    True,
                    self._damage,
                    self._bullet_decay_sec,
                )
                self.roll_next_shot_cd()
                self._shot_time_left = self._shot_cd

    def move(self):
        self.move_because_of_player()

    def move_because_of_player(self, chase: bool = True):
        self.is_moving = False
        player_horizontal_facing = self.game.player.last_horizontall_facing
        player_rect = self.game.get_player_rect()
        enemy_vector = pygame.math.Vector2(self.rect.center)
        player_vector = None

        left = player_rect.left + self.game.settings.PLAYER_SIZE // 2
        right = player_rect.right
        if self._reversed_moves:
            left, right = right, left

        if player_horizontal_facing == Directions.LEFT:
            player_vector = pygame.math.Vector2(left, player_rect.top)
        else:
            player_vector = pygame.math.Vector2(right, player_rect.top)

        distance = (player_vector - enemy_vector).magnitude()
        if distance > 3:
            self.is_moving = True
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
        pass

    def animate_alive(self):
        self.time -= 1
        if self.time <= 0:
            self.time = self.next_frame_ticks_cd
            self.which_frame += 1
            self.which_frame %= 2
        
        if self.shot_animation_left > 0:
            self.shot_animation_left -= 1
            self.which_frame = 2

        self.next_frame()

    def next_frame(self):  
        self.image = self.images[self.which_frame]
