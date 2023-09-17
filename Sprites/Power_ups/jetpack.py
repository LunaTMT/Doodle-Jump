import Assets.sounds as sounds
import pygame
import texture

class Jetpack(pygame.sprite.Sprite):
    
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

    START_ANIMATION = [ROCKET_1, ROCKET_2, ROCKET_3]    #  0  -  16 frames
    MAIN_BLAST = [ROCKET_4, ROCKET_5, ROCKET_6]         # 16  - 147 frames
    END_ANIMAITON = [ROCKET_7, ROCKET_8, ROCKET_9]      # 147 - 163 frames

   

    def __init__(self, game, x, y, _):
        super().__init__()
        self.game           = game
        self.SCREEN_HEIGHT  = game.SCREEN_HEIGHT
        self.SCREEN_WIDTH   = game.SCREEN_WIDTH
        self.CENTER_X       = game.CENTER_X
        self.player         = game.player

        self.x = x
        self.y = y - 10

        self.image = self.DEFAULT_ROCKET 
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        
        self.being_used = False
    
    @classmethod
    def update_images(cls):
        """
        This function updates the class images when a different texture pack has been chosen
        """
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

        START_ANIMATION = [ROCKET_1, ROCKET_2, ROCKET_3]    #  0  -  16 frames
        MAIN_BLAST = [ROCKET_4, ROCKET_5, ROCKET_6]         # 16  - 147 frames
        END_ANIMAITON = [ROCKET_7, ROCKET_8, ROCKET_9]      # 147 - 163 frames

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
        This function checks to see if the player has collided with the jetpack powerup placed on the tile.

        So long as the player is not dead or is not using a flying powerup (propeller/rocket) the player can use the rocket
        """
        collision = self.rect.colliderect(self.player.rect)
        if (collision 
            and not self.player.dead 
            and not self.player.is_flying()):

            """
            The illusion of the jetpack 'jump' just alters the jump strength, calls the jump function and,
            then returns the jump strenght to its previous value
            """
            previous_jump_strength = self.player.JUMP_STRENGTH
            self.player.JUMP_STRENGTH = -65
            self.player.jump(play_sound=False)
            self.player.JUMP_STRENGTH = previous_jump_strength
            self.player.using_jetpack = True #Used for drawing the animation
            
            sounds.jetpack.play()


    def draw(self, screen):
        self.image.set_alpha(self.game.fade_out_alpha)   
        screen.blit(self.image, self.rect)

