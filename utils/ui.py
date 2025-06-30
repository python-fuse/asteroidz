import pygame

pygame.font.init()

ui_font = pygame.font.SysFont("Fira code", 30)


class Button:
    def __init__(
        self,
        text,
        x,
        y,
        width,
        height,
        font,
        color=(255, 255, 255),
        action=lambda: None,
    ):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.font = font
        self.color = color
        self.action = action

    def draw(self, surface):
        pygame.draw.rect(surface, (0, 0, 0, 0), self.rect, border_radius=5)
        text_surface = ui_font.render(self.text, True, (0, 255, 0))
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

    def handle_click(self):
        if callable(self.action):
            self.action()
        else:
            raise ValueError("Action must be a callable function.")
