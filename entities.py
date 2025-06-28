import math
import pygame


class Entity:
    def __init__(self, x: int, y: int, width: int, height: int, sprite: str) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.sprite = sprite
        self.collision_rect = pygame.Rect(x, y, width, height)
        self.debug_mode = False  # Flag for debug mode

    def __repr__(self) -> str:
        return f"Entity(x={self.x}, y={self.y}, width={self.width}, height={self.height}, sprite='{self.sprite}')"

    def draw(self, screen: pygame.Surface) -> None:
        # Placeholder for drawing logic
        # Override this method in subclasses to implement actual drawing
        print(
            f"Drawing {self.sprite} at ({self.x}, {self.y}) with size ({self.width}, {self.height}) on screen {screen.get_size()}"
        )

    def update(self) -> None:
        # Placeholder for update logic
        # Override this method in subclasses to implement actual update behavior
        self.collision_rect.topleft = (self.x, self.y)

    def check_collision(self, other: "Entity") -> bool:
        """Check if this entity collides with another entity."""
        collision = self.collision_rect.colliderect(other.collision_rect)
        if collision:
            print(f"Collision detected between {self.sprite} and {other.sprite}")
        return collision


class Player(Entity):
    def __init__(self, x: int, y: int, width: int, height: int, sprite: str) -> None:
        super().__init__(x, y, width, height, sprite)
        self.health = 100
        self.speed = 5
        self.direction = 0
        self.momentum_x = 0
        self.momentum_y = 0
        self.acceleration = 0.2

    def update(self) -> None:
        # Additional player-specific update logic can go here
        self.x += self.momentum_x
        self.y += self.momentum_y

        self.momentum_x *= 0.99
        self.momentum_y *= 0.99

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the player on the screen."""

        # Center the sprite on its position
        sprite_image = pygame.image.load(self.sprite)
        sprite_image = pygame.transform.scale(sprite_image, (self.width, self.height))
        rotated_image = pygame.transform.rotate(sprite_image, self.direction)
        rotated_rect = rotated_image.get_rect(
            center=(self.x + self.width // 2, self.y + self.height // 2)
        )

        # Set the collision rectangle to the rotated position
        self.collision_rect = rotated_rect

        # Show the collision rectangle in debug mode
        if self.debug_mode:
            pygame.draw.rect(screen, (255, 0, 0), self.collision_rect, 1)

        # Draw the rotated sprite on the screen
        screen.blit(rotated_image, rotated_rect.topleft)

    def handle_input(self, keys: pygame.key.ScancodeWrapper) -> None:
        """Handle player input for movement and actions."""
        if keys[pygame.K_LEFT]:
            self.direction += self.speed
        if keys[pygame.K_RIGHT]:
            self.direction -= self.speed

        # Accelerate in the direction the player is facing
        if keys[pygame.K_UP]:
            angle_rad = math.radians(self.direction + 90)
            self.momentum_x += self.acceleration * math.cos(angle_rad)
            self.momentum_y -= self.acceleration * math.sin(angle_rad)

    def take_damage(self, amount: int) -> None:
        """Reduce player health by the specified amount."""
        self.health -= amount
        if self.health < 0:
            self.health = 0
        print(f"{self.sprite} took {amount} damage, health is now {self.health}")

    def __repr__(self) -> str:
        return f"Player(x={self.x}, y={self.y}, width={self.width}, height={self.height}, sprite='{self.sprite}', health={self.health})"
