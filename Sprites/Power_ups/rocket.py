import pygame
import Assets.sounds as sounds

import texture


class Jetpack(pygame.sprite.Sprite):
    id = 0 

    SPRITE_SHEET = pygame.image.load(f"Assets/Images/Animations/Jetpack/{texture.file_name}.png")
    
    ROCKET_1 = SPRITE_SHEET.subsurface(pygame.Rect(0, 0, 32, 62))  
    ROCKET_2 = SPRITE_SHEET.subsurface(pygame.Rect(32, 0, 32, 62))  
    ROCKET_3 = SPRITE_SHEET.subsurface(pygame.Rect(64, 0, 32, 62))  
    ROCKET_4 = SPRITE_SHEET.subsurface(pygame.Rect(96, 0, 32, 62))  
    
    ROCKET_5 = SPRITE_SHEET.subsurface(pygame.Rect(0, 64, 32, 62))  
    ROCKET_6 = SPRITE_SHEET.subsurface(pygame.Rect(32, 64, 32, 62)) 
    ROCKET_7 = SPRITE_SHEET.subsurface(pygame.Rect(64, 64, 32, 62))  
    ROCKET_8 = SPRITE_SHEET.subsurface(pygame.Rect(96, 64, 32, 62)) 
    
    ROCKET_9 = SPRITE_SHEET.subsurface(pygame.Rect(0, 128, 32, 62))  
    DEFAULT_ROCKET = SPRITE_SHEET.subsurface(pygame.Rect(32, 128, 32, 62))  

    START_ANIMATION = [ROCKET_1, ROCKET_2, ROCKET_3]                #  0  -  16 frames
    MAIN_BLAST = [ROCKET_4, ROCKET_5, ROCKET_6]                     # 16  - 147 frames
    END_ANIMAITON = [ROCKET_7, ROCKET_8, ROCKET_9]  # 147 - 163 frames

   

    def __init__(self, game, tile, x, y):
        super().__init__()
        self.game = game
        self.SCREEN_HEIGHT = game.SCREEN_HEIGHT
        self.SCREEN_WIDTH = game.SCREEN_WIDTH
        
        self.CENTER_X = game.CENTER_X
        self.player = game.player


        self.x = x
        self.y = y - 10
        self.image = self.DEFAULT_ROCKET 
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.center = (self.x, self.y)
        self.being_used = False


    def update(self):
        self.death_check()
        self.player_collision_check()


    def player_collision_check(self):
        collision = self.rect.colliderect(self.game.player.rect)
        if (collision 
            and not self.player.dead 
            and not self.player.is_flying()):

            self.player.JUMP_STRENGTH = -65
            self.player.jump(play_sound=False)
            self.player.JUMP_STRENGTH = -23 if self.player.using_spring_shoes else -15
            self.player.using_jetpack = True
            
            self.being_used = True
            sounds.jetpack.play()


    def death_check(self):
        if self.rect.y > self.SCREEN_HEIGHT:
            self.kill()

    def draw(self, screen):
        self.image.set_alpha(self.game.fade_out_alpha)    
        screen.blit(self.image, self.rect)

