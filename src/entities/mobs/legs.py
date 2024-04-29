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
        self.images = []
        self.frame = None

        self.which_frame = 0
        self.reversed_frame = False
    
        self.prepare_images()
        self.image = self.images[0]

        #HITBOX
        self.mask = pygame.mask.from_surface(self.image)

    def prepare_images(self):
        for y in range(6):
            for x in range(4):
                self.images.append(self.img.subsurface(pygame.Rect(x * self.MOB_SIZE, y * self.MOB_SIZE, self.MOB_SIZE, self.MOB_SIZE)))
               
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
        curr_frame = self.which_frame # if up/down

        if self.facing == Directions.LEFT or self.facing == Directions.RIGHT:
            curr_frame += 10
            if self.facing == Directions.LEFT:
                self.reversed_frame = True
         
        if self.reversed_frame:
            self.image = pygame.transform.flip(self.images[curr_frame], True, False)
        else:
            self.image = self.images[curr_frame]
    