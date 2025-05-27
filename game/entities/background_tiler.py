import pygame
from core.entity import Entity
from core.input import get_input, KeyAction
from core.component.position import Position
from core.component.velocity import Velocity
from core.component.sprite import Sprite
from core import get_delta_time
from common.sprites import SPRITES

class BackgroundTiler(Entity):
    """Tiles the background with a particular image"""
    def __init__(self, width, height):
        # Blue square
        super().__init__()
        self.add_component(Sprite(SPRITES['tiles']['floor_tile']))
        self.width = width
        self.height = height

    def draw(self, screen):
        tile_width, tile_height = self.sprite.width, self.sprite.height
        for x in range(0, self.width, tile_width):
            for y in range(0, self.height, tile_height):
                screen.blit(self.sprite.image, (x, y))
