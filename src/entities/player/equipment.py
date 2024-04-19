import pygame
import config


class Equipment():
    def __init__(self, player):
        self.health = 0                  #[0-9]      +300%
        self.dmg_reduction = 0           #[0-0.6]    -60%
        self.dmg = 0                     #[0-2]      +200%
        self.speed = 0                   #[0-3]      +37.5%
        self.extra_immortality = 0       #[0-1.25]   +125%
        self.shooting_cd_decrease = 0.0  #[0-0.3]    -50%
        self.shot_speed = 10             #[0-10]     +50%
        self.items = []

        self.player = player
        self.image = pygame.image.load("resources/other/eq-background.png")
        self.width, self.height = self.image.get_size()
        self.x = (player.game.settings.WIN_WIDTH - self.width) // 2
        self.y = (player.game.settings.WIN_HEIGHT - self.height) // 2

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
    
    def pick_up_item(self, item):
        self.items.append(item)
    
    def drop_item(self, item):
        self.items.remove(item)