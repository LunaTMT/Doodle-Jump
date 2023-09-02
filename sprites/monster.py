import pygame
from pygame.locals import *
import assets.colours as colours
import assets.sounds as sounds


import random
from random import randint

class Monster(pygame.sprite.Sprite):


    SPRITE_SHEET = pygame.image.load("Doodle_Jump/assets/images/game-tiles.png")

    TERRIFIER = SPRITE_SHEET.subsurface(pygame.Rect(3, 421, 58, 86))  # Extract a 32x32 sprite
    FAT_GREEN = SPRITE_SHEET.subsurface(pygame.Rect(0, 359, 84, 53))  # Extract a 32x32 sprite
    BAT = SPRITE_SHEET.subsurface(pygame.Rect(148, 0, 77, 45))
    DOUBLE = SPRITE_SHEET.subsurface(pygame.Rect(63, 183, 80, 53))
    CUCUMBER = SPRITE_SHEET.subsurface(pygame.Rect(512, 425, 65, 85))
    BALL = SPRITE_SHEET.subsurface(pygame.Rect(149, 263, 46, 39))
    UGLY = SPRITE_SHEET.subsurface(pygame.Rect(514, 70, 87, 54))
    SAUSAGE = SPRITE_SHEET.subsurface(pygame.Rect(512, 3, 92, 31))

    


    def __init__(self, game):
        super().__init__()
        self.game = game
        self.player = game.player
        self.CENTER_X = game.CENTER_X
        self.CENTER_Y = game.CENTER_Y
        self.SCREEN_HEIGHT = game.SCREEN_HEIGHT
        self.SCREEN_WIDTH = game.SCREEN_WIDTH
        self.GRAVITY = game.GRAVITY
        self.JUMP_STRENGTH = game.JUMP_STRENGTH

        self.monsters = (self.TERRIFIER,
                         self.FAT_GREEN,
                         self.BAT,
                         self.DOUBLE,
                         self.CUCUMBER,
                         self.BALL,
                         self.UGLY,
                         self.SAUSAGE)
        
        self.image = random.choice(self.monsters)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(self.rect.width, self.SCREEN_WIDTH - self.rect.width)
        self.rect.y = 0

        self.mask = pygame.mask.from_surface(self.image)
        
   
        self.angle = 0 
        self.prior_speed = self.speed = random.randint(1,5)

        self.prior_speed_x = self.speed_x = random.randint(1,5)
        self.prior_speed_y = self.speed_y = random.randint(1,5)
        
        self.direction = 1
        self.direction_x = 1
        self.direction_y = 1

        self.radius = 100  # Circular path radius
        self.movements =  (self.ping_pong_ball,
                          self.up_down_movement,
                          self.side_to_side_movement)
        self.movement_function = random.choice(self.movements)
        
        self.sound = sounds.monster
        self.sound.play(-1)
        
        self.blocked = False
        self.collision = False
        
    def update(self):
        self.movement_function()
        self.boundary_check()
        self.killed_check()
        self.player_collision_check()

    def player_collision_check(self):
   
        if (self.rect.colliderect(self.game.player.rect) 
            and not self.collision 
            and not self.player.using_jetpack 
            and not self.player.using_propeller):
            
            if self.player.using_shield:
                self.player.using_shield = False
                self.player.jump(play_sound=False)
                self.blocked = True
                self.collision = False
                sounds.block.play()
            
            if not self.blocked:
                self.collision = True

                if self.player.falling:
                    self.player.jump()
                    self.sound.stop()
                    self.kill()
                    self.game.monsters.add(Monster(self.game))
                    del self

                else:
                    self.game.player.paused = True
                    self.game.player.knocked_out = True
                    self.game.player.velocity_y = -1
                    sounds.thump.set_volume(4)
                    sounds.thump.play()
       
        else: 
            self.blocked = False
        

    def killed_check(self):
        if pygame.sprite.spritecollide(self, self.game.bullets, True):
            random.choice((sounds.die_1, sounds.die_2)).play()
            self.sound.stop()
            self.kill()
            self.game.monsters.add(Monster(self.game))
            del self
            

    def boundary_check(self):
        if self.rect.y > self.SCREEN_HEIGHT:
            self.sound.stop()
            self.kill()
            self.game.monsters.add(Monster(self.game))
            
        
        
    def ping_pong_ball(self):
        self.rect.x += self.speed_x * self.direction_x
        self.rect.y += self.speed_y * self.direction_y
        
        if self.rect.right > self.SCREEN_WIDTH or self.rect.left < 0:
            self.direction_x *= -1
        if self.rect.bottom > self.SCREEN_HEIGHT or self.rect.top < 0:
            self.direction_y *= -1

    def up_down_movement(self):
        self.rect.y += self.speed * self.direction
        if self.rect.bottom > self.SCREEN_HEIGHT or self.rect.top < 0:
            self.direction *= -1
        
    def side_to_side_movement(self):
        self.rect.x += self.speed * self.direction
        if self.rect.right > self.SCREEN_WIDTH or self.rect.left < 0:
            self.direction *= -1


    def draw(self, screen):
        screen.blit(self.image, self.rect)
        
        
