import Assets.sounds as sounds
import pygame
import texture

class Trampoline(pygame.sprite.Sprite):

    SPRITE_SHEET = pygame.image.load(f"Assets/Images/Game_tiles/{texture.file_name}.png")
    TRAMPOLINE_1 = SPRITE_SHEET.subsurface(pygame.Rect(188, 98, 36, 14))  # Extract a 32x32 sprite
    TRAMPOLINE_2 = SPRITE_SHEET.subsurface(pygame.Rect(474, 53, 36, 14))
    TRAMPOLINE_3 = SPRITE_SHEET.subsurface(pygame.Rect(149, 94, 36, 18))

    def __init__(self, game, x, y, _):
        super().__init__()
        self.game           = game
        self.SCREEN_HEIGHT  = game.SCREEN_HEIGHT
        self.SCREEN_WIDTH   = game.SCREEN_WIDTH
        self.CENTER_X       = game.CENTER_X
        self.player         = game.player

        self.x = x
        self.y = y - 10

        self.image = self.TRAMPOLINE_1
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

        self.expanded = False

    @classmethod
    def update_images(cls):
        """
        This function updates the class images when a different texture pack has been chosen
        """
        cls.SPRITE_SHEET = pygame.image.load(f"Assets/Images/Game_tiles/{texture.file_name}.png")
        cls.TRAMPOLINE_1 = cls.SPRITE_SHEET.subsurface(pygame.Rect(188, 98, 36, 14)) 
        cls.TRAMPOLINE_2 = cls.SPRITE_SHEET.subsurface(pygame.Rect(474, 53, 36, 14))
        cls.TRAMPOLINE_3 = cls.SPRITE_SHEET.subsurface(pygame.Rect(149, 94, 36, 18))

    def update(self):
        self.death_check()
        self.player_collision_check()

    def death_check(self):
        """
        This function checks to see if the power up on the tile has gone past the bottom of the screen
        """
        if self.rect.y > self.SCREEN_HEIGHT:
            self.kill()

    def player_collision_check(self):
        """ 
        This function checks to see if the player has collided with the trampoline powerup placed on the tile.

        So long as the player is falling and not dead the collision will take place
        """
        collision = self.rect.colliderect(self.player.rect)
        
        if (collision 
            and self.player.falling 
            and not self.player.dead):
            
            previous_jump_strength = self.player.JUMP_STRENGTH
            self.player.JUMP_STRENGTH = -30
            self.player.jump(play_sound=False)
            self.player.JUMP_STRENGTH =  previous_jump_strength
           
            sounds.trampoline.play()
            self.expanded = True
            self.player.using_trampoline = True
            self.image = self.TRAMPOLINE_2
        
        elif not collision and self.expanded:
            self.image = self.TRAMPOLINE_3
    

    def draw(self, screen):
        self.image.set_alpha(self.game.fade_out_alpha)    
        screen.blit(self.image, self.rect)