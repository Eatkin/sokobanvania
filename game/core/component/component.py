from abc import ABC, abstractmethod

class Component(ABC):
    """
    Abstract base class for all components in the game.
    Components are used to add functionality to entities.
    """
    def __init__(self):
        super().__init__()

    @abstractmethod
    def attach(self, entity):
        """
        Attach the component to an entity.

        Args:
            entity: The entity to attach the component to.
        """
        pass
