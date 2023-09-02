import pygame

class MenuButton:
    SPRITE_SHEET = pygame.image.load("assets/images/start-end-tiles.png")
    DEFAULT_IMAGE = SPRITE_SHEET.subsurface(pygame.Rect(1, 49, 112, 41))
