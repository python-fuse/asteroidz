import sys
import pygame

from entities import AsteroidManager, BulletsManager, Player
from utils.constants import ASTEROID_SCORE_UP_EVENT, WINDOW_HEIGHT, WINDOW_WIDTH


SPAWN_ASTEROID = pygame.USEREVENT + 10
SPAND_ASTEROID_DELAY = 2000
MAX_ASTEROIDS = 20


class Game:
    def __init__(self) -> None:
        # Initialize pygame the game window and clock
        pygame.init()
        pygame.display.set_caption("Azteroidz")
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.fps = 60

        # font
        self.score_font = pygame.font.SysFont("Ani", 60)

        # Score
        self.score = 0

        # custome events
        pygame.time.set_timer(SPAWN_ASTEROID, SPAND_ASTEROID_DELAY)

        # Managers
        self.player_bullet_manager = BulletsManager()
        self.asteroids_manager = AsteroidManager(self.player_bullet_manager)

        # Create the entities
        self.player = Player(
            WINDOW_WIDTH // 2,
            WINDOW_HEIGHT // 2,
            40,
            60,
            "./assets/player.png",
            self.player_bullet_manager,
        )

        # Game run conditions
        self.is_running = True
        self.game_over = False

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

            if event.type == ASTEROID_SCORE_UP_EVENT.type:
                self.score += 25

    def handle_input(self):
        keys = pygame.key.get_pressed()
        self.player.handle_input(keys)

    def draw(self):
        self.window.fill((0, 0, 0))

        # Draw score
        score_surface = self.score_font.render(str(self.score), True, (255, 255, 155))
        self.window.blit(score_surface, (10, 10))

        # Draw the player
        self.player.draw(self.window)

        # Draw asteroids
        self.asteroids_manager.draw(self.window)

    def update(self):
        self.draw()

        # Call entity update methods
        self.player.update()
        self.asteroids_manager.update()

    def handle_game_over(self):
        if (
            self.player.x < 0
            or self.player.x > WINDOW_WIDTH
            or self.player.y < 0
            or self.player.y > WINDOW_HEIGHT
        ):
            self.game_over = True

    def run(self):
        while self.is_running:
            self.update()

            self.handle_events()
            self.handle_input()
            self.handle_game_over()

            pygame.display.flip()
            self.clock.tick(self.fps)
