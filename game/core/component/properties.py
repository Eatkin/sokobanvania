class Properties:
    """
    Properties component for a configurable grab bag of properties.
    """
    def __init__(self,):
        super().__init__()


    def attach(self, entity):
        """
        Attach the component to an entity.

        Args:
            entity: The entity to attach the component to.
        """
        entity.properties = self
        entity.components['properties'] = self
