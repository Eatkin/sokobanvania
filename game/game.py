import atexit
import pygame
from core import update_timing
from core.input import get_input_handler
from core.debugger import Debugger
from core.scene import BaseScene

from entities.player import Player
from entities.blocks import Block, GreenLockBlock
from entities.pickup import PickUp
from entities.background_tiler import BackgroundTiler

@atexit.register
def cleanup():
    pygame.quit()

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.running = True
        self.current_scene = None

        self.input_handler = get_input_handler()
        self.debugger = Debugger()

    def update(self):
        self.debugger.update()
        self.input_handler.update()
        if self.current_scene:
            self.current_scene.update()

    def render(self):
        if self.current_scene:
            self.current_scene.render(self.screen)

        self.debugger.render(self.screen)
        pygame.display.flip()
        # Clear screen again
        self.screen.fill((0, 0, 0))

    def run(self):
        self.current_scene = BaseScene()
        player = Player(32, 32)
        self.current_scene.add_entity_to_layer(player, "player")

        # Add a few blocks
        for coords in zip([64, 96, 128, 160], [32, 64, 96, 128]):
            block = Block(*coords)
            self.current_scene.add_entity_to_layer(block, "game")

        # Add a green key
        key = PickUp(32, 128, "green_key")
        self.current_scene.add_entity_to_layer(key, "items")

        # Add a green lock block
        green_lock_block = GreenLockBlock(96, 128)
        self.current_scene.add_entity_to_layer(green_lock_block, "game")

        tiler = BackgroundTiler(width=self.current_scene.width, height=self.current_scene.height)
        self.current_scene.add_entity_to_layer(tiler, "background")


        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            update_timing()
            self.update()
            self.render()
