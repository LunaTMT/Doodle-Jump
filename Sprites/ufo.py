import pygame
import random
import Assets.sounds as sounds
import Assets.colours as colours
import texture
from math import sin, radians


class UFO(pygame.sprite.Sprite):

    SPRITE_SHEET = pygame.image.load(f"Assets/Images/Game_tiles/{texture.file_name}.png")

    DEFAULT = SPRITE_SHEET.subsurface(pygame.Rect(428, 208, 84, 122))  # Extract a 32x32 sprite
    COLLISION_IMAGE = SPRITE_SHEET.subsurface(pygame.Rect(428, 83, 84, 122))  # Extract a 32x32 sprite
    

    def __init__(self, game, x=None, y=None):
        super().__init__()
        self.game           = game
        self.SCREEN_WIDTH   = game.SCREEN_WIDTH
        self.SCREEN_HEIGHT  = game.SCREEN_HEIGHT
        self.player         = game.player
        self.fade_out_alpha = game.fade_out_alpha

        self.paused = False

        self.image = self.DEFAULT
        self.rect = self.image.get_rect()

        """
        These two conditionals are for the initialisation of the ufo for the main menu.
        """
        if x == None:
            self.x = self.rect.x = random.randint(self.rect.width + 80, self.SCREEN_WIDTH - self.rect.width - 80)
        else:
            self.x = self.rect.x = x

        if x == None:  
            self.y = self.rect.y = -self.rect.height
        else:
            self.y = self.rect.y = y
        
        self.blocked = False
        self.collision = False

        self.angle = 0
        self.sound = sounds.ufo
        self.sound.set_volume(2)
        self.sound.play(-1)


    @classmethod
    def update_images(cls):
        """
        This function updates the class images when a different texture pack has been chosen
        """
        cls.SPRITE_SHEET = pygame.image.load(f"Assets/Images/Game_tiles/{texture.file_name}.png")
        cls.DEFAULT = cls.SPRITE_SHEET.subsurface(pygame.Rect(428, 208, 84, 122))  # Extract a 32x32 sprite
        cls.COLLISION_IMAGE = cls.SPRITE_SHEET.subsurface(pygame.Rect(428, 83, 84, 122))  # Extract a 32x32 sprite
    
    def update_current_image(self):
        """
        This function is specifically here for the ufo in the main menu screen
        When a texture is selected we update the ufo currently shown
        """
        self.image = self.DEFAULT

    def update(self):
        self.movement_update()
        self.player_collision_check()
        self.death_check()
        self.killed_check()


    def death_check(self):
        """
        If the tile goes beyond the screen at the bottom then we kill the object whilst decrementing the total tile number
        """
        if self.rect.y > self.SCREEN_HEIGHT:
            self.remove()
            
    
    def player_collision_check(self):
        """ 
        This function checks to see if the player has collided with the ufo
        
        so long as the player has not already collided with the ufo, meaning we only run this piece of code once upon collision 
        and the player is not using a flying power up
        and the player is not dead 
        the collision will occur
        """
        if (self.rect.colliderect(self.game.player.rect) 
            and not self.collision 
            and not self.player.is_flying()
            and not self.player.dead):
            
            """
            if if they're falling we kill the ufo
            else the player is using a shield then we protect them if they collide head on
            """
            if self.player.using_shield:
                
                self.player.jump(play_sound=False)
                self.blocked = True
                self.collision = False
            
                if self.player.falling:
                    self.remove(play_sound=True)
                else:
                    self.player.using_shield = False
                    sounds.block.play()
            
            elif not self.blocked:
                self.collision = True

                #If player hits the top kill ufo
                if self.player.falling: 
                    self.player.jump(play_sound=False)                    
                    self.remove(play_sound=True)
                #Head on collision
                else:
                    #Update player states
                    self.player.using_spring_shoes = False #When sucked into black whole they stick out of edge without being removed
                    self.player.suction_object_collided_with = self
                    self.player.suction_object_collision = True
                    self.player.dead_by_suction = True
                    self.player.paused = True
                    self.player.dead = True

                    self.collision = True

                    #gamestate change
                    self.game.end_game = True

                    #Sucking up image
                    self.image = self.COLLISION_IMAGE
                    sounds.ufo_suck.play()
        else: 
            self.blocked = False

    def killed_check(self):
        if pygame.sprite.spritecollide(self, self.game.bullets, True):
            self.remove(play_sound=True)

    def remove(self, play_sound=False):
        """
        This function removes the ufo and makes a sound if the bool for making a sound is specified
        The object is then deleted
        """
        if play_sound: sounds.tile_disappear.play() 
        self.sound.stop()
        self.kill()   
        del self
            
    def draw(self, screen):
        self.image.set_alpha(self.game.fade_out_alpha)
        screen.blit(self.image, self.rect)

    def movement_update(self):
        if not self.paused:
            # Update the sprite's x-coordinate based on the figure 8 motion
            self.angle += 0.09 # Adjust this value to control the speed of the motion

            self.rect.x += int(5 * sin(self.angle))
            self.rect.y += int(2.5 * sin(2*self.angle))
