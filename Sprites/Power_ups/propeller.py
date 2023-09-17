import pygame
import Assets.sounds as sounds
import texture

class Propeller(pygame.sprite.Sprite):

    SPRITE_SHEET = pygame.image.load(f"Assets/Images/Animations/Propeller/{texture.file_name}.png")
    
    PROPELLER_1 = SPRITE_SHEET.subsurface(pygame.Rect(0, 0, 32, 32))  
    PROPELLER_2 = SPRITE_SHEET.subsurface(pygame.Rect(32, 0, 32, 32))  
    PROPELLER_3 = SPRITE_SHEET.subsurface(pygame.Rect(0, 32, 32, 32))  
    PROPELLER_4 = SPRITE_SHEET.subsurface(pygame.Rect(32, 0, 32, 32))  
    PROPELLERS = [PROPELLER_1, PROPELLER_2, PROPELLER_3, PROPELLER_4]

    def __init__(self, game, x, y, _):
        super().__init__()
        self.game           = game
        self.SCREEN_HEIGHT  = game.SCREEN_HEIGHT
        self.SCREEN_WIDTH   = game.SCREEN_WIDTH
        self.CENTER_X       = game.CENTER_X
        self.player         = game.player      
        
        self.x = x
        self.y = y - 15
        
        self.image = self.PROPELLER_1 
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

        self.being_used = False

    @classmethod
    def update_images(cls):
        """
        This function updates the class images when a different texture pack has been chosen
        """
        cls.SPRITE_SHEET = pygame.image.load(f"Assets/Images/Animations/Propeller/{texture.file_name}.png")
    
        cls.PROPELLER_1 = cls.SPRITE_SHEET.subsurface(pygame.Rect(0, 0, 32, 32))  
        cls.PROPELLER_2 = cls.SPRITE_SHEET.subsurface(pygame.Rect(32, 0, 32, 32))  
        cls.PROPELLER_3 = cls.SPRITE_SHEET.subsurface(pygame.Rect(0, 32, 32, 32))  
        cls.PROPELLER_4 = cls.SPRITE_SHEET.subsurface(pygame.Rect(32, 0, 32, 32))  
        cls.PROPELLERS = [cls.PROPELLER_1, cls.PROPELLER_2, cls.PROPELLER_3, cls.PROPELLER_4]


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
        This function checks to see if the player has collided with the propeller powerup placed on the tile.

        So long as the player is not dead or is not using another flying powerup (propeller/rocket) the player can use the propeller
        """
        collision = self.rect.colliderect(self.player.rect)
        if (collision 
            and not self.player.dead 
            and not self.player.is_flying()):

            """
            The illusion of the propeller 'jump' just alters the jump strength, calls the jump function and,
            then returns the jump strenght to its previous value
            """
            previous_jump_strength = self.player.JUMP_STRENGTH
            self.player.JUMP_STRENGTH = -55
            self.player.jump(play_sound=False)
            self.player.JUMP_STRENGTH = previous_jump_strength
            
            self.player.using_propeller = True
            sounds.propeller.play()

    def draw(self, screen):
        self.image.set_alpha(self.game.fade_out_alpha)   
        screen.blit(self.image, self.rect)

