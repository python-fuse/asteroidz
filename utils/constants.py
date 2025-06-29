from os import path
import pygame

pygame.mixer.init()

WINDOW_HEIGHT = 800
WINDOW_WIDTH = 1000


EXPLOSION_SOUND = pygame.mixer.Sound("assets/enemy_explode.wav")
SHOOT_SOUND = pygame.mixer.Sound("assets/shoot.mp3")


ASTEROID_SCORE_UP_EVENT = pygame.event.Event(pygame.USEREVENT + 1)
