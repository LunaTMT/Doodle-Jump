import pygame

class Tile(pygame.sprite.Sprite):

    SPRITE_SHEET = pygame.image.load("Doodle_Jump/assets/images/game-tiles.png")
    DEFAULT_IMAGE = SPRITE_SHEET.subsurface(pygame.Rect(0, 0, 58, 18))  # Extract a 32x32 sprite


    def __init__(self, game, x, y):
        super().__init__()
        self.game = game
        self.SCREEN_HEIGHT = game.SCREEN_HEIGHT

        self.x = x
        self.y = y
        self.image = self.DEFAULT_IMAGE
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.center = (self.x, self.y)

    def update(self):
        if self.rect.y > self.SCREEN_HEIGHT:
            self.game.generate_tiles(1, top=True)
            self.kill()

    def draw(self, screen):
        screen.blit(self.image, self.rect)