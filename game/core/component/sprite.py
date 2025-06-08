import pygame
from core.component.component import Component
from common.sprites import SpriteInfo
from core import get_alpha

class Sprite(Component, pygame.sprite.Sprite):
    """
    Component that represents a sprite for an entity.
    """
    def __init__(self, sprite_info: SpriteInfo, components: list[Component]|None=None):
        # Multiclass inheritence yo
        for c in [Component, pygame.sprite.Sprite]:
            c.__init__(self)
        self.sprite_info = sprite_info
        # We can switch out for no-op if invisible
        self.base_image = pygame.image.load(sprite_info.path)
        if sprite_info.alpha_channel:
            self.base_image = self.base_image.convert_alpha()
        else:
            self.base_image = self.base_image.convert()

        self.image = self.base_image

        self.render_group = None
        self._visible = True
        self.visible = self._visible

        self.rect = self.image.get_rect()

        if components:
            for component in components:
                component.attach(self)

        self.x_draw = 0
        self.y_draw = 0

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

    @property
    def visible(self):
        return self._visible

    @visible.setter
    def visible(self, value):
        # Don't do anything if the state isn't changing
        if value == self._visible:
            return

        print("Changing sprite visibility to", value)

        self._visible = value
        if value:
            # If we're becoming visible, add ourselves back to the group
            if self.render_group:
                self.render_group.add(self)
        else:
            # If we're becoming invisible, remove ourselves from the group
            if self.render_group:
                print("Removing sprite from render group")
                self.render_group.remove(self)

    def update(self, position):
        """
        Update draw position and other properties of the sprite.
        """
        # This logic correctly sets self.image to the right frame or flip state
        if hasattr(self, 'xflip'):
            if self.xflip:
                if not self._last_xflip:
                    self._flipped_base_image = pygame.transform.flip(self.base_image, True, False)
                    self._last_xflip = True
                self.image = self._flipped_base_image
            else:
                self.image = self.base_image
                self._last_xflip = False

        alpha = get_alpha()
        x_draw = position.xprevious * (1 - alpha) + position.x * alpha
        y_draw = position.yprevious * (1 - alpha) + position.y * alpha
        self.rect.topleft = (x_draw, y_draw)

    def attach(self, entity):
        """
        Attach the component to an entity.

        Args:
            entity: The entity to attach the component to.
        """
        entity.sprite = self
        entity.components['sprite'] = self

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
