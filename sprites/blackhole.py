import pygame
from random import randint
import assets.sounds as sounds

class Blackhole(pygame.sprite.Sprite):
    
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.SCREEN_WIDTH = game.SCREEN_WIDTH
        self.SCREEN_HEIGHT = game.SCREEN_HEIGHT
        self.player = game.player

        self.image = pygame.image.load("assets/images/backgrounds/blackhole.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = randint(self.rect.width, self.SCREEN_WIDTH - self.rect.width)
        self.rect.y = 0
        self.blocked = False
        self.collision = False
     
    def update(self):
        self.player_collision_check()
        self.death_check()

    def death_check(self):
        if self.rect.y > self.SCREEN_HEIGHT:
            self.kill()
            self.game.blackholes.add(Blackhole(self.game))
            del self
    
    def player_collision_check(self):
    
        if (self.rect.colliderect(self.game.player.rect) 
            and not self.collision 
            and not self.player.is_flying()):
            
            if self.player.using_shield:
                self.player.jump(play_sound=False)
                self.player.using_shield = False
                self.blocked = True
                self.collision = False
                sounds.block.play()
                
            elif not self.blocked:
                self.player.using_spring_shoes = False #When sucked into black whole they stick out of edge without being removed
                self.player.black_hole_collided_with = self
                self.player.paused = True
                self.player.blackhole_collision = True
                self.collision = True
                sounds.suck.play()
        else: 
            self.blocked = False
            


    def draw(self, screen):
        screen.blit(self.image, self.rect)