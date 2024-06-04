import random

import pygame

from config import FPS
from utils.directions import Directions


class EnemyMoves:
    def __init__(self, enemy, game):
        self.game = game
        self.enemy = enemy

        self._wander_interval = [int(0.7 * FPS), int(1.7 * FPS)]
        self._idle_interval = [int(1.2 * FPS), int(2.5 * FPS)]

        self._wander_time = self.roll_interval(self._wander_interval)
        self._wander_time_left = self._wander_time

        self._idle_time = self.roll_interval(self._idle_interval)
        self._idle_time_left = self._idle_time

    def wander(self):
        if self.enemy._is_idling:
            if not self.enemy.check_group_attacked():
                self.idle()
            else:
                self.enemy._is_idling = False
                self.enemy._is_wandering = False
        else:
            self._wander_time_left -= 1
            if self._wander_time_left <= 0:
                self.enemy._is_idling = True
                self._wander_time = self.roll_interval(self._wander_interval)
                self._wander_time_left = self._wander_time
            else:
                if self.enemy.facing == Directions.LEFT:
                    self.enemy.x_change = -self.enemy._speed // 2
                elif self.enemy.facing == Directions.RIGHT:
                    self.enemy.x_change = self.enemy._speed // 2
                    self.correct_low_speed_enemies("x")
                elif self.enemy.facing == Directions.UP:
                    self.enemy.y_change = -self.enemy._speed // 2
                elif self.enemy.facing == Directions.DOWN:
                    self.enemy.y_change = self.enemy._speed // 2
                    self.correct_low_speed_enemies("y")

    def idle(self):
        self._idle_time_left -= 1
        if self._idle_time_left <= 0:
            self.enemy._is_idling = False
            self.roll_facing()
            self._idle_time = self.roll_interval(self._idle_interval)
            self._idle_time_left = self._idle_time

    def roll_facing(self):
        rand = random.choice(
            [
                self.enemy.facing.rotate_clockwise(),
                self.enemy.facing.reverse(),
                self.enemy.facing.rotate_counter_clockwise(),
                self.enemy.facing,
            ]
        )
        self.enemy.facing = rand

    def move(self):
        if self.enemy._is_wandering:
            self.wander()
        else:
            self.move_because_of_player()

    def move_because_of_player(self, chase: bool = True):
        player_vector = pygame.math.Vector2(self.game.get_player_rect().center)
        enemy_vector = pygame.math.Vector2(self.enemy.rect.center)
        distance = (player_vector - enemy_vector).magnitude()
        if distance > 3:
            direction = None
            if distance > 0:
                direction = (player_vector - enemy_vector).normalize()
            else:
                direction = pygame.math.Vector2()

            speed = self.enemy._speed
            if not chase:
                direction.rotate_ip(180)
                speed = self.enemy._speed * self.enemy._chase_speed_debuff

            velocity = direction * speed
            self.enemy.x_change = velocity.x
            self.enemy.y_change = velocity.y
            self.enemy._correct_rounding()
            self.correct_facing()

    def correct_facing(self):
        y_abs = abs(self.enemy.y_change)
        x_abs = abs(self.enemy.x_change)

        if x_abs >= y_abs:
            if self.enemy.x_change < 0:
                self.enemy.facing = Directions.LEFT
            elif self.enemy.x_change > 0:
                self.enemy.facing = Directions.RIGHT
        else:
            if self.enemy.y_change < 0:
                self.enemy.facing = Directions.UP
            elif self.enemy.y_change > 0:
                self.enemy.facing = Directions.DOWN

    def correct_low_speed_enemies(self, axis: str):
        if self.enemy._speed // 2 == 0:
            if axis == "x":
                self.enemy.x_change = self.enemy._speed
            if axis == "y":
                self.enemy.y_change = self.enemy._speed

    def roll_interval(self, interval):
        return random.randint(interval[0], interval[1])
