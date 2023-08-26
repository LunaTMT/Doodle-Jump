import pygame
import sys
import assets.colours as colours
import assets.sounds as sounds
from random import choice, randint
from player import Player
from tile import Tile

class Game:

    SCREEN_WIDTH = 640
    SCREEN_HEIGHT = 900
    CENTER_X = SCREEN_WIDTH // 2
    CENTER_Y = SCREEN_HEIGHT // 2
    GRAVITY = 0.4 # Adjust gravity strength
    JUMP_STRENGTH = -15  # Adjust jump strength


    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Doodle Jump")
    clock = pygame.time.Clock()

    all_sprites = pygame.sprite.Group()
    platforms = pygame.sprite.Group()
    bullets = pygame.sprite.Group()


    def __init__(self):
        self.running = True
        self.background_image = pygame.image.load("Doodle_Jump/assets/images/background.png")
        self.player = Player(self, self.CENTER_X, self.CENTER_Y)
        self.all_sprites.add(self.player)
        self.generate_tiles(20)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            self.player.handle_events(event)

        self.player.handle_events()
        
        collisions = pygame.sprite.spritecollide(self.player, self.platforms, False, pygame.sprite.collide_mask)
        if collisions and self.player.falling:
            self.player.jump()


    def update(self):
        self.bullets.update()

        for platform in self.platforms.sprites():
            platform.update()

        self.player.update()
        

    def draw(self):
        self.screen.fill(colours.WHITE)
        self.screen.blit(self.background_image, (0, 0))
        
        self.bullets.draw(self.screen)
        self.platforms.draw(self.screen)
        self.player.draw(self.screen)

        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()

    def generate_tiles(self, n, top=False):
        
        for _ in range(n):
            
            x, y = randint(58, self.SCREEN_WIDTH - 58), (0 if top else randint(0, self.SCREEN_HEIGHT))
            new_platform_rect = pygame.Rect(x, y, 58, 18)

            while any(new_platform_rect.colliderect(platform) for platform in self.platforms.sprites()):
                x, y = randint(58, self.SCREEN_WIDTH - 58), (0 if top else randint(0, self.SCREEN_HEIGHT))
                new_platform_rect = pygame.Rect(x, y, 58, 18)
            
            platform = Tile(self, x, y)
            self.all_sprites.add(platform)
            self.platforms.add(platform)

class Platforms(pygame.sprite.Group):
    def update(self):
        # Custom update logic for the entire group
        for platform in self.sprites():
            platform.update()





