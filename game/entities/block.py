from core.entity import Solid
from common.sprites import SPRITES

class Block(Solid):
    def __init__(self, x, y):
        sprite = SPRITES['tiles']['wall_tile']
        super().__init__(x, y, sprite_info=sprite)
