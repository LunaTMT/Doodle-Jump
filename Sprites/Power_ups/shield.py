import pygame
import Assets.sounds as sounds

class Shield(pygame.sprite.Sprite):

    DEFAULT_IMAGE = pygame.image.load(f"Assets/Images/Power_up/shield_power_up.png")
    
    def __init__(self, game, x, y, tile):
        super().__init__()
        self.game           = game
        self.SCREEN_HEIGHT  = game.SCREEN_HEIGHT
        self.SCREEN_WIDTH   = game.SCREEN_WIDTH
        self.CENTER_X       = game.CENTER_X
        self.player         = game.player

        self.tile = tile

        self.x = x
        self.y = y - 30

        self.image = self.DEFAULT_IMAGE 
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

        self.being_used = False

    @classmethod
    def update_images(_):
        """
        We must have this method when iterating through all powerup classes and updating the image based on the texture.
        The shield however, is a static image that does not change. Hence, the empty function.
        """
        pass

    def update(self):
        self.death_check()
        self.player_collision_check()
    
    def death_check(self):
        """
        Removing the shield power up when the tile goes off screen or the shield power up is being used by the player
        """
        if (self.rect.y > self.SCREEN_HEIGHT) or self.being_used:
            self.tile.power_up = None
            self.kill()
            

    def player_collision_check(self):
        """
        If the player collides with the power up the we activate the using_shield state for the player unless the player is already using a shield
        """
        collision = self.rect.colliderect(self.player.rect)
        if (collision 
            and not self.player.dead
            and not self.player.using_shield):
            self.player.using_shield = True
            self.being_used = True
            sounds.activate_shield.play()

    def draw(self, screen):
        self.image.set_alpha(self.game.fade_out_alpha)    
        screen.blit(self.image, self.rect)