import pygame
from config import *

class ImageLoader:
    def __init__(self, settings):
        self.settings = settings

        self.menu_ = ["introbackground", "menucard", "settingscard", "menuoverlay", "pausecard2", "arrow2", "maintitle"]
        self.mobs_ = ["alpha_maggot", "fly","legs", "maggot", "parasite", "slime"]
        self.rooms_ = ["basement", "catacombs", "caves", "controls", "depths", "necropolis", "shading", "shop_room", "utero", "womb"]
        self.doors_ = ["angel_door", "boss_door", "devil_door", "door", "red_door"]
        self.blocks_ = ["rocks2"]

        self.images_dict = {}
        self.__load_images_to_dict()

        self.blocks = {}
        self.load_blocks()

        self.tears = {}
        self.load_tears()


    def __load_images_to_dict(self):
        print("Loading images...")
        for menu_element in self.menu_:
            self.images_dict[menu_element] = pygame.image.load("resources/menu/" + menu_element + ".png")

        for mob in self.mobs_:
            self.images_dict[mob] = pygame.image.load("resources/mobs/" + mob + ".png").convert_alpha()

        room_scaled_size = (self.settings.WIN_WIDTH * 1.08, self.settings.WIN_HEIGHT * 1.08)
        for room in self.rooms_:
            self.images_dict[room] = pygame.transform.scale(pygame.image.load("resources/rooms/" + room + ".png"), room_scaled_size).convert_alpha()
            #self.images_dict[room] = pygame.image.load("resources/rooms/" + room + ".png").convert()

        for door in self.doors_:
            self.images_dict[door] = pygame.image.load("resources/doors/" + door + ".png").convert_alpha()

        for block in self.blocks_:
            self.images_dict[block] = pygame.image.load("resources/blocks/" + block + ".png").convert_alpha()

        self.images_dict["items"] = pygame.image.load("resources/items/items.png").convert_alpha()
        self.images_dict["bullet"] = pygame.image.load("resources/other/tears.png").convert_alpha()
        self.images_dict["tears"] = pygame.image.load("resources/other/tears.png").convert_alpha()
        self.images_dict["tears_pop"] = pygame.image.load("resources/other/tears_pop.png").convert_alpha()

    def load_blocks(self):
        self.blocks["rock1"] = pygame.transform.scale(self.images_dict["rocks2"].subsurface(pygame.Rect(5, 5, 51, 55)), (self.settings.TILE_SIZE, self.settings.TILE_SIZE)).convert_alpha()
        self.blocks["rock2"] = pygame.transform.scale(self.images_dict["rocks2"].subsurface(pygame.Rect(67, 5, 55, 57)), (self.settings.TILE_SIZE, self.settings.TILE_SIZE)).convert_alpha()
        self.blocks["rock3"] = pygame.transform.scale(self.images_dict["rocks2"].subsurface(pygame.Rect(131, 1, 55, 63)), (self.settings.TILE_SIZE, self.settings.TILE_SIZE)).convert_alpha()
        self.blocks["rock4"] = pygame.transform.scale(self.images_dict["rocks2"].subsurface(pygame.Rect(69, 69, 51, 55)), (self.settings.TILE_SIZE, self.settings.TILE_SIZE)).convert_alpha()
        self.blocks["rock5"] = pygame.transform.scale(self.images_dict["rocks2"].subsurface(pygame.Rect(69, 133, 51, 56)), (self.settings.TILE_SIZE, self.settings.TILE_SIZE)).convert_alpha()
        self.blocks["rock6"] = pygame.transform.scale(self.images_dict["rocks2"].subsurface(pygame.Rect(197, 135, 53, 55)), (self.settings.TILE_SIZE, self.settings.TILE_SIZE)).convert_alpha()

    def load_tears(self):
        self.tears["blue_tear"] = pygame.transform.scale(self.images_dict["tears"].subsurface(pygame.Rect(650, 12, 42, 42)), (BULLET_WIDTH, BULLET_HEIGHT)).convert_alpha()
        self.tears["red_tear"] = pygame.transform.scale(self.images_dict["tears"].subsurface(pygame.Rect(650, 76, 42, 42)), (BULLET_WIDTH, BULLET_HEIGHT)).convert_alpha()

        for i in range(16):
            self.tears["blue_tear_pop" + str(i)] = pygame.transform.scale(self.images_dict["tears_pop"].subsurface(pygame.Rect(i * 64, 0, 64, 64)), (BULLET_WIDTH*3, BULLET_HEIGHT*3)).convert_alpha()
            self.tears["red_tear_pop" + str(i)] = pygame.transform.scale(self.images_dict["tears_pop"].subsurface(pygame.Rect(i * 64, 64, 64, 64)), (BULLET_WIDTH*2, BULLET_HEIGHT)).convert_alpha()

    def get_image(self, name: str):
        return self.images_dict[name]
       
