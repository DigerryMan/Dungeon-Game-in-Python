import pygame

class ImageLoader:
    def __init__(self):
        self._mobs = ["alpha_maggot", "fly","legs", "maggot", "parasite", "slime"]
        self._path = "resources/mobs/"
        self._images_dict = {}
        self.__load_images_to_dict()

    def __load_images_to_dict(self):
        for mob in self._mobs:
            self._images_dict[mob] = pygame.image.load(self._path + mob + ".png")

    def get_image(self, name: str):
        return self._images_dict[name]
       
