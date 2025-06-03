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

    # Misc methods with no-op to prevent weird crashes
    def on_inventory_change(self):
        pass
