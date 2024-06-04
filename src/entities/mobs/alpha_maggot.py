from entities.bullet import Bullet
from entities.mobs.maggot import Maggot
from utils.directions import Directions


class AlphaMaggot(Maggot):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        # CHANGEABLE STATS
        self._health = 8
        self._speed = 4 * game.settings.SCALE
        self._projectal_speed = 3

        # SKIN
        self.img = game.image_loader.get_image("alpha_maggot")
        self.prepare_images()

    def attack(self):
        self._shot_time_left -= 1
        if self._shot_time_left <= 0:
            Bullet(
                self.game,
                self.rect.centerx,
                self.rect.centery,
                Directions.PLAYER,
                self._projectal_speed,
                False,
                time_decay_in_seconds=1.5,
            )
            self.roll_next_shot_cd()
            self._shot_time_left = self._shot_cd

    def prepare_images(self):
        self.images.clear()
        super().prepare_images()
