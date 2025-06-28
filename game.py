import sys
import pygame

from entities import Player
from utils.constants import WINDOW_HEIGHT, WINDOW_WIDTH

pygame.init()
pygame.display.set_caption("Azteroidz")


class Game:
    def __init__(self) -> None:
        # Initialize the game window and clock
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.is_running = True

        # Create the entities
        self.player = Player(
            WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, 50, 70, "./assets/player.png"
        )

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def handle_input(self):
        keys = pygame.key.get_pressed()
        self.player.handle_input(keys)

    def draw(self):
        self.window.fill((0, 0, 0))

        # Draw the player
        self.player.draw(self.window)

    def update(self):
        self.draw()

        # Call entity update methods
        self.player.update()

    def run(self):
        while self.is_running:
            self.handle_events()
            self.update()
            self.handle_input()

            pygame.display.flip()
            self.clock.tick(self.fps)
