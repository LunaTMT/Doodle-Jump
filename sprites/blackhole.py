import pygame
from random import randint
import assets.sounds as sounds

class Blackhole(pygame.sprite.Sprite):
    
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.SCREEN_WIDTH = game.SCREEN_WIDTH
        self.player = game.player

        self.image = pygame.image.load("Doodle_Jump/assets/images/backgrounds/blackhole.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = randint(self.rect.width, self.SCREEN_WIDTH - self.rect.width)
        self.rect.y = 0
        self.collision = False

    def update(self):
        self.player_collision_check()


    def player_collision_check(self):
        if self.rect.colliderect(self.game.player.rect) and not self.collision:
            self.player.paused = True
            self.player.blackhole_collision = True
            self.collision = True
            sounds.suck.play()
            


    def draw(self, screen):
        screen.blit(self.image, self.rect)