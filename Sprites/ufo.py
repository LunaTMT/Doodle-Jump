import pygame
import random
import Assets.sounds as sounds
import Assets.colours as colours
import texture
from math import sin, radians


class UFO(pygame.sprite.Sprite):
    
    SPRITE_SHEET = pygame.image.load(f"Assets/Images/Game_tiles/{texture.file_name}.png")

    DEFAULT = SPRITE_SHEET.subsurface(pygame.Rect(428, 208, 84, 122))  # Extract a 32x32 sprite
    COLLISION_IMAGE = SPRITE_SHEET.subsurface(pygame.Rect(428, 83, 84, 122))  # Extract a 32x32 sprite
    

    def __init__(self, game):
        super().__init__()
        self.game = game
        self.SCREEN_WIDTH = game.SCREEN_WIDTH
        self.SCREEN_HEIGHT = game.SCREEN_HEIGHT
        self.player = game.player
        self.fade_out_alpha = game.fade_out_alpha

        self.paused = False

        self.alpha = 255
        self.image = self.DEFAULT
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(self.rect.width, self.SCREEN_WIDTH - self.rect.width)
        self.rect.y = -self.rect.height
        self.blocked = False
        self.collision = False
        self.angle = 0
        self.sound = sounds.ufo
        self.sound.set_volume(2)
        self.sound.play(-1)
        
        
    @classmethod
    def update_images(cls):
        cls.SPRITE_SHEET = pygame.image.load(f"Assets/Images/Game_tiles/{texture.file_name}.png")
        cls.DEFAULT = cls.SPRITE_SHEET.subsurface(pygame.Rect(428, 208, 84, 122))  # Extract a 32x32 sprite
        cls.COLLISION_IMAGE = cls.SPRITE_SHEET.subsurface(pygame.Rect(428, 83, 84, 122))  # Extract a 32x32 sprite
    
    def update(self):
        self.movement_update()
        self.player_collision_check()
        self.death_check()
        self.killed_check()
        self.fade_check()

    def fade_check(self):
        if self.game.end_game and self.player.dead_by_blackhole:
            self.alpha = self.game.fade_out_alpha

    def death_check(self):
        if self.rect.y > self.SCREEN_HEIGHT:
            self.kill()
            del self
    
    def player_collision_check(self):
    
        if (self.rect.colliderect(self.game.player.rect) 
            and not self.collision 
            and not self.player.is_flying()
            and not self.player.dead):
            
            if self.player.using_shield:
                self.player.jump(play_sound=False)
                self.player.using_shield = False
                self.blocked = True
                self.collision = False
                sounds.block.play()
            
            
            elif not self.blocked:
                
                if self.player.falling:
                    self.player.jump(play_sound=False)                    
                    self.remove()
                else:
            
                    self.player.using_spring_shoes = False #When sucked into black whole they stick out of edge without being removed
                    self.player.black_hole_collided_with = self
                    self.player.blackhole_collision = True
                    self.player.dead_by_blackhole = True
                    self.player.paused = True
                    self.player.dead = True
                    self.collision = True
                    self.game.end_game = True

                    sounds.ufo_suck.play()

        else: 
            self.blocked = False

    def killed_check(self):
        if pygame.sprite.spritecollide(self, self.game.bullets, True):
            self.remove()

    def remove(self):
        sounds.tile_disappear.play()
        self.sound.stop()
        self.kill()   
        del self
            
    def draw(self, screen):
        
        if self.alpha < 0: 
            self.alpha = 0
        else:
            self.image.set_alpha(self.alpha)
        screen.blit(self.image, self.rect)


    

    def movement_update(self):
        if not self.paused:
            # Update the sprite's x-coordinate based on the figure 8 motion
            self.angle += 1  # Adjust this value to control the speed of the motion
            x = self.SCREEN_WIDTH // 2 + 100 * sin(radians(self.angle))
            self.rect.centerx = x