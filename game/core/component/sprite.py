import pygame
from core.component.component import Component
from common.sprites import SpriteInfo

class Sprite(Component):
    """
    Component that represents a sprite for an entity.
    """
    def __init__(self, sprite_info: SpriteInfo):
        super().__init__()
        self.sprite_info = sprite_info
        self.visible = True
        self.image = pygame.image.load(sprite_info.path)
        if sprite_info.alpha_channel:
            self.image = self.image.convert_alpha()
        else:
            self.image = self.image.convert()
        self.rect = self.image.get_rect()

    @property
    def width(self):
        """
        Get the width of the sprite.

        Returns:
            int: The width of the sprite.
        """
        return self.rect.width

    @property
    def height(self):
        """
        Get the height of the sprite.

        Returns:
            int: The height of the sprite.
        """
        return self.rect.height

    def attach(self, entity):
        """
        Attach the component to an entity.

        Args:
            entity: The entity to attach the component to.
        """
        entity.sprite = self
        entity.components['sprite'] = self

    def draw(self, screen, position):
        """
        Draw the sprite on the screen at the given position.

        Args:
            screen: The screen to draw the sprite on.
            position: The position to draw the sprite at.
        """
        if not self.visible:
            return
        self.rect.topleft = (position.x, position.y)
        screen.blit(self.image, self.rect)
