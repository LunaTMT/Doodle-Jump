import pygame
import Assets.sounds as sounds
import texture



class SpringShoes(pygame.sprite.Sprite):
    id = 0 

    SPRITE_SHEET = pygame.image.load(f"Assets/Images/Game_tiles/default.png")
    
    DEFAULT_IMAGE = SPRITE_SHEET.subsurface(pygame.Rect(301, 205, 27, 21))  
    COMPRESSED_IMAGE = SPRITE_SHEET.subsurface(pygame.Rect(301, 237, 27, 21))  

    SHOOT_IMAGE = SPRITE_SHEET.subsurface(pygame.Rect(590, 214, 27, 20))  
    SHOOT_COMPRESSED = SPRITE_SHEET.subsurface(pygame.Rect(589, 241, 27, 21))  
    
    def __init__(self, game, tile, x, y):
        super().__init__()
        self.game = game
        self.SCREEN_HEIGHT = game.SCREEN_HEIGHT
        self.SCREEN_WIDTH = game.SCREEN_WIDTH
        
        self.CENTER_X = game.CENTER_X
        self.player = game.player


        self.alpha = 255
        self.x = x
        self.y = y - 18
        self.image = self.DEFAULT_IMAGE 
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.center = (self.x, self.y)
        self.being_used = False

    @classmethod
    def update_images(_):
        pass


    def update(self):
        self.death_check()
        self.player_collision_check()


    def player_collision_check(self):
        collision = self.rect.colliderect(self.game.player.rect)
        if (collision 
            and not self.player.dead 
            and not self.player.is_flying()):
            
            self.being_used = True
            self.player.using_spring_shoes = True
            self.player.spring_shoe_jump_count = 0
            self.player.JUMP_STRENGTH = -23
            self.player.jump()


    def death_check(self):
        if self.rect.y > self.SCREEN_HEIGHT:
            self.kill()

    def draw(self, screen):
        if not self.being_used:
            self.image.set_alpha(self.game.fade_out_alpha)    
            screen.blit(self.image, self.rect)

