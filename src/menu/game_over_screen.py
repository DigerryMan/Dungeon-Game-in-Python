import pygame
from config import FPS

class GameOverScreen():
    def __init__(self, menu):
        self.menu = menu
        self.game = menu.game

    def display(self):
        self.game.sound_manager.stop_all_with_fadeout(250)
        spotlight = self.game.image_loader.images_dict["spotlight"]
        spotlight_positon = (self.game.settings.WIN_WIDTH//2 - spotlight.get_width()//2, -spotlight.get_height()//4)
        should_display = True
        start_time = pygame.time.get_ticks()

        self.game.sound_manager.play_with_fadein("gameOver", 500)

        if self.game.player.is_alive:
            player_image = self.game.player.animation.win_image
            player_image_position = (self.game.settings.WIN_WIDTH//2 - player_image.get_width()//2, self.game.settings.WIN_HEIGHT//1.65)

        else:
            player_image = self.game.player.animation.intro_image
            player_image_position = (self.game.settings.WIN_WIDTH//2 - player_image.get_width()//2, self.game.settings.WIN_HEIGHT//1.5)

        while should_display:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game.running = False
                    should_display = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE:
                        self.game.menu_playing = True
                        self.game.sound_manager.play("pageTurn")
                        should_display = False

            self.game.screen.fill((0, 0, 0))
            self.game.screen.blit(spotlight, spotlight_positon)
            self.game.screen.blit(player_image, player_image_position)

            elapsed_time = pygame.time.get_ticks() - start_time
            if elapsed_time < 4000:
                alpha = (255 * elapsed_time) // 4000
                fade_surface = pygame.Surface((self.game.settings.WIN_WIDTH, self.game.settings.WIN_HEIGHT))
                fade_surface.fill((0, 0, 0))
                fade_surface.set_alpha(255 - alpha)
                self.game.screen.blit(fade_surface, (0, 0))


            self.game.clock.tick(FPS)
            pygame.display.update()