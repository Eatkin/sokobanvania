class Layer:
    """
    A class representing a layer in a game engine.
    """
    def __init__(self, name: str):
        """
        Initialize the Layer with a name.

        :param name: The name of the layer.
        """
        self.name = name
        self.entities = []
        self.scene = None

    def update(self):
        """
        This method should be called every frame to update the state of the layer.
        """
        pass

    def render(self, screen):
        """
        Render all entities in the layer to the given screen.

        :param screen: The screen to render the entities on.
        """
        for entity in self.entities:
            entity.draw(screen)

    def add_entity(self, entity):
        """
        Add an entity to the layer.

        :param entity: The entity to add.
        """
        self.entities.append(entity)

    def remove_entity(self, entity):
        """
        Remove an entity from the layer.

        :param entity: The entity to remove.
        """
        self.entities.remove(entity)
