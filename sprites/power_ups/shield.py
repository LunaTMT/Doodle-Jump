import pygame

class Shield(pygame.sprite.Sprite):

    SPRITE_SHEET = pygame.image.load("Doodle_Jump/assets/images/game-tiles.png")
    DEFAULT_IMAGE = SPRITE_SHEET.subsurface(pygame.Rect(235, 306, 34, 34))  # Extract a 32x32 sprite
    
    def __init__(self, game, tile, x, y):
        super().__init__()
        self.game = game
        self.tile = tile
        self.SCREEN_HEIGHT = game.SCREEN_HEIGHT
        self.SCREEN_WIDTH = game.SCREEN_WIDTH
        
        self.CENTER_X = game.CENTER_X
        self.player = game.player

        self.x = x
        self.y = y - 30
        self.image = self.DEFAULT_IMAGE 
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.center = (self.x, self.y)
        self.being_used = False

    def update(self):
        self.death_check()
        self.player_collision_check()

    def player_collision_check(self):
        collision = pygame.sprite.collide_rect(self.player, self)
        if collision and not self.player.knocked_out:
            self.player.using_shield = True
            self.being_used = True

    def death_check(self):
        if (self.rect.y > self.SCREEN_HEIGHT) or self.being_used:
            self.kill()
            self.tile.power_up = None

    def draw(self, screen):
        if not self.being_used:
            screen.blit(self.image, self.rect)