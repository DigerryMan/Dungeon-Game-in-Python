import pygame


class ImageTransformer:
    def change_image_to_more_red(image):
        new_image = pygame.Surface(image.get_size(), pygame.SRCALPHA)
        for x in range(image.get_width()):
            for y in range(image.get_height()):
                pixel_color = image.get_at((x, y))

                if pixel_color.a <= 0:
                    new_image.set_at((x, y), pixel_color)
                else:
                    new_red = min(pixel_color.r + 100, 255)
                    new_pixel_color = (
                        new_red,
                        pixel_color.g,
                        pixel_color.b,
                        pixel_color.a,
                    )
                    new_image.set_at((x, y), new_pixel_color)
        return new_image

    def change_opacity(image, opacity=50):
        image = image.copy()
        if 0 <= opacity <= 255:
            for x in range(image.get_width()):
                for y in range(image.get_height()):
                    r, g, b, a = image.get_at((x, y))
                    if a != 0:
                        image.set_at((x, y), (r, g, b, opacity))
        return image
