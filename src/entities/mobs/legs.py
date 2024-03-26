from ..enemy import *

class Mob1(Enemy):
    def __init__(self, game, x, y):
        super().__init__(game, x, y, False)
        self._speed = 16
        self._health = 5
        self.image.fill(PURPLE)
    
    def move(self):
        self.wall_collision()
        if self.facing == Directions.LEFT:
            self.x_change -= self._speed

        if self.facing == Directions.RIGHT:
            self.x_change += self._speed
         
    def attack(self):
        now = pygame.time.get_ticks()
        if now - self._last_attack > self._attack_speed:
            self._last_attack = now
            Bullet(self.game, self.rect.centerx, self.rect.centery, Directions.LEFT, 12, False, self._damage)
            Bullet(self.game, self.rect.centerx, self.rect.centery, Directions.RIGHT, 12, False, self._damage)

    def wall_collision(self):
        hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
        if(hits):
            self.facing = self.facing.reverse()
