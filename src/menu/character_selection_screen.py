import pygame

from config import FPS
from entities.player.player_types import PlayerTypes


class CharacterSelectionScreen:
    def __init__(self, menu):
        self.menu = menu
        self.game = menu.game

    def display(self):
        character_selection_playing = True
        characters = PlayerTypes.get_all_characters()
        current_character = 0

        image, name, stats = None, None, None

        def set_character_display():
            nonlocal image, name, stats
            image = self.game.image_loader.images_dict[
                characters[current_character].value + "_display"
            ]["image"]
            name = self.game.image_loader.images_dict[
                characters[current_character].value + "_display"
            ]["name"]
            stats = self.game.image_loader.images_dict[
                characters[current_character].value + "_display"
            ]["stats"]

        set_character_display()

        while character_selection_playing:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    character_selection_playing = False
                    self.game.menu_playing = False
                    self.game.running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        self.game.sound_manager.play("selectRight")
                        current_character = (current_character + 1) % len(characters)
                        set_character_display()

                    if event.key == pygame.K_LEFT:
                        self.game.sound_manager.play("selectLeft")
                        current_character = (current_character - 1) % len(characters)
                        set_character_display()

                    if event.key == pygame.K_RETURN:
                        self.game.sound_manager.play("pageTurn")
                        character_selection_playing = False
                        self.game.character_type = characters[current_character]
                        self.game.render_new_map(first_map=True)
                        self.game.sound_manager.play_with_fadein(
                            "basementLoop", 4000, looped=True
                        )

                    if event.key == pygame.K_ESCAPE:
                        self.game.sound_manager.play("pageTurn")
                        character_selection_playing = False
                        self.game.menu_playing = True

            self.game.screen.blit(self.menu.character_selection, (0, 0))
            self.game.screen.blit(
                image,
                (
                    self.game.settings.WIN_WIDTH // 2.25,
                    self.game.settings.WIN_HEIGHT // 2.5,
                ),
            )
            self.game.screen.blit(
                name,
                (
                    self.game.settings.WIN_WIDTH // 2.25,
                    self.game.settings.WIN_HEIGHT // 1.8,
                ),
            )
            self.game.screen.blit(
                stats,
                (
                    self.game.settings.WIN_WIDTH // 2.5,
                    self.game.settings.WIN_HEIGHT // 1.5,
                ),
            )
            self.game.screen.blit(self.menu.menu_background, (0, 0))
            self.game.screen.blit(
                self.menu.main_title, (self.game.settings.WIN_WIDTH // 8, 0)
            )

            self.game.clock.tick(FPS)
            pygame.display.update()
