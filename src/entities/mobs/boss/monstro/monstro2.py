from config import FPS
from entities.mobs.boss.boss_health_bar import BossHealthBar
from entities.mobs.boss.monstro.monstro import Monstro
from entities.mobs.boss.monstro.monstro_animation import MonstroAnimation

class Monstro2(Monstro):
    def __init__(self, game, x: int, y: int):
        super().__init__(game, x, y)
        #STATS
        self._max_health = 45
        self._health = self._max_health
        self._damage = 1.25
        self._projectal_speed = 11
        self.health_bar = BossHealthBar(game, self)

        #ANIMATION
        self.animation = MonstroAnimation(self, game, "monstro2")

        # BOSS STAGES
        self.stage = 1

        self.is_doing_bullet_attack = False
        self.bullet_direction = None
        self.bullet_shooting_cd = 0.5 * FPS
        self.bullet_shooting_time_left = self.bullet_shooting_cd 

        self.jump_cd_s = 0.75
        self.jump_cd = self.jump_cd_s * FPS

        self.max_number_of_jumps = 2
        self.number_of_jumps = 0
        self.stage_1_time = None