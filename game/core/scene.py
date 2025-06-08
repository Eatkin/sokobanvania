from collections import defaultdict
from core import is_physics_tick
from core.layer import Layer

class Scene:
    def __init__(self, width=800, height=600):
        self.layers = {}
        self.width = width
        self.height = height
        self.entities = []
        self.occupancy_map = defaultdict(list)

    def add_layer(self, layer):
        """Add a layer to the scene."""
        self.layers[layer.name] = layer
        layer.scene = self

    def update(self):
        """Update all layers in the scene."""
        # Main updates
        for entity in self.entities:
            entity.update()

        # Fixed updates
        while is_physics_tick():
            # We stage for movement and then apply it in fixed update
            for entity in self.entities:
                entity.staging_update()

            for entity in self.entities:
                entity.fixed_update()


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

        # Add to the occupancy map if the entity has a position
        if hasattr(entity, 'position'):
            x, y = entity.position.x, entity.position.y
            self.occupy(x, y, entity)

    def remove_entity(self, entity, destroy_entity=True):
        layer = entity.layer
        layer.remove_entity(entity)
        entity.layer = None
        entity.scene = None
        self.entities.remove(entity)
        # Also de-occupy the position if it exists
        if hasattr(entity, 'position'):
            # Occupancy is at proposed target position if it exists, otherwise at current position
            x, y = entity.position.get_occupied_tile()
            self.vacate(x, y, entity)
        if destroy_entity:
            entity.delete()

    def get_entities_by_class(self, cls):
        """Get all entities of a specific class (or classes) in the scene."""
        if isinstance(cls, list):
            return [e for e in self.entities if isinstance(e, tuple(cls))]

        return [e for e in self.entities if isinstance(e, cls)]

    def get_occupants(self, x, y):
        """Gets occupants of a specific position in the grid."""
        return self.occupancy_map.get((x, y), [])

    def occupy(self, x, y, entity):
        """Occupy a position in the grid with an entity."""
        if entity not in self.occupancy_map[(x, y)]:
            self.occupancy_map[(x, y)].append(entity)

    def vacate(self, x, y, entity):
        """Remove an entity from a specific position in the grid."""
        try:
            self.occupancy_map[(x, y)].remove(entity)
            if not self.occupancy_map[(x, y)]:
                del self.occupancy_map[(x, y)]
        except (ValueError, KeyError):
            pass

    def is_blocked(self, x, y, blocking_classes=None):
        """
        Check if a position (x, y) is blocked by any entity of the specified blocking classes.
        Args:
            x (int): The x-coordinate in grid units.
            y (int): The y-coordinate in grid units.
            blocking_classes (tuple, optional): A tuple of classes that block movement. If None, any occupant blocks.
        Returns:
            list: A list of entities blocking the position, or an empty list if not blocked.
        """
        occupants = self.get_occupants(x, y)

        if blocking_classes is None:
            return occupants  # Any presence is a block

        res = []
        for entity in occupants:
            if isinstance(entity, tuple(blocking_classes)):
                res.append(entity)

        return res if res else []

class BaseScene(Scene):
    def __init__(self, width=800, height=600):
        super().__init__(width=width, height=height)
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
