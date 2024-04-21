from items.stat_items.categories import Categories
from utils.image_loader import ImageLoader
import pygame
import random

class ItemsList():
    def __init__(self, game):
        self.game = game

        self.commons = {}
        self.epics = {}
        self.legendaries ={}

        self.commons["heart"] = {
            "name": "Heart",
            "category": Categories.COMMON,
            "stats": {
                "health": 1
            },
            "image": pygame.transform.scale(game.image_loader.get_image("items").subsurface(pygame.Rect(3 * 32, 2 * 32, 32, 32)), (game.settings.TILE_SIZE, game.settings.TILE_SIZE))
        }

        self.commons["armor"] = {
            "name": "Armor",
            "category": Categories.COMMON,
            "stats": {
                "dmg_reduction": 0.1
            },
            "image": pygame.transform.scale(game.image_loader.get_image("items").subsurface(pygame.Rect(3 * 32, 21 * 32, 32, 32)), (game.settings.TILE_SIZE, game.settings.TILE_SIZE))
        }

        self.commons["small_sword"] = {
            "name": "Small sword",
            "category": Categories.COMMON,
            "stats": {
                "dmg": 0.2
            },
            "image": pygame.transform.scale(game.image_loader.get_image("items").subsurface(pygame.Rect(15 * 32, 19 * 32, 32, 32)), (game.settings.TILE_SIZE, game.settings.TILE_SIZE))
        }

        self.commons["glasses"] = {
            "name": "Glasses",
            "category": Categories.COMMON,
            "stats": {
                "bullet_fly_time": 0.2
            },
            "image": pygame.transform.scale(game.image_loader.get_image("items").subsurface(pygame.Rect(12 * 32, 3 * 32, 32, 32)), (game.settings.TILE_SIZE, game.settings.TILE_SIZE))
        }

        self.commons["green_syringe"] = {
            "name": "Green syringe",
            "category": Categories.COMMON,
            "stats": {
                "shot_speed": 2
            },
            "image": pygame.transform.scale(game.image_loader.get_image("items").subsurface(pygame.Rect(13 * 32, 0 * 32, 32, 32)), (game.settings.TILE_SIZE, game.settings.TILE_SIZE))
        }





        self.epics["angel"] = {
            "name": "Angel",
            "category": Categories.EPIC,
            "stats": {
                "immortality_after_hit": 0.5
            },
            "image": pygame.transform.scale(game.image_loader.get_image("items").subsurface(pygame.Rect(5 * 32, 19 * 32, 32, 32)), (game.settings.TILE_SIZE, game.settings.TILE_SIZE))
        }

        self.epics["big_sword"] = {
            "name": "Big sword",
            "category": Categories.EPIC,
            "stats": {
                "dmg": 0.5
            },
            "image": pygame.transform.scale(game.image_loader.get_image("items").subsurface(pygame.Rect(26 * 32, 13 * 32, 32, 32)), (game.settings.TILE_SIZE, game.settings.TILE_SIZE))
        }

        self.epics["holy_cross"] = {
            "name": "Holy cross",
            "category": Categories.EPIC,
            "stats": {
                "luck": 0.1
            },
            "image": pygame.transform.scale(game.image_loader.get_image("items").subsurface(pygame.Rect(36 * 32, 6 * 32, 32, 32)), (game.settings.TILE_SIZE, game.settings.TILE_SIZE))
        }
    


    def get_random_item(self, category):
        if category == Categories.COMMON:
            return random.choice(list(self.commons.values()))
        elif category == Categories.EPIC:
            return random.choice(list(self.epics.values()))
        elif category == Categories.LEGENDARY:
            return random.choice(list(self.legendaries.values()))
        else:
            return None