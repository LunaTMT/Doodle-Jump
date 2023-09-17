import Assets.sounds as sounds
import pygame
import texture

from random import randint

class Blackhole(pygame.sprite.Sprite):
    
    SPRITE_SHEET = pygame.image.load(f"Assets/Images/Game_tiles/{texture.file_name}.png")
    DEFAULT = SPRITE_SHEET.subsurface(pygame.Rect(233, 51, 67, 65))  # Extract a 32x32 sprite
    SUCK_SOUND = sounds.suck
    

    def __init__(self, game):
        super().__init__()
        self.game           = game
        self.SCREEN_WIDTH   = game.SCREEN_WIDTH
        self.SCREEN_HEIGHT  = game.SCREEN_HEIGHT
        self.player         = game.player

        self.image = self.DEFAULT
        self.rect = self.image.get_rect()
        self.rect.x = randint(self.rect.width, self.SCREEN_WIDTH - self.rect.width)
        self.rect.y = -self.rect.height

        self.blocked = False
        self.collision = False

    @classmethod
    def update_images(cls):
        """
        This function updates the class images when a different texture pack has been chosen
        """
        cls.SPRITE_SHEET = pygame.image.load(f"Assets/Images/Game_tiles/{texture.file_name}.png")
        cls.DEFAULT = cls.SPRITE_SHEET.subsurface(pygame.Rect(233, 51, 67, 65))  # Extract a 32x32 sprite

    def update(self):
        self.death_check()
        self.player_collision_check()

    def death_check(self):
        """
        This function checks to see if the blackhole has gone past the bottom of the screen
        """
        if self.rect.y > self.SCREEN_HEIGHT:
            self.kill()
            del self
        
    def player_collision_check(self):
        """ 
        This function checks to see if the player has collided with the blackhole
        
        so long as the player has not already collide with the blackhole, meaning we only run this piece of code once upon collision
        and the player is not using a flying powewr up
        and the player is not dead 
        the collision will occur
        """
        if (self.rect.colliderect(self.game.player.rect) 
            and not self.collision 
            and not self.player.is_flying()
            and not self.player.dead):
            
    
            if self.player.using_shield:
                """
                If the player is using a shield we don't kill the player but rather make them jump past the blackhole and remove the shield
                whilst the user collides with the blackhole and they have a shield the blackhole is 'blocked' until the user no longer collides with it
                hence the else statement that unblocks the blackhole
                """
                self.player.jump(play_sound=False)
                self.player.using_shield = False
                self.blocked = True
                self.collision = False
                sounds.block.play()
                

            elif not self.blocked:
                """
                If the blackhole is not blocked then the player's states are necessarily changed such that the player obj will be sucked into
                the blackholes location
                """
                self.player.using_spring_shoes = False #When sucked into black whole they stick out of edge without being removed
                
                self.player.suction_object_collided_with = self #Used in player function 'suck_player_to_center_of_object'
                self.player.suction_object_collision = True
                
                self.player.paused = True
                
                self.player.dead_by_suction = True #end game state to determine whether to show the bottom 'falling image'
                self.player.dead = True

                self.collision = True
                self.game.end_game = True #game-state change
                sounds.suck.play()
        else: 
            self.blocked = False
    

    def draw(self, screen):
        self.image.set_alpha(self.game.fade_out_alpha)
        screen.blit(self.image, self.rect)