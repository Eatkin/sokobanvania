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
        Destructor for behaviour on dereferencing the entity.
        """
        pass
