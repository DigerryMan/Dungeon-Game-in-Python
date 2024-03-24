import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, game, name="Player1"):
        self.__health = 3
        self.__movement_speed = 100
        self.__name = name
        self._layer = 3
        self.x = 0
        self.y = 0
        self.vel = 5
        self.width = 20
        self.height = 20

        self.game = game
        self.groups = self.game.all_sprites

        self.image = pygame.Surface([self.width, self.height])
        self.image.fill((255,0,0))

        self.rect = self.image.get_rect()

        pygame.sprite.Sprite.__init__(self, self.groups)
    
    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.x -= self.vel
        
        if keys[pygame.K_d]:
            self.x += self.vel

        if keys[pygame.K_w]: 
            self.y -= self.vel

        if keys[pygame.K_s]:
            self.y += self.vel

        self.rect.x = self.x
        self.rect.y = self.y

    def draw(self, screen):
        pygame.draw.rect(screen, (0,0,255), (self.x, self.y, self.width, self.height))

    def update(self):
        self.move()