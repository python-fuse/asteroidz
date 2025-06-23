import sys
import pygame

from utils.constants import WINDOW_HEIGHT, WINDOW_WIDTH

pygame.init()
pygame.display.set_caption("Azteroidz")


class Game:
    def __init__(self) -> None:
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()

        self.is_running = True

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def draw(self):
        pass

    def update(self):
        self.draw()

    def run(self):
        while self.is_running:
            self.handle_events()
            self.update()
