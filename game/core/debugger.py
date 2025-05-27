import pygame
import tracemalloc
from core import get_delta_time

tracemalloc.start()  # Do this once, here is fine

class Debugger:
    def __init__(self, smoothing=0.9, font_size=18):
        self.font = pygame.font.SysFont("consolas", font_size)
        self.smoothing = smoothing
        self.smoothed_fps = 0.0

    def update(self):
        dt = get_delta_time()
        current_fps = 1.0 / dt if dt > 0 else 0.0

        if self.smoothed_fps == 0.0:
            self.smoothed_fps = current_fps
        else:
            self.smoothed_fps = (
                self.smoothed_fps * self.smoothing + current_fps * (1 - self.smoothing)
            )

    def render(self, screen):
        current, peak = tracemalloc.get_traced_memory()
        mem_text = f"MEM: {current / (1024 * 1024):.2f} MB"
        fps_text = f"FPS: {self.smoothed_fps:.1f}"

        fps_surface = self.font.render(fps_text, True, (0, 255, 0))
        mem_surface = self.font.render(mem_text, True, (255, 255, 0))

        screen.blit(fps_surface, (10, 10))
        screen.blit(mem_surface, (10, 30))
