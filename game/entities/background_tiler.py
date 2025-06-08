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
        self.add_component(Sprite(SPRITES['tiles']['floor_tile']))
        tile_width, tile_height = self.sprite.width, self.sprite.height
        for x in range(0, width, tile_width):
            for y in range(0, height, tile_height):
                self.image.blit(self.sprite.image, (x, y))

        self.rect = self.image.get_rect(topleft=(0, 0))

        # Overwrite our sprite update method to do nothing
        self.sprite.update = lambda pos: None
        self.sprite.image = self.image
