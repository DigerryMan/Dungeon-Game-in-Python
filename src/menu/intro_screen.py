import math

import pygame

from config import FPS


class IntroScreen:
    def __init__(self, menu):
        self.menu = menu
        self.game = menu.game
        self.last_change_time = pygame.time.get_ticks()
        self.current_image = 1
        self.main_title = pygame.transform.scale(
            self.menu.main_title,
            (
                self.menu.main_title.get_width() * 1.5,
                self.menu.main_title.get_height() * 1.5,
            ),
        )
        self.main_title_position = (
            self.game.settings.WIN_WIDTH // 2 - self.main_title.get_width() // 2,
            self.game.settings.WIN_HEIGHT // 2 - self.main_title.get_height(),
        )

        self.start_time = pygame.time.get_ticks()

    def display(self):
        self.game.sound_manager.play_with_fadein("intro", 2000, looped=True)
        spotlightcry1 = self.game.image_loader.images_dict["spotlightcry1"]
        spotlightcry2 = self.game.image_loader.images_dict["spotlightcry2"]
        spotlightcry_pos = (
            self.game.settings.WIN_WIDTH // 2 - spotlightcry1.get_width() // 2,
            self.game.settings.WIN_HEIGHT // 2 - spotlightcry1.get_height() // 2,
        )
        overlay = self.game.image_loader.images_dict["introoverlay"]

        while self.game.intro_playing:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game.intro_playing = False
                    self.game.running = False

                if event.type == pygame.MOUSEBUTTONDOWN or (
                    event.type == pygame.KEYDOWN
                    and (event.key == pygame.K_SPACE or event.key == pygame.K_RETURN)
                ):
                    self.game.sound_manager.stop_with_fadeout("intro", 2000)
                    self.game.intro_playing = False
                    self.game.menu_playing = True

            current_time = pygame.time.get_ticks()
            if current_time - self.last_change_time >= 200:
                self.current_image = 2 if self.current_image == 1 else 1
                self.last_change_time = current_time

            self.game.screen.blit(self.menu.intro_background, (0, 0))

            if self.current_image == 1:
                self.game.screen.blit(spotlightcry1, spotlightcry_pos)
            else:
                self.game.screen.blit(spotlightcry2, spotlightcry_pos)

            self.display_tilted_main_title_enlarged()
            self.game.screen.blit(overlay, (0, 0))

            self.game.clock.tick(FPS)
            pygame.display.update()

    def display_tilted_main_title_enlarged(self):
        time_passed = pygame.time.get_ticks() - self.start_time
        tilt_angle = math.sin(time_passed / 500) * 1

        tilted_enlarged_main_title = pygame.transform.rotate(
            self.main_title, tilt_angle
        )

        new_x = (
            self.main_title_position[0]
            - (tilted_enlarged_main_title.get_width() - self.main_title.get_width()) / 2
        )
        new_y = (
            self.main_title_position[1]
            - (tilted_enlarged_main_title.get_height() - self.main_title.get_height())
            / 2
        )
        tilted_enlarged_main_title_position = (new_x, new_y)

        self.game.screen.blit(
            tilted_enlarged_main_title, tilted_enlarged_main_title_position
        )
