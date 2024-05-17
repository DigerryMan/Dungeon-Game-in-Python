import pygame
from config import FPS

class PauseScreen():
    def __init__(self, menu):
        self.menu = menu
        self.game = menu.game

    def display(self):
        self.game.sound_manager.play("pageTurn")
        arrow_positions = [(self.game.settings.WIN_WIDTH//3.1, self.game.settings.WIN_HEIGHT//2.05),
                           (self.game.settings.WIN_WIDTH//2.85, self.game.settings.WIN_HEIGHT//1.75)]
        current_arrow = 0

        while self.game.paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game.paused = False
                    self.game.running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.game.sound_manager.play("pageTurn")
                        self.game.paused = False
                    
                    if event.key == pygame.K_DOWN or event.key == pygame.K_UP:
                        current_arrow = current_arrow + 1 if current_arrow == 0 else 0
                        self.game.sound_manager.play("selectRight")

                    if event.key == pygame.K_RETURN:
                        if current_arrow == 0:
                            self.game.paused = False
                            self.game.sound_manager.play("pageTurn")
                        elif current_arrow == 1:
                            self.game.paused = False
                            self.game.menu_playing = True
                            self.game.sound_manager.play("pageTurn")
                            self.game.sound_manager.stop_with_fadeout("basementLoop", 2000)

            self.game.screen.blit(self.menu.pause_card, (self.game.settings.WIN_WIDTH//4, self.game.settings.WIN_HEIGHT//4))
            self.game.screen.blit(self.menu.arrow, (arrow_positions[current_arrow][0], arrow_positions[current_arrow][1]))

            self.game.clock.tick(FPS)
            pygame.display.update()