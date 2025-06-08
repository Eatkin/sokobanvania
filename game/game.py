import atexit
import pygame
from core import update_timing
from core.input import get_input_handler
from core.debugger import Debugger
from entities.background_tiler import BackgroundTiler
from core.scene import BaseScene

from core.level_parser import get_level

@atexit.register
def cleanup():
    pygame.quit()

class Game:
    def __init__(self):
        pygame.init()
        flags = pygame.DOUBLEBUF
        self.screen = pygame.display.set_mode((800, 600), flags)
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
        dirty_rects = None
        if self.current_scene:
            background_surface = self.current_scene.background_surface
            self.current_scene.render_group.clear(self.screen, background_surface)
            dirty_rects = self.current_scene.render_group.draw(self.screen)

        if dirty_rects:
            print(f"Dirty Rects: {dirty_rects}")

        pygame.display.update(dirty_rects)

    def run(self):
        self.current_scene = get_level("assets/levels/lesson2.lvl")

        self.screen.blit(self.current_scene.background_surface, (0, 0))
        self.current_scene.render_group.draw(self.screen)
        pygame.display.flip()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            update_timing()
            self.update()
            self.render()
