from core.component.position import Position
from core.component.sprite import Sprite
from core.component.collision import CollisionBox

class Entity:
    def __init__(self):
        self.components = {}
        self.layer = None
        self.scene = None

    def update(self):
        # General updates every frame
        pass

    def fixed_update(self):
        # Fixed updates every physics tick (e.g., 60 FPS)
        pass

    def draw(self, screen):
        if hasattr(self, 'sprite') and hasattr(self, 'position'):
            self.sprite.draw(screen, self.position)


    def add_component(self, component):
        """
        Add a component to the entity.

        Args:
            component: The component to add.
        """
        component.attach(self)

    def destroy(self):
        """
        Destroy the entity, removing it from the scene and cleaning up.
        """
        if self.scene:
            self.scene.remove_entity(self)

    def delete(self):
        """
        Destructor for behaviour on dereferencing the entity.
        """
        pass

# Subclasses here
class Solid(Entity):
    def __init__(self, x, y, sprite_info, components=None):
        super().__init__()
        self.add_component(Position(x, y))
        self.add_component(Sprite(sprite_info, components=components))
        self.add_component(CollisionBox())

        # Add components
        if components:
            for component in components:
                self.add_component(component)
