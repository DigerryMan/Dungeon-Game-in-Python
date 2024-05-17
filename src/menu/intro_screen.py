import pygame
from config import FPS

class IntroScreen():
    def __init__(self, menu):
        self.menu = menu
        self.game = menu.game

    def display(self):
        self.game.sound_manager.play_with_fadein("intro", 2000, looped=True)
        while self.game.intro_playing:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game.intro_playing = False
                    self.game.running = False

                if event.type == pygame.MOUSEBUTTONDOWN or (event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE or event.key == pygame.K_RETURN)):
                    self.game.sound_manager.stop_with_fadeout("intro", 2000)
                    self.game.intro_playing = False
                    self.game.menu_playing = True

            self.game.screen.blit(self.menu.intro_background, (0, 0))
            self.game.clock.tick(FPS)
            pygame.display.update()