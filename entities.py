import math
import random
import pygame

from utils.constants import (
    EXPLOSION_SOUND,
    ASTEROID_SCORE_UP_EVENT,
    SHOOT_SOUND,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
)


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


class Bullet(Entity):
    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        sprite: str,
        direction: int = 0,
    ) -> None:
        super().__init__(x, y, width, height, sprite)
        self.direction = direction
        self.speed = 10
        self.lifetime = 100
        self.debug_mode = False

    def update(self) -> None:
        """Update the bullet's position based on its speed and direction."""
        angle_rad = math.radians(self.direction)
        self.x += self.speed * math.cos(angle_rad)
        self.y -= self.speed * math.sin(angle_rad)
        self.collision_rect.topleft = (int(self.x), int(self.y))

        # Decrease lifetime
        self.lifetime -= 1

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the bullet on the screen."""
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

    def is_dead(self):
        if self.lifetime < 1:
            return True
        else:
            return False

    def __repr__(self) -> str:
        return f"Bullet(x={self.x}, y={self.y}, width={self.width}, height={self.height}, sprite='{self.sprite}', direction={self.direction})"


class BulletsManager:
    def __init__(self) -> None:
        self.bullets: list[Bullet] = []

    def draw(self, surface: pygame.Surface):
        for bullet in self.bullets:
            bullet.draw(surface)

    def delete(self, bullet: Bullet):
        """Remove a bullet from the list."""
        if bullet in self.bullets:
            self.bullets.remove(bullet)

    def update(self):
        for bullet in self.bullets:
            bullet.update()

        for bullet in self.bullets:
            if bullet.is_dead():
                self.delete(bullet)

    def shoot(self, x, y, width, height, sprite, direction=0):
        self.bullets.append(Bullet(x, y, width, height, sprite, direction))

    def get_bullets(self):
        return self.bullets


class Player(Entity):
    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        sprite: str,
        bullet_manager: BulletsManager,
        debug_mode: bool = False,
    ) -> None:
        super().__init__(x, y, width, height, sprite)
        self.lives = 3
        self.rotation_speed = 4
        self.direction = 0
        self.momentum_x = 0
        self.momentum_y = 0
        self.acceleration = 0.1
        self.debug_mode = debug_mode

        # Player surface
        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        # Cooldown for shooting
        self.shoot_cooldown = 0
        self.shoot_delay = 10

        # Bullet manager
        self.bullet_manager = bullet_manager

        # Invincibility timer
        self.invincibility_duration = 60 * 3
        self.invincibility_timer = 0
        self.is_invincible = False

        # Blink logic
        self.blink_timer = 0
        self.blink_interval = 5
        self.blink_visible = True

    def update(self) -> None:
        """Update the player's position and handle movement."""
        if self.invincibility_timer > 0:
            self.invincibility_timer -= 1
            self.blink_timer += 1

            if self.blink_timer >= self.blink_interval:
                self.blink_timer = 0
                self.blink_visible = not self.blink_visible

            if self.invincibility_timer <= 0:
                self.is_invincible = False
                self.blink_visible = True

        self.x += self.momentum_x
        self.y += self.momentum_y

        self.momentum_x *= 0.99
        self.momentum_y *= 0.99

        # Update the collision rectangle
        self.collision_rect.topleft = (int(self.x), int(self.y))

        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

        # bullet manager update
        self.bullet_manager.update()

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the player on the screen."""

        # Center the sprite on its position
        sprite_image = pygame.image.load(self.sprite)
        sprite_image = pygame.transform.scale(sprite_image, (self.width, self.height))
        self.surface = pygame.transform.rotate(sprite_image, self.direction)
        rotated_rect = self.surface.get_rect(
            center=(self.x + self.width // 2, self.y + self.height // 2)
        )

        # Set the collision rectangle to the rotated position
        self.collision_rect = rotated_rect

        # Show the collision rectangle in debug mode
        if self.debug_mode:
            pygame.draw.rect(screen, (255, 0, 0), self.collision_rect, 1)

        # Draw the rotated sprite on the screen
        if not self.is_invincible or self.blink_visible:
            screen.blit(self.surface, rotated_rect.topleft)

        # Bullet manager draw
        self.bullet_manager.draw(screen)

    def handle_input(self, keys: pygame.key.ScancodeWrapper) -> None:
        """Handle player input for movement and actions."""
        if keys[pygame.K_LEFT]:
            self.direction += self.rotation_speed
        if keys[pygame.K_RIGHT]:
            self.direction -= self.rotation_speed

        # Accelerate in the direction the player is facing
        if keys[pygame.K_UP]:
            max_speed = 10
            if self.momentum_x**2 + self.momentum_y**2 < max_speed**2:
                angle_rad = math.radians(self.direction + 90)
                self.momentum_x += self.acceleration * math.cos(angle_rad)
                self.momentum_y -= self.acceleration * math.sin(angle_rad)

        if keys[pygame.K_SPACE]:
            self.shoot()

    def shoot(self):
        if self.shoot_cooldown > 0:
            return

        # shoot from the center of the player in x and tip of the player in y
        self.bullet_manager.shoot(
            self.x + self.width // 2,
            self.y + self.height // 2,
            5,
            5,
            "./assets/bullet_player.png",
            direction=self.direction + 90,
        )

        SHOOT_SOUND.play()

        self.shoot_cooldown = self.shoot_delay

    def reset_position(self) -> None:
        self.x = WINDOW_HEIGHT // 2
        self.y = WINDOW_HEIGHT // 2

        self.momentum_x = 0
        self.momentum_y = 0
        self.direction = 0

    def take_damage(self) -> None:
        """Check player's lives and take action"""
        if self.lives < 1:
            print("Dead")
        else:
            # Reset player position to the center of the screen
            if self.is_invincible:
                return

            self.lives -= 1
            self.reset_position()
            # Set invincibility timer
            self.invincibility_timer = self.invincibility_duration

        self.is_invincible = True
        self.invincibility_timer = self.invincibility_duration
        self.blink_visible = True
        self.blink_timer = 0

    def __repr__(self) -> str:
        return f"Player(x={self.x}, y={self.y}, width={self.width}, height={self.height}, sprite='{self.sprite}', health={self.lives})"


