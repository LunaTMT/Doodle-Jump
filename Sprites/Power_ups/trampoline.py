
import pygame
import Assets.sounds as sounds
import texture

class Trampoline(pygame.sprite.Sprite):

    SPRITE_SHEET = pygame.image.load(f"Assets/Images/Game_tiles/{texture.file_name}.png")
    TRAMPOLINE_1 = SPRITE_SHEET.subsurface(pygame.Rect(188, 98, 36, 14))  # Extract a 32x32 sprite
    TRAMPOLINE_2 = SPRITE_SHEET.subsurface(pygame.Rect(474, 53, 36, 14))
    TRAMPOLINE_3 = SPRITE_SHEET.subsurface(pygame.Rect(149, 94, 36, 18))

    def __init__(self, game, tile, x, y):
        super().__init__()
        self.game = game
        self.SCREEN_HEIGHT = game.SCREEN_HEIGHT
        self.SCREEN_WIDTH = game.SCREEN_WIDTH
        
        self.CENTER_X = game.CENTER_X
        self.player = game.player

        self.alpha = 255
        self.x = x
        self.y = y - 10
        self.image = self.TRAMPOLINE_1
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.center = (self.x, self.y)
        self.expanded = False


    def update(self):
        self.death_check()
        self.player_collision_check()

    def player_collision_check(self):
        collision = self.rect.colliderect(self.game.player.rect)
        
        if (collision 
            and self.player.falling 
            and not self.player.dead):
            
            self.player.using_trampoline = True
            
            self.player.JUMP_STRENGTH = -30
            self.player.jump(play_sound=False)
            
            if not self.player.using_spring_shoes:
                self.player.JUMP_STRENGTH = -15
            
            sounds.trampoline.play()
            self.expanded = True
            self.image = self.TRAMPOLINE_2
        
        elif self.player.falling:
            self.image = self.TRAMPOLINE_1
        
        elif not collision and self.expanded:
            self.image = self.TRAMPOLINE_3
        
        

    def death_check(self):
        if self.rect.y > self.SCREEN_HEIGHT:
            self.kill()

    def draw(self, screen):
        self.image.set_alpha(self.game.fade_out_alpha)    
        screen.blit(self.image, self.rect)