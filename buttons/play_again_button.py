import pygame

class PlayAgain:
    SPRITE_SHEET = pygame.image.load("assets/images/start-end-tiles.png")
    DEFAULT_IMAGE = SPRITE_SHEET.subsurface(pygame.Rect(115, 49, 112, 41))