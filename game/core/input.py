import pygame
from enum import Enum

class KeyAction(Enum):
    KEY_LEFT = 1
    KEY_RIGHT = 2
    KEY_UP = 3
    KEY_DOWN = 4
    KEY_ACTION = 5

class InputHandler:
    def __init__(self):
        """Initialize the input handler and set up key states."""
        self.keys_pressed = self.get_default_state()
        self.keys_released = self.get_default_state()
        self.keys_held = self.get_default_state()

    def get_default_state(self):
        default_state = {action: False for action in KeyAction}
        return default_state

    def update(self):
        """Update the state of the keys for this frame."""
        self.keys_pressed = self.get_default_state()
        self.keys_released = self.get_default_state()

        keys = pygame.key.get_pressed()

        for action in KeyAction:
            key = self._get_key_for_action(action)
            is_pressed = keys[key]

            if is_pressed:
                # Mark as pressed if it was not already held
                if not self.keys_held.get(action, False):
                    self.keys_pressed[action] = True
                self.keys_held[action] = True
            else:
                # Mark as released if it was held until now
                if self.keys_held.get(action, False):
                    self.keys_released[action] = True
                self.keys_held[action] = False

    def _get_key_for_action(self, action: KeyAction):
        """Map actions to their corresponding pygame keys"""
        if action == KeyAction.KEY_LEFT:
            return pygame.K_LEFT
        elif action == KeyAction.KEY_RIGHT:
            return pygame.K_RIGHT
        elif action == KeyAction.KEY_UP:
            return pygame.K_UP
        elif action == KeyAction.KEY_DOWN:
            return pygame.K_DOWN
        elif action == KeyAction.KEY_ACTION:
            return pygame.K_SPACE
        return None  # Default case (can be extended)

    def is_key_pressed(self, action: KeyAction):
        """Returns True if the key for this action is pressed in this frame."""
        return self.keys_pressed.get(action, False)

    def is_key_held(self, action: KeyAction):
        """Returns True if the key for this action is being held down."""
        return self.keys_held.get(action, False)

    def is_key_released(self, action: KeyAction):
        """Returns True if the key for this action is released in this frame."""
        return self.keys_released.get(action, False)

    def get_all_states(self):
        """Returns a dictionary of all key states."""
        return {
            "pressed": self.keys_pressed,
            "held": self.keys_held,
            "released": self.keys_released
        }

# Global instance to access InputHandler
INPUT_HANDLER = None

def get_input_handler():
    """Initialises and returns the input handler."""
    global INPUT_HANDLER
    if INPUT_HANDLER is None:
        INPUT_HANDLER = InputHandler()

    return INPUT_HANDLER

def get_input():
    """Returns the current state of all keys as a dictionary."""
    global INPUT_HANDLER
    if INPUT_HANDLER is None:
        raise Exception("Input handler not initialized. Call init_input_handler() first.")
    return INPUT_HANDLER.get_all_states()
