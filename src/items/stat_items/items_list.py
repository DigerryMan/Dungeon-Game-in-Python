from items.stat_items.categories import Categories
from utils.image_loader import ImageLoader
import pygame


class ItemsList():
    def __init__(self, game):
        self.game = game

        self.commons = []
        self.epics = []
        self.legendaries = []

        heart = {
            "name": "Heart",
            "category": Categories.COMMON,
            "stats": {
                "health": 1
            },
            "image": pygame.transform.scale(game.image_loader.get_image("items").subsurface(pygame.Rect(3 * 32, 2 * 32, 32, 32)), (game.settings.TILE_SIZE, game.settings.TILE_SIZE))
        }

        self.commons.append(heart)