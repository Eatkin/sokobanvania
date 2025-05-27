from core.layer import Layer

class Scene:
    def __init__(self, width=800, height=600):
        self.layers = {}
        self.width = width
        self.height = height

    def add_layer(self, layer):
        """Add a layer to the scene."""
        self.layers[layer.name] = layer

    def update(self):
        """Update all layers in the scene."""
        for layer in self.layers.values():
            layer.update()

    def render(self, screen):
        """Render all layers in the scene."""
        for layer in self.layers.values():
            layer.render(screen)

    def add_entity_to_layer(self, entity, layer_name):
        """Add an entity to a specific layer."""
        if layer_name in self.layers:
            self.layers[layer_name].add_entity(entity)
        else:
            raise ValueError(f"Layer '{layer_name}' not found in the scene.")

    def remove_entity_from_layer(self, entity, layer_name):
        """Remove an entity from a specific layer."""
        if layer_name in self.layers:
            self.layers[layer_name].remove_entity(entity)
        else:
            raise ValueError(f"Layer '{layer_name}' not found in the scene.")

class BaseScene(Scene):
    def __init__(self, width=800, height=600):
        super().__init__(width=800, height=600)
        # Create default layers
        layers = [
            Layer("background"),
            Layer("game"),
            Layer("ui")
        ]
        for layer in layers:
            self.add_layer(layer)
