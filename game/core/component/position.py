from core.component.component import Component

class Position(Component):
    """
    Component that represents the position of an entity in the game world.
    """
    def __init__(self, x=0, y=0):
        super().__init__()
        self.x = x
        self.y = y
        self.xprevious = x
        self.yprevious = y
        self.target = None

    def attach(self, entity):
        """
        Attach the component to an entity.

        Args:
            entity: The entity to attach the component to.
        """
        entity.position = self
        entity.components['position'] = self

    def get_occupied_tile(self):
        """
        Get the tile coordinates occupied by this position.

        Returns:
            tuple: (tile_x, tile_y) coordinates of the occupied tile.
        """
        if self.target:
            return self.target
        return self.x, self.y