class Asteroid(Entity):
    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        sprite: str,
        direction: int,
        debug=False,
        type="normal",
    ) -> None:
        super().__init__(x, y, width, height, sprite)
        self.speed = 2
        self.direction = math.radians(direction)
        self.debug_mode = debug
        self.exploded = False
        self.explosion_timer = 10
        self.type = type

    def move(self):

        # same speed but in the direction of the angle
        self.x += self.speed * math.cos(self.direction)
        self.y -= self.speed * math.sin(self.direction)

        # Update the collision rectangle position
        self.collision_rect.width = self.width
        self.collision_rect.height = self.height
        # Update the collision rectangle position to match the entity's position
        # This ensures that the collision rectangle is always in sync with the entity's position
        self.collision_rect.topleft = (int(self.x), int(self.y))

    def update(self) -> None:
        self.move()

    def explode(self):
        self.exploded = True

    def draw(self, screen: pygame.Surface) -> None:
        sprite_to_render = (
            self.sprite if self.exploded == False else "assets/explosion.png"
        )

        sprite_image = pygame.transform.scale(
            pygame.image.load(sprite_to_render), (self.width, self.height)
        )

        if self.debug_mode:
            pygame.draw.rect(screen, (255, 0, 0), self.collision_rect)

        screen.blit(sprite_image, (self.x, self.y))

    def check_collision(self, other: Entity) -> bool:
        """Check if this asteroid collides with another entity."""
        collision = self.collision_rect.colliderect(other.collision_rect)
        return collision

    def __repr__(self) -> str:
        return f"Asteroid(x={self.x}, y={self.y}, width={self.width}, height={self.height}, sprite='{self.sprite}')"


class AsteroidManager:
    def __init__(self, bullets_manager: BulletsManager, player: Player) -> None:
        self.asteroids: list[Asteroid] = []
        self.bullets = bullets_manager.get_bullets()
        self.player = player

    def draw(self, surface: pygame.Surface):
        for bullet in self.asteroids:
            bullet.draw(surface)

    def delete(self, asteroid: Asteroid):
        try:
            self.asteroids.remove(asteroid)
        except ValueError:
            print(f"Asteroid {asteroid} not found in the list.")

    def update(self):
        for asteroid in self.asteroids:
            asteroid.update()
            if (
                asteroid.x < 0 - asteroid.width
                or asteroid.x > WINDOW_WIDTH
                or asteroid.y < 0 - asteroid.height
                or asteroid.y > WINDOW_HEIGHT
            ):
                self.destroy(asteroid)
            if asteroid.exploded:
                asteroid.explosion_timer -= 1
                if asteroid.explosion_timer < 1:
                    self.destroy(asteroid)

        for bullet in self.bullets:
            self.check_collisions(bullet)

        self.check_collisions(self.player)

    def destroy(self, asteroid: Asteroid):
        """Remove an asteroid from the list."""
        if asteroid in self.asteroids:
            self.asteroids.remove(asteroid)

    def spawn(self, player: Player):
        """Spawn a new asteroid at a random position."""

        rand_x = random.randint(0, WINDOW_WIDTH - 20)
        rand_y = random.randint(0, WINDOW_HEIGHT - 20)
        rand_direction = random.randint(0, 360)

        # Spawn a new asteroid at a random position
        # Ensure it does not spawn on the player
        while abs(rand_x - player.x) < 50 and abs(rand_y - player.y) < 50:
            rand_x = random.randint(0, WINDOW_WIDTH - 20)
            rand_y = random.randint(0, WINDOW_HEIGHT - 20)

        self.asteroids.append(
            Asteroid(rand_x, rand_y, 70, 70, "./assets/asteroid1.png", rand_direction)
        )

    def get_asteroids(self):
        return self.asteroids

    def check_collisions(self, entity: Entity) -> None:
        """Check for collisions with the given entity and return a list of colliding asteroids."""
        for asteroid in self.asteroids:
            if asteroid.check_collision(entity):
                if isinstance(entity, Bullet):
                    EXPLOSION_SOUND.play()
                    asteroid.explode()
                    entity.lifetime = 0

                    if asteroid.type == "normal":
                        self.asteroids.extend(
                            [
                                Asteroid(
                                    asteroid.x,
                                    asteroid.y,
                                    30,
                                    30,
                                    "./assets/asteroid2.png",
                                    random.randint(0, 360),
                                    type="small",
                                ),
                                Asteroid(
                                    asteroid.x,
                                    asteroid.y,
                                    30,
                                    30,
                                    "./assets/asteroid2.png",
                                    random.randint(0, 360),
                                    type="small",
                                ),
                            ]
                        )

                    pygame.event.post(ASTEROID_SCORE_UP_EVENT)

                if isinstance(entity, Player):
                    entity.take_damage()

    def __repr__(self) -> str:
        return f"AsteroidManager(asteroids={self.asteroids})"


