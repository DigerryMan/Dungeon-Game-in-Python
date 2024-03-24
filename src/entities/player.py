import pygame


class Player:
    def __init__(self, name="Player1"):
        self.__health = 3
        self.__movement_speed = 100
        self.__name = name
        self.x = 0
        self.y = 0
        self.vel = 10
        self.width = 20
        self.height = 20
    
    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and self.x > 0 + self.x < 1000 - self.width:
            self.x -= self.vel
        
        if keys[pygame.K_RIGHT] and self.x < 1000 - self.width:
            self.x += self.vel

        if keys[pygame.K_UP] and self.y > 0 + self.height: 
            self.y += self.vel

        if keys[pygame.K_DOWN] and self.y > 1000 - self.height:
            self.y -= self.vel

    def draw(self, screen):
        pygame.draw.rect(screen, (0,0,255), (self.x, self.y, self.width, self.height))