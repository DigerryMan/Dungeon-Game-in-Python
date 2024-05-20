import pygame
from config import FPS
from menu.character_selection_screen import CharacterSelectionScreen
from menu.intro_screen import IntroScreen
from menu.pause_screen import PauseScreen
from menu.settings_screen import SettingsScreen

class Menu():
    def __init__(self, game):
        self.game = game
        self.update_images()

        self.intro_screen = IntroScreen(self)
        self.character_selection_screen = CharacterSelectionScreen(self)
        self.settings_screen = SettingsScreen(self)
        self.pause_screen = PauseScreen(self)

    def update_images(self):
        self.intro_background = self.game.image_loader.get_image("introbackground")
        self.menu_card = self.game.image_loader.get_image("menucard")
        self.settings_card = self.game.image_loader.get_image("settingscard")
        self.resolution_settings_card = self.game.image_loader.get_image("resolutionsettingscard")
        self.sound_settings_card = self.game.image_loader.get_image("soundsettingscard")
        self.character_selection = self.game.image_loader.get_image("character_selection")
        self.menu_background = self.game.image_loader.get_image("menuoverlay")
        self.pause_card = self.game.image_loader.get_image("pausecard")
        self.arrow = self.game.image_loader.get_image("arrow")
        self.main_title = self.game.image_loader.get_image("maintitle")

    def display_main_menu(self):
        self.game.sound_manager.play_with_fadein("menuMusic", 2000, looped=True)
        arrow_positions = [(self.game.settings.WIN_WIDTH//2.35, self.game.settings.WIN_HEIGHT//3.13), 
                           (self.game.settings.WIN_WIDTH//2.44, self.game.settings.WIN_HEIGHT//2.15), 
                           (self.game.settings.WIN_WIDTH//2.27, self.game.settings.WIN_HEIGHT//1.67)]
        current_arrow = 0

        while self.game.menu_playing:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game.menu_playing = False
                    self.game.running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        current_arrow = current_arrow + 1 if current_arrow < 2 else 0
                        self.game.sound_manager.play("selectLeft")

                    if event.key == pygame.K_UP:
                        current_arrow = current_arrow - 1 if current_arrow > 0 else 2
                        self.game.sound_manager.play("selectRight")

                    if event.key == pygame.K_RETURN:
                        if current_arrow == 0:
                            self.game.sound_manager.play("pageTurn")
                            self.game.menu_playing = False
                            self.display_character_selection()
                            self.game.paused = False

                        elif current_arrow == 1:
                            self.game.sound_manager.play("pageTurn")
                            self.game.menu_playing = False
                            self.display_settings()
                            arrow_positions = [(self.game.settings.WIN_WIDTH//2.35, self.game.settings.WIN_HEIGHT//3.13), 
                                            (self.game.settings.WIN_WIDTH//2.44, self.game.settings.WIN_HEIGHT//2.15), 
                                            (self.game.settings.WIN_WIDTH//2.27, self.game.settings.WIN_HEIGHT//1.67)]
                            
                        elif current_arrow == 2:
                            self.game.menu_playing = False
                            self.game.running = False

                        if not self.game.menu_playing:
                            self.game.sound_manager.stop_with_fadeout("menuMusic", 2000)
                            return

            self.game.screen.blit(self.menu_card, (0, 0))
            self.game.screen.blit(self.menu_background, (0, 0))
            self.game.screen.blit(self.main_title, (self.game.settings.WIN_WIDTH//8, 0))

            self.game.screen.blit(self.arrow, (arrow_positions[current_arrow][0], arrow_positions[current_arrow][1]))

            self.game.clock.tick(FPS)
            pygame.display.update()

    def display_intro_screen(self):
        self.intro_screen.display()

    def display_character_selection(self):
        self.character_selection_screen.display()

    def display_settings(self):
        self.settings_screen.display()

    def display_pause(self):
        self.pause_screen.display()