# class Enemy(Entity):
#     def __init__(
#         self,
#         x: int,
#         y: int,
#         width: int,
#         height: int,
#         sprite: str,
#         speed: int = 2,
#     ) -> None:
#         super().__init__(x, y, width, height, sprite)
#         self.speed = speed
#         self.direction = random.randint(0, 360)

#         self.bullet_manager = BulletsManager()
#         self.collision_rect = pygame.Rect(x, y, width, height)
#         self.debug_mode = False  # Flag for debug mode

#         self.life = 1

#     def update(self) -> None:
#         """Update the enemy's position based on its speed and direction."""
#         angle_rad = math.radians(self.direction)
#         self.x += self.speed * math.cos(angle_rad)
#         self.y -= self.speed * math.sin(angle_rad)
#         self.collision_rect.topleft = (int(self.x), int(self.y))

#     def draw(self, screen: pygame.Surface) -> None:
#         """Draw the enemy on the screen."""
#         sprite_image = pygame.image.load(self.sprite)
#         sprite_image = pygame.transform.scale(sprite_image, (self.width, self.height))
#         rotated_image = pygame.transform.rotate(sprite_image, self.direction)
#         rotated_rect = rotated_image.get_rect(
#             center=(self.x + self.width // 2, self.y + self.height // 2)
#         )

#         # Set the collision rectangle to the rotated position
#         self.collision_rect = rotated_rect

#         # Draw the rotated sprite on the screen
#         screen.blit(rotated_image, rotated_rect.topleft)

#     def shoot_at_player(self, player: Player) -> None:
#         """Shoot a bullet at the player."""
#         if random.random() < 0.01:
#             direction_to_player = math.degrees(
#                 math.atan2(player.y - self.y, player.x - self.x)
#             )
#             self.bullet_manager.shoot(
#                 self.x + self.width // 2,
#                 self.y + self.height // 2,
#                 5,
#                 5,
#                 "./assets/bullet_enemy.png",
#                 direction=int(direction_to_player),
#             )
#             SHOOT_SOUND.play()

#     def check_collision(self, other: Entity) -> bool:
#         return super().check_collision(other)

#     def take_damage(self, bullet: Bullet) -> None:
#         """Handle damage taken by the enemy."""
#         if self.check_collision(bullet):
#             if isinstance(bullet, Bullet):
#                 self.life = 0

#     def __repr__(self) -> str:
#         return f"Enemy(x={self.x}, y={self.y}, width={self.width}, height={self.height}, sprite='{self.sprite}', speed={self.speed})"


# class EnemyManager:
#     def __init__(self, player: Player) -> None:
#         self.enemies: list[Enemy] = []
#         self.player = player

#     def draw(self, surface: pygame.Surface):
#         for enemy in self.enemies:
#             enemy.draw(surface)

#     def update(self):
#         for enemy in self.enemies:
#             enemy.update()
#             enemy.shoot_at_player(self.player)

#             if enemy.life < 1:
#                 self.enemies.remove(enemy)

#         # Remove enemies that are out of bounds
#         self.enemies = [
#             enemy
#             for enemy in self.enemies
#             if 0 <= enemy.x <= WINDOW_WIDTH and 0 <= enemy.y <= WINDOW_HEIGHT
#         ]

#     def spawn(self):
#         """Spawn a new enemy at the specified position."""
#         rand_x = random.randint(0, WINDOW_WIDTH - 20)
#         rand_y = random.randint(0, WINDOW_HEIGHT - 20)
#         rand_direction = random.randint(0, 360)

#         self.enemies.append(Enemy(rand_x, rand_y, 50, 70, "assets/enemy1.png"))

#     def __repr__(self) -> str:
#         return f"EnemyManager(enemies={self.enemies})"
