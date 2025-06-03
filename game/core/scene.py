from core import is_physics_tick
from core.layer import Layer

class Scene:
    def __init__(self, width=800, height=600):
        self.layers = {}
        self.width = width
        self.height = height
        self.entities = []

    def add_layer(self, layer):
        """Add a layer to the scene."""
        self.layers[layer.name] = layer
        layer.scene = self

    def update(self):
        """Update all layers in the scene."""
        # Fixed updates
        while is_physics_tick():
            for entity in self.entities:
                entity.fixed_update()

        # Then other updates
        for layer in self.layers.values():
            layer.update()

    def render(self, screen):
        """Render all layers in the scene."""
        for layer in self.layers.values():
            layer.render(screen)

    def add_entity_to_layer(self, entity, layer_name):
        if layer_name not in self.layers:
            raise ValueError(f"Layer '{layer_name}' not found in the scene.")
        layer = self.layers[layer_name]
        layer.add_entity(entity)
        entity.layer = layer
        entity.scene = self
        self.entities.append(entity)

    def remove_entity(self, entity, destroy_entity=True):
        layer = entity.layer
        layer.remove_entity(entity)
        entity.layer = None
        entity.scene = None
        self.entities.remove(entity)
        if destroy_entity:
            entity.delete()

    def get_entities_by_class(self, cls):
        """Get all entities of a specific class (or classes) in the scene."""
        if isinstance(cls, list):
            return [e for e in self.entities if isinstance(e, tuple(cls))]

        return [e for e in self.entities if isinstance(e, cls)]


class BaseScene(Scene):
    def __init__(self, width=800, height=600):
        super().__init__(width=800, height=600)
        # Create default layers
        layers = [
            Layer("background"),
            Layer("items"),
            Layer("game"),
            Layer("player"),
            Layer("ui")
        ]
        for layer in layers:
            self.add_layer(layer)
