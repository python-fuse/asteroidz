import pygame


class Entity:
    def __init__(self, x: int, y: int, width: int, height: int, sprite: str) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.sprite = sprite
        self.collision_rect = pygame.Rect(x, y, width, height)

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
        print(f"Updating {self.sprite}")

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

    def __repr__(self) -> str:
        return f"Player(x={self.x}, y={self.y}, width={self.width}, height={self.height}, sprite='{self.sprite}', health={self.health})"

    def update(self) -> None:
        # Additional player-specific update logic can go here
        pass

    def draw(self, screen: pygame.Surface) -> None:
        sprite_surface = pygame.image.load(self.sprite)
        sprite_surface = pygame.transform.scale(
            sprite_surface, (self.width, self.height)
        )
        screen.blit(sprite_surface, (self.x, self.y))

    def handle_input(self, keys: pygame.key.ScancodeWrapper) -> None:
        """Handle player input for movement and actions."""
        if keys[pygame.K_LEFT]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.x += self.speed
        if keys[pygame.K_UP]:
            self.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.y += self.speed

        # Update the collision rectangle position
        self.collision_rect.topleft = (self.x, self.y)

    def take_damage(self, amount: int) -> None:
        """Reduce player health by the specified amount."""
        self.health -= amount
        if self.health < 0:
            self.health = 0
        print(f"{self.sprite} took {amount} damage, health is now {self.health}")


class Enemy(Entity):
    def __init__(self, x: int, y: int, width: int, height: int, sprite: str) -> None:
        super().__init__(x, y, width, height, sprite)
        self.damage = 10

    def __repr__(self) -> str:
        return f"Enemy(x={self.x}, y={self.y}, width={self.width}, height={self.height}, sprite='{self.sprite}', damage={self.damage})"

    def update(self) -> None:
        # Additional enemy-specific update logic can go here
        pass

    def draw(self, screen: pygame.Surface) -> None:
        # Additional enemy-specific drawing logic can go here
        pass


class Bullet(Entity):
    def __init__(
        self, x: int, y: int, width: int, height: int, sprite: str, speed: int
    ) -> None:
        super().__init__(x, y, width, height, sprite)
        self.speed = speed

    def __repr__(self) -> str:
        return f"Bullet(x={self.x}, y={self.y}, width={self.width}, height={self.height}, sprite='{self.sprite}', speed={self.speed})"

    def update(self) -> None:
        # Move the bullet in a specific direction
        self.x += self.speed
        self.collision_rect.topleft = (self.x, self.y)
        print(f"Bullet moved to ({self.x}, {self.y}) with speed {self.speed}")

    def draw(self, screen: pygame.Surface) -> None:
        pass
