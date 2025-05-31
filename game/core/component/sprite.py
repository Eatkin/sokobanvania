import pygame
from core.component.component import Component
from common.sprites import SpriteInfo
from core import get_alpha

class Sprite(Component):
    """
    Component that represents a sprite for an entity.
    """
    def __init__(self, sprite_info: SpriteInfo, components: list[Component]|None=None):
        super().__init__()
        self.sprite_info = sprite_info
        self.visible = True
        self.image = pygame.image.load(sprite_info.path)
        if sprite_info.alpha_channel:
            self.image = self.image.convert_alpha()
        else:
            self.image = self.image.convert()
        self.rect = self.image.get_rect()
        if components:
            for component in components:
                component.attach(self)

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
        if not self.visible:
            return

        image_to_draw = self.image

        if hasattr(self, 'xflip') and self.xflip:
            if not self._last_xflip or self._flipped_image is None:
                self._flipped_image = pygame.transform.flip(self.image, True, False)
            image_to_draw = self._flipped_image
            self._last_xflip = True
        else:
            self._last_xflip = False

        alpha = get_alpha()
        x_draw = position.xprevious * (1 - alpha) + position.x * alpha
        y_draw = position.yprevious * (1 - alpha) + position.y * alpha
        self.rect.topleft = (x_draw, y_draw)

        screen.blit(image_to_draw, self.rect)



# Sprite Components to extend functionality
class Xflip(Component):
    """Component to handle horizontal flipping of a sprite."""
    def attach(self, entity):
        """
        Attach the component to an entity.

        Args:
            entity: The entity to attach the component to.
        """
        entity.xflip = False
        entity._flipped_image = None
        entity._last_xflip = False
