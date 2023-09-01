import pygame

class SpringShoes(pygame.sprite.Sprite):

    SPRITE_SHEET = pygame.image.load("Doodle_Jump/assets/images/game-tiles.png")
    SPRING = SPRITE_SHEET.subsurface(pygame.Rect(17, 12, 404, 99))  # Extract a 32x32 sprite
    SPRING_EXPANDED = SPRITE_SHEET.subsurface(pygame.Rect(17, 28, 404, 115))


    def __init__(self, game, x, y):
        super().__init__()
        self.game = game
        self.SCREEN_HEIGHT = game.SCREEN_HEIGHT
        self.SCREEN_WIDTH = game.SCREEN_WIDTH
        
        self.CENTER_X = game.CENTER_X
        self.player = game.player

        self.x = x
        self.y = y
        self.image = self.SPRING 
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.center = (self.x, self.y)

    def update(self):
        self.death_check()
        self.player_collision_check()

    def player_collision_check(self):
        collision = pygame.sprite.collide_rect(self.player, self)
        if collision and self.player.falling and not self.player.paused:
            self.player.spring_jump()

    def death_check(self):
        if self.rect.y > self.SCREEN_HEIGHT:
            self.kill()

    def draw(self, screen):
        screen.blit(self.image, self.rect)