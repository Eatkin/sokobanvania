import pygame
from core.entity import Entity
from core.component.sprite import Sprite
from common.sprites import SPRITES

class BackgroundTiler(Entity):
    """Tiles the background with a particular image"""
    def __init__(self, width, height):
        # You only draw once
        # This is a fucking jank ass way of making a tiled background
        super().__init__()
        self.image = pygame.Surface((width, height))
        sprite_info = SPRITES['tiles']['floor_tile']
        self.base_image = pygame.image.load(sprite_info.path)

        if sprite_info.alpha_channel:
            self.base_image = self.base_image.convert_alpha()
        else:
            self.base_image = self.base_image.convert()

        tile_width, tile_height = self.base_image.width, self.base_image.height
        for x in range(0, width, tile_width):
            for y in range(0, height, tile_height):
                self.image.blit(self.base_image, (x, y))

        self.rect = self.image.get_rect(topleft=(0, 0))
