import pygame
import Assets.colours as colours
import Assets.sounds as sounds
import random
import texture

from pygame.locals import *
from random import randint

class Monster(pygame.sprite.Sprite):


    SPRITE_SHEET = pygame.image.load(f"Assets/Images/Game_tiles/{texture.file_name}.png")

    TERRIFIER = SPRITE_SHEET.subsurface(pygame.Rect(0, 421, 62, 91))  
    FAT_GREEN = SPRITE_SHEET.subsurface(pygame.Rect(0, 357, 84, 61))  
    BAT = SPRITE_SHEET.subsurface(pygame.Rect(148, 0, 77, 45))
    DOUBLE = SPRITE_SHEET.subsurface(pygame.Rect(63, 183, 80, 53))
    BALL = SPRITE_SHEET.subsurface(pygame.Rect(149, 263, 46, 39))

    def __init__(self, game):
        super().__init__()
        self.game           = game
        self.player         = game.player
        self.CENTER_X       = game.CENTER_X
        self.CENTER_Y       = game.CENTER_Y
        self.SCREEN_HEIGHT  = game.SCREEN_HEIGHT
        self.SCREEN_WIDTH   = game.SCREEN_WIDTH
        self.GRAVITY        = game.GRAVITY
        self.JUMP_STRENGTH  = game.JUMP_STRENGTH

        # All the different types of monster images 
        self.monsters = (self.TERRIFIER,
                         self.FAT_GREEN,
                         self.BAT,
                         self.DOUBLE,
                         self.BALL)
        
        #Setting random image and initiating rect object with its coordinates
        self.image = random.choice(self.monsters)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(self.rect.width, self.SCREEN_WIDTH - self.rect.width)
        self.rect.y = -self.rect.height

        #####
        #speed direction and angle/radius for movement
        self.prior_speed = self.speed = random.randint(1,5)
        self.prior_speed_x = self.speed_x = random.randint(1,5)
        self.prior_speed_y = self.speed_y = random.randint(1,5)
        
        self.direction = 1
        self.direction_x = 1
        self.direction_y = 1

        self.angle = 0 
        self.radius = 100  # Circular path radius
        #####
        
        #Variety of movment functions
        self.movements = (self.ping_pong_ball,
                          self.up_down_movement,
                          self.side_to_side_movement)
        self.movement_function = random.choice(self.movements)

        #default monster sound played continuously whilst alive
        self.sound = sounds.monster
        self.sound.play(-1)
        
        #states
        self.blocked = False
        self.collision = False
        self.paused = False
    
    @classmethod
    def update_images(cls):
        """
        This function updates the class images when a different texture pack has been chosen
        """
        cls.SPRITE_SHEET = pygame.image.load(f"Assets/Images/Game_tiles/{texture.file_name}.png")

        cls.TERRIFIER = cls.SPRITE_SHEET.subsurface(pygame.Rect(0, 421, 62, 91))  
        cls.FAT_GREEN = cls.SPRITE_SHEET.subsurface(pygame.Rect(0, 357, 84, 61))  
        cls.BAT = cls.SPRITE_SHEET.subsurface(pygame.Rect(148, 0, 77, 45))
        cls.DOUBLE = cls.SPRITE_SHEET.subsurface(pygame.Rect(63, 183, 80, 53))
        cls.BALL = cls.SPRITE_SHEET.subsurface(pygame.Rect(149, 263, 46, 39))
    
    def update(self):
        self.movement_function()
        self.boundary_check()
        self.killed_check()
        self.player_collision_check()

    def pause(self):
        """
        Given each instantiation of a monster can have a different movement function where the speed in either x or y plane will vary we must
        store the prior speed for all planes when pausing
        Once paused we set all directional speed to 0"""
        self.prior_speed     = self.speed 
        self.prior_speed_x   = self.speed_x 
        self.prior_speed_y   = self.speed_y 

        self.speed = 0
        self.speed_x = 0
        self.speed_y = 0

    def unpause(self):
        """
        Upon unpausing we reassign the speed of both planes to the value stored in our pause function.
        """
        self.speed   = self.prior_speed
        self.speed_x = self.prior_speed_x 
        self.speed_y = self.prior_speed_y 


    def player_collision_check(self):
        """ 
        This function checks to see if the player has collided with the monster
        
        so long as the player has not already collided with the monster, meaning we only run this piece of code once upon collision 
        and the player is not using a flying power up
        and the player is not dead 
        the collision will occur
        """
        if (self.rect.colliderect(self.player.rect) 
            and not self.collision 
            and not self.player.is_flying()
            and not self.player.dead):
            
            
            if self.player.using_shield:
                
                self.player.jump(play_sound=False)
                self.blocked = True
                self.collision = False
                
                """
                If the player is falling it must have jumped on top of the monster, thus killing it.
                else the player hit it directly and we must remove the shield
                """
                if self.player.falling:
                    self.remove()
                else:
                    self.player.using_shield = False
                    sounds.block.play()
            

            elif not self.blocked:
                """
                When the player hits the monster with a shield on we must block the collision until the player is no longer touching the monster
                otherwise the shield would just be removed and the played would die
                """
                self.collision = True #Only want to run this once (beginning: 'and not self.collision')

                #If the player is falling then it must hit the top thus killing monster
                if self.player.falling:
                    self.player.jump(play_sound=False)                    
                    self.remove()

                #otherwise the player goes directly into the monster head first and dies
                else:
                    self.player.handling_events = False
                    self.player.knocked_out = True
                    self.player.dead = True
                    self.player.velocity_y = -1
                    sounds.thump.set_volume(4)
                    sounds.thump.play()
       
        else: 
            self.blocked = False

    def remove(self):
        """
        This function removes the monster by playing a death sound, killing the main monster sound and deleting the object
        """
        random.choice((sounds.die_1, sounds.die_2)).play()
        self.sound.stop()
        self.kill()   
        del self

    def killed_check(self):
        """This function checks to see if a bullet has collided with the monster"""
        if pygame.sprite.spritecollide(self, self.game.bullets, True):
            self.remove()
            
    def boundary_check(self):
        "This function checks to see if the monster has gone past the bottom of the screen"
        if self.rect.y > self.SCREEN_HEIGHT:
            self.sound.stop()
            self.kill()
            
    
    """
    The following three functions are all movement functions 
    - Bouncing off the the left and right wall like a ping pong ball
    - Moving up and down
    - Side to side motion
    
    """
    def ping_pong_ball(self):
        self.rect.x += self.speed_x * self.direction_x
        self.rect.y += self.speed_y * self.direction_y
        
        if self.rect.right > self.SCREEN_WIDTH or self.rect.left < 0:
            self.direction_x *= -1
        if self.rect.bottom > self.SCREEN_HEIGHT or self.rect.top < 0:
            self.direction_y *= -1

    def up_down_movement(self):
        self.rect.y += self.speed * self.direction
        if self.rect.bottom > self.SCREEN_HEIGHT or self.rect.top < 0:
            self.direction *= -1
        
    def side_to_side_movement(self):
        self.rect.x += self.speed * self.direction
        if self.rect.right > self.SCREEN_WIDTH or self.rect.left < 0:
            self.direction *= -1


    def draw(self, screen):
        self.image.set_alpha(self.game.fade_out_alpha)
        screen.blit(self.image, self.rect)
        
        
