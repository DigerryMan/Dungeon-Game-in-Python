from .enemy import *

class Mob1(Enemy):
    def __init__(self, game, x, y):
        super().__init__(game, x, y, False)
        self._speed = 16
        self._health = 5
        self.image.fill(PURPLE)
    
    def move(self):
        self.wall_collision()
        if self.facing == 'left':
            self.x_change -= self._speed

        if self.facing == 'right':
            self.x_change += self._speed
         

    def wall_collision(self):
        hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
        if(hits):
            if self.facing == 'left':
                self.facing = 'right'
            elif self.facing == 'right':
                self.facing = 'left'
