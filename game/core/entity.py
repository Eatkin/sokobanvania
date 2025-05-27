class Entity:
    def __init__(self):
        self.components = {}

    def update(self):
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
