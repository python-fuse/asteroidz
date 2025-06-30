import sys
import pygame

from entities import AsteroidManager, BulletsManager, Player
from utils.constants import ASTEROID_SCORE_UP_EVENT, WINDOW_HEIGHT, WINDOW_WIDTH
from utils.ui import Button


SPAWN_ASTEROID = pygame.USEREVENT + 10
SPAND_ASTEROID_DELAY = 2000
MAX_ASTEROIDS = 20

pygame.init()
pygame.display.set_caption("Azteroidz")


class Game:
    def __init__(self) -> None:
        # Initialize pygame the game window and clock
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
        # Create the entities
        self.player = Player(
            WINDOW_WIDTH // 2,
            WINDOW_HEIGHT // 2,
            40,
            60,
            "./assets/player.png",
            self.player_bullet_manager,
        )

        self.asteroids_manager = AsteroidManager(
            self.player_bullet_manager, self.player
        )

        # Game run conditions
        self.is_running = True
        self.game_over = False

        # UI components
        # retry button
        self.retry_button = Button(
            "Retry",
            WINDOW_WIDTH // 2 - 50,
            WINDOW_HEIGHT // 2 + 50,
            100,
            50,
            self.score_font,
            (255, 255, 255),
            action=lambda: self.__init__(),
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

            if event.type == ASTEROID_SCORE_UP_EVENT.type:
                self.score += 25

    def handle_input(self):
        keys = pygame.key.get_pressed()
        self.player.handle_input(keys)

        # Handle mouse events for the retry button
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()
        if self.retry_button.is_clicked(mouse_pos) and mouse_click[0]:
            # If the retry button is clicked, reset the game
            self.retry_button.handle_click()

    def draw_game_over(self):
        # Show game over message and retry button
        game_over_screen = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        game_over_screen.fill((12, 12, 12, 50))

        game_over_text_surface = self.score_font.render("Game Over", True, (255, 0, 0))

        game_over_rect = game_over_text_surface.get_rect(
            center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        )

        # Draw score
        score_surface = self.score_font.render(
            f"Score: {self.score}", True, (255, 255, 155)
        )

        score_rect = score_surface.get_rect(
            center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 4)
        )

        game_over_screen.blit(score_surface, score_rect)

        self.retry_button.draw(game_over_screen)
        game_over_screen.blit(game_over_text_surface, game_over_rect)
        self.window.blit(game_over_screen, (0, 0))

    def draw(self):
        self.window.fill((0, 0, 0))

        # Draw score
        score_surface = self.score_font.render(str(self.score), True, (255, 255, 155))
        self.window.blit(score_surface, (10, 10))

        # Draw the player
        self.player.draw(self.window)

        # Draw asteroids
        self.asteroids_manager.draw(self.window)

        # Draw player lives icon
        if self.player.lives <= 0:
            self.game_over = True
            self.draw_game_over()
            return

        for i in range(self.player.lives):
            life_icon = pygame.transform.grayscale(
                (pygame.image.load("./assets/player.png"))
            )

            life_icon = pygame.transform.scale(life_icon, (20, 30))
            self.window.blit(life_icon, (10 + i * 35, 110))

    def update(self):
        self.draw()

        # Call entity update methods
        self.player.update()
        self.asteroids_manager.update()

    def handle_space_damage(self):
        if (
            self.player.x < 0 - 100
            or self.player.x > WINDOW_WIDTH + 100
            or self.player.y < 0 - 100
            or self.player.y > WINDOW_HEIGHT + 100
        ):
            self.player.take_damage()

    def run(self):
        while self.is_running:
            if not self.game_over:
                self.update()
            else:
                self.draw_game_over()

            self.handle_events()
            self.handle_input()
            self.handle_space_damage()

            pygame.display.flip()
            self.clock.tick(self.fps)
