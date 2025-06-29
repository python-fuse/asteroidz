import sys
import pygame

from entities import AsteroidManager, BulletsManager, Player
from utils.constants import WINDOW_HEIGHT, WINDOW_WIDTH

pygame.init()
pygame.display.set_caption("Azteroidz")


SPAWN_ASTEROID = pygame.USEREVENT + 10
SPAND_ASTEROID_DELAY = 2000
MAX_ASTEROIDS = 10


class Game:
    def __init__(self) -> None:
        # Initialize the game window and clock
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.is_running = True

        # custome events
        pygame.time.set_timer(SPAWN_ASTEROID, SPAND_ASTEROID_DELAY)

        # Managers
        self.player_bullet_manager = BulletsManager()
        self.asteroids_manager = AsteroidManager()

        # Create the entities
        self.player = Player(
            WINDOW_WIDTH // 2,
            WINDOW_HEIGHT // 2,
            40,
            60,
            "./assets/player.png",
            self.player_bullet_manager,
        )

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if (
                event.type == SPAWN_ASTEROID
                and len(self.asteroids_manager.get_asteroids()) < MAX_ASTEROIDS
            ):
                self.asteroids_manager.spawn(self.player)

    def handle_input(self):
        keys = pygame.key.get_pressed()
        self.player.handle_input(keys)

    def draw(self):
        self.window.fill((0, 0, 0))

        # Draw the player
        self.player.draw(self.window)

        # Draw asteroids
        self.asteroids_manager.draw(self.window)

    def update(self):
        self.draw()

        # Call entity update methods
        self.player.update()
        self.asteroids_manager.update()

    def run(self):
        while self.is_running:
            self.handle_events()
            self.update()
            self.handle_input()

            pygame.display.flip()
            self.clock.tick(self.fps)
