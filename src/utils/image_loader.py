import pygame

class ImageLoader:
    def __init__(self, settings):
        self.settings = settings

        self.menu_ = ["introbackground", "menucard", "settingscard", "menuoverlay", "pausecard2", "arrow2", "maintitle"]
        self.mobs_ = ["alpha_maggot", "fly","legs", "maggot", "parasite", "slime"]
        self.rooms_ = ["basement", "catacombs", "caves", "controls", "depths", "necropolis", "shading", "shop", "utero", "womb"]
        self.doors_ = ["angel_door", "boss_door", "devil_door", "door", "red_door"]
        self.blocks_ = ["rocks2"]

        self.images_dict = {}
        self.__load_images_to_dict()

        self.blocks = {}
        self.load_blocks()

    def __load_images_to_dict(self):
        for menu_element in self.menu_:
            self.images_dict[menu_element] = pygame.image.load("resources/menu/" + menu_element + ".png")

        for mob in self.mobs_:
            self.images_dict[mob] = pygame.image.load("resources/mobs/" + mob + ".png")

        for room in self.rooms_:
            self.images_dict[room] = pygame.image.load("resources/rooms/" + room + ".png")

        for door in self.doors_:
            self.images_dict[door] = pygame.image.load("resources/doors/" + door + ".png")

        for block in self.blocks_:
            self.images_dict[block] = pygame.image.load("resources/blocks/" + block + ".png")

    def load_blocks(self):
        self.blocks["rock1"] = pygame.transform.smoothscale(self.images_dict["rocks2"].subsurface(pygame.Rect(5, 5, 51, 55)), (self.settings.TILE_SIZE, self.settings.TILE_SIZE))
        self.blocks["rock2"] = pygame.transform.smoothscale(self.images_dict["rocks2"].subsurface(pygame.Rect(67, 5, 55, 57)), (self.settings.TILE_SIZE, self.settings.TILE_SIZE))
        self.blocks["rock3"] = pygame.transform.smoothscale(self.images_dict["rocks2"].subsurface(pygame.Rect(131, 1, 55, 63)), (self.settings.TILE_SIZE, self.settings.TILE_SIZE))
        self.blocks["rock4"] = pygame.transform.smoothscale(self.images_dict["rocks2"].subsurface(pygame.Rect(69, 69, 51, 55)), (self.settings.TILE_SIZE, self.settings.TILE_SIZE))
        self.blocks["rock5"] = pygame.transform.smoothscale(self.images_dict["rocks2"].subsurface(pygame.Rect(69, 133, 51, 56)), (self.settings.TILE_SIZE, self.settings.TILE_SIZE))
        self.blocks["rock6"] = pygame.transform.smoothscale(self.images_dict["rocks2"].subsurface(pygame.Rect(197, 135, 53, 55)), (self.settings.TILE_SIZE, self.settings.TILE_SIZE))

    def get_image(self, name: str):
        return self.images_dict[name]
       
