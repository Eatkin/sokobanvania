from core.component.component import Component
from core.input import get_input, KeyAction

class InputParser(Component):
    """
    Component that parses input from the user.
    """
    def __init__(self):
        super().__init__()
        self.hinput = 0
        self.vinput = 0

    def attach(self, entity):
        """
        Attach the component to an entity.

        Args:
            entity: The entity to attach the component to.
        """
        entity.input = self
        entity.components['input'] = self

    def update(self):
        input = get_input()
        self.hinput = input['held'][KeyAction.KEY_RIGHT] - input['held'][KeyAction.KEY_LEFT]
        self.vinput = input['held'][KeyAction.KEY_DOWN] - input['held'][KeyAction.KEY_UP]
