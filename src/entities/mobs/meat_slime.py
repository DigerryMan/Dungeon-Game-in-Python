import pygame
from entities.bullet import Bullet
from entities.mobs.slime import Slime
from utils.directions import Directions

class MeatSlime(Slime):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)

        self._health = 3
        self._projectal_speed = int(7 * game.settings.SCALE)
        self._bullet_decay_sec = 1.8

        # SKINS
        self.img = game.image_loader.get_image("meat_slime")
        self.images.clear()
        self.prepare_images()
        self.image = self.images[0]
        self.unchanged_image = self.image.copy()
        self.mask = pygame.mask.from_surface(self.image)
    
    def attack(self):
        if self.prepare_atack:
            self.prepare_atack = False
            self.shoot_diagonally()
            self.shoot_straight()
            
    
    def shoot_diagonally(self):
        direction_to_shoot = Directions.LEFT
        multiplier = -1
        diagonal_speed = int(self._projectal_speed * 0.8)
        for _ in range(4):
            if direction_to_shoot == Directions.LEFT or direction_to_shoot == Directions.DOWN:
                multiplier = -1
            else: multiplier = 1
            Bullet(
                self.game,
                self.rect.centerx,
                self.rect.centery,
                direction_to_shoot,
                speed=diagonal_speed,
                is_friendly=False,
                dmg=1,
                time_decay_in_seconds=self._bullet_decay_sec,
                additional_speed=diagonal_speed * multiplier
            )
            direction_to_shoot = direction_to_shoot.rotate_clockwise()
    
    def shoot_straight(self):
        direction_to_shoot = Directions.LEFT
        for _ in range(4):
            Bullet(
                self.game,
                self.rect.centerx,
                self.rect.centery,
                direction_to_shoot,
                speed=self._projectal_speed,
                is_friendly=False,
                dmg=1,
                time_decay_in_seconds=self._bullet_decay_sec,
            )
            direction_to_shoot = direction_to_shoot.rotate_clockwise()