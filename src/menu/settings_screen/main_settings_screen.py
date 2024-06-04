import pygame

from config import FPS
from menu.settings_screen.audio_settings_screen import AudioSettingsScreen
from menu.settings_screen.resolution_settings_screen import ResolutionSettingsScreen


class MainSettingsScreen:
    def __init__(self, menu):
        self.menu = menu
        self.game = menu.game
        self.settings_playing = True

        self.audio_settings_screen = AudioSettingsScreen(self)
        self.resolution_settings_screen = ResolutionSettingsScreen(self)

    def display(self):
        self.settings_playing = True
        arrow_positions = None

        def get_arrow_positions():
            nonlocal arrow_positions
            arrow_positions = [
                (
                    self.game.settings.WIN_WIDTH // 2.6,
                    self.game.settings.WIN_HEIGHT // 2.8,
                ),
                (
                    self.game.settings.WIN_WIDTH // 2.4,
                    self.game.settings.WIN_HEIGHT // 2.13,
                ),
            ]

        get_arrow_positions()
        current_arrow = 0

        while self.settings_playing:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.settings_playing = False
                    self.game.menu_playing = False
                    self.game.running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        self.game.sound_manager.play("selectLeft")
                        current_arrow = current_arrow + 1 if current_arrow < 1 else 0

                    if event.key == pygame.K_UP:
                        self.game.sound_manager.play("selectRight")
                        current_arrow = current_arrow - 1 if current_arrow > 0 else 1

                    if event.key == pygame.K_RETURN:
                        if current_arrow == 0:
                            self.game.sound_manager.play("pageTurn")
                            self.display_resolution_settings()
                            get_arrow_positions()

                        elif current_arrow == 1:
                            self.game.sound_manager.play("pageTurn")
                            self.display_sound_settings()

                    if event.key == pygame.K_ESCAPE:
                        self.game.sound_manager.play("pageTurn")
                        self.settings_playing = False
                        self.game.menu_playing = True

            self.game.screen.blit(self.menu.settings_card, (0, 0))
            self.game.screen.blit(self.menu.menu_background, (0, 0))
            self.game.screen.blit(
                self.menu.main_title, (self.game.settings.WIN_WIDTH // 8, 0)
            )

            self.game.screen.blit(
                self.menu.arrow,
                (arrow_positions[current_arrow][0], arrow_positions[current_arrow][1]),
            )

            self.game.clock.tick(FPS)
            pygame.display.update()

    def display_resolution_settings(self):
        self.resolution_settings_screen.display()

    def display_sound_settings(self):
        self.audio_settings_screen.display()
