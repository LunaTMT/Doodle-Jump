import pygame
import Assets.sounds as sounds
import texture

class Spring(pygame.sprite.Sprite):

    SPRITE_SHEET = pygame.image.load(f"Assets/Images/Game_tiles/{texture.file_name}.png")
    SPRING = SPRITE_SHEET.subsurface(pygame.Rect(404, 99, 17, 12))  # Extract a 32x32 sprite
    SPRING_EXPANDED = SPRITE_SHEET.subsurface(pygame.Rect(404, 115, 17, 28))

    #x = random.randint(self.rect.topleft, self.rect.topright)
    #y = self.rect.top 

    def __init__(self, game, x, y, _):
        super().__init__()
        self.game           = game
        self.SCREEN_HEIGHT  = game.SCREEN_HEIGHT
        self.SCREEN_WIDTH   = game.SCREEN_WIDTH
        self.CENTER_X       = game.CENTER_X
        self.player         = game.player
        
        self.x = x
        self.y = y - 10

        self.image = self.SPRING 
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        
        self.expanded = False
        self.collision = False

    @classmethod
    def update_images(cls):
        """
        This function updates the class images when a different texture pack has been chosen
        """
        cls.SPRITE_SHEET = pygame.image.load(f"Assets/Images/Game_tiles/{texture.file_name}.png")
        cls.SPRING = cls.SPRITE_SHEET.subsurface(pygame.Rect(404, 99, 17, 12))  # Extract a 32x32 sprite
        cls.SPRING_EXPANDED = cls.SPRITE_SHEET.subsurface(pygame.Rect(404, 115, 17, 28))

    def update(self):
        self.death_check()
        self.player_collision_check()

    def player_collision_check(self):
        """ 
        This function checks to see if the player has collided with the spring powerup placed on the tile.

        So long as the player is falling, not dead and the spring hasn't already been used before the collision takes place.
        """
        collision = self.rect.colliderect(self.player.rect)
        if (collision 
            and self.player.falling  
            and not self.player.dead
            and not self.expanded):
           
            previous_jump_strength = self.player.JUMP_STRENGTH
            self.player.JUMP_STRENGTH = -23
            self.player.jump(play_sound=False)
            self.player.JUMP_STRENGTH = previous_jump_strength
            
            sounds.spring.play()
            self.player.using_spring = True
            self.collision = True


    def death_check(self):
        """
        This function checks to see if the power up on the tile has gone past the bottom of the screen
        """
        if self.rect.y > self.SCREEN_HEIGHT:
            self.kill()

    def draw(self, screen):
        if self.collision and not self.expanded:
            self.image = self.SPRING_EXPANDED
            self.rect.y -= 20
            self.expanded = True

        self.image.set_alpha(self.game.fade_out_alpha)   
        screen.blit(self.image, self.rect)