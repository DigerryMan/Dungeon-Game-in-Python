from ..enemy import *

class Legs(Enemy):
    def __init__(self, game, x, y):
        super().__init__(game, x, y, True, is_wandering=False)
        self._speed = 3 * game.settings.SCALE
        self._health = 5
        
        #ANIMATION
        self.next_frame_ticks_cd = 3
        self.time = 0

        self.MOB_SIZE = game.settings.MOB_SIZE
        self.img = game.image_loader.get_image("legs")
        self.frame = self.img.subsurface(pygame.Rect(0, 0, 32, 32))
        self.frame = pygame.transform.scale(self.frame, (self.MOB_SIZE, self.MOB_SIZE))
        self.image = self.frame

        self.x_frame = 0
        self.y_frame = 0
        self.which_frame = 0
        self.reversed_frame = False

        #HITBOX
        self.mask = pygame.mask.from_surface(self.image)

    def attack(self):
        pass
    
    def animate(self):
        self.reversed_frame = False

        if not self._is_wandering or not self._is_idling:
            self.time -= 1
   
        if self.time <= 0:
            self.time = self.next_frame_ticks_cd 
            self.which_frame += 1
            self.which_frame %= 10

            self.next_frame()

    def next_frame(self):
        y = self.which_frame // 4 #for up down
        x = self.which_frame % 4  #for up down

        if self.facing == Directions.LEFT or self.facing == Directions.RIGHT:
            y = (10 + self.which_frame) // 4
            x = (self.which_frame + 2) % 4
            if self.facing == Directions.LEFT:
                self.reversed_frame = True
            
        self.frame = self.img.subsurface(pygame.Rect(x * 32, y * 32, 32, 32))
        self.frame = pygame.transform.scale(self.frame, (self.MOB_SIZE, self.MOB_SIZE))
        if self.reversed_frame:
            self.frame = pygame.transform.flip(self.frame, True, False)

        self.image = self.frame
    