import pygame
import Assets.sounds as sounds


import texture

class Propeller(pygame.sprite.Sprite):
    id = 0 

    SPRITE_SHEET = pygame.image.load(f"Assets/Images/Animations/Propeller/{texture.file_name}.png")
    
    PROPELLER_1 = SPRITE_SHEET.subsurface(pygame.Rect(0, 0, 32, 32))  
    PROPELLER_2 = SPRITE_SHEET.subsurface(pygame.Rect(32, 0, 32, 32))  
    PROPELLER_3 = SPRITE_SHEET.subsurface(pygame.Rect(0, 32, 32, 32))  
    PROPELLER_4 = SPRITE_SHEET.subsurface(pygame.Rect(32, 0, 32, 32))  
    PROPELLERS = [PROPELLER_1, PROPELLER_2, PROPELLER_3, PROPELLER_4]

    def __init__(self, game, tile, x, y):
        super().__init__()
        self.game = game
        self.SCREEN_HEIGHT = game.SCREEN_HEIGHT
        self.SCREEN_WIDTH = game.SCREEN_WIDTH
        
        self.CENTER_X = game.CENTER_X
        self.player = game.player

        self.alpha = 255
        self.x = x
        self.y = y - 15
        self.image = self.PROPELLER_1 
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.center = (self.x, self.y)
        self.being_used = False

    @classmethod
    def update_images(cls):
        cls.SPRITE_SHEET = pygame.image.load(f"Assets/Images/Animations/Propeller/{texture.file_name}.png")
    
        cls.PROPELLER_1 = cls.SPRITE_SHEET.subsurface(pygame.Rect(0, 0, 32, 32))  
        cls.PROPELLER_2 = cls.SPRITE_SHEET.subsurface(pygame.Rect(32, 0, 32, 32))  
        cls.PROPELLER_3 = cls.SPRITE_SHEET.subsurface(pygame.Rect(0, 32, 32, 32))  
        cls.PROPELLER_4 = cls.SPRITE_SHEET.subsurface(pygame.Rect(32, 0, 32, 32))  
        cls.PROPELLERS = [cls.PROPELLER_1, cls.PROPELLER_2, cls.PROPELLER_3, cls.PROPELLER_4]


    def update(self):
        self.death_check()
        self.player_collision_check()


    def player_collision_check(self):
        collision = self.rect.colliderect(self.game.player.rect)
        if (collision 
            and not self.player.dead 
            and not self.player.is_flying()):

            self.player.JUMP_STRENGTH = -55
            self.player.jump(play_sound=False)
            self.player.JUMP_STRENGTH = -23 if self.player.using_spring_shoes else -15
            
            self.being_used = True
            self.player.using_propeller = True
            sounds.propeller.play()


    def death_check(self):
        if self.rect.y > self.SCREEN_HEIGHT:
            self.kill()

    def draw(self, screen):
        self.image.set_alpha(self.game.fade_out_alpha)    
        screen.blit(self.image, self.rect)

