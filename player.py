import pygame
from pygame.locals import *
import assets.colours as colours
import assets.sounds as sounds
from random import choice, randint




class Player(pygame.sprite.Sprite):

    def __init__(self, game, x, y):
        super().__init__()

        self.game = game
    
        self.CENTER_X = game.CENTER_X
        self.CENTER_Y = game.CENTER_Y
        self.SCREEN_HEIGHT = game.SCREEN_HEIGHT
        self.SCREEN_WIDTH = game.SCREEN_WIDTH
        self.GRAVITY = game.GRAVITY
        self.JUMP_STRENGTH = game.JUMP_STRENGTH

        self.default_x = self.x = x
        self.default_y = self.y = y
        self.previous_y_difference = int(self.y - self.CENTER_Y)

        self.speed = 5 
        
        self.left_image = pygame.image.load("Doodle_Jump/assets/images/player/left.png").convert_alpha()
        self.left_image_nose = pygame.image.load("Doodle_Jump/assets/images/player/left_nose.png").convert_alpha()

        self.left_jump_image = pygame.image.load("Doodle_Jump/assets/images/player/left_jump.png").convert_alpha()
        self.left_jump_image_nose = pygame.image.load("Doodle_Jump/assets/images/player/left_jump_nose.png").convert_alpha()
        
        self.right_image = pygame.image.load("Doodle_Jump/assets/images/player/right.png").convert_alpha()
        self.right_image_nose = pygame.image.load("Doodle_Jump/assets/images/player/right_nose.png").convert_alpha()

        self.right_jump_image = pygame.image.load("Doodle_Jump/assets/images/player/right_jump.png").convert_alpha()
        self.right_jump_image_nose = pygame.image.load("Doodle_Jump/assets/images/player/right_jump_nose.png").convert_alpha()
        
        self.shoot_image = pygame.image.load("Doodle_Jump/assets/images/player/shoot.png").convert_alpha()
        self.shoot_image_nose = pygame.image.load("Doodle_Jump/assets/images/player/shoot_nose.png").convert_alpha()
        
        self.shoot_jump_image = pygame.image.load("Doodle_Jump/assets/images/player/shoot_jump.png").convert_alpha()
        self.shoot_jump_image_nose = pygame.image.load("Doodle_Jump/assets/images/player/shoot_jump_nose.png").convert_alpha()
        
        self.prior_nose = self.nose = self.left_image_nose
        self.prior_image = self.image = self.left_image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.center = (self.x, self.y)
        
        self.prior_y_velocity = 0
        self.velocity_y = 0
        self.on_ground = False
        self.jumping = False
        self.falling = False

        self.counter = 0
        self.differences = []
        self.paused = False

    def handle_events(self, event):
        if not self.paused:
            if ((event.type == KEYDOWN and event.key in (K_SPACE, K_UP)) or 
                (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1)):
                self.shoot()

           

    def move_left(self):
        self.prior_image = self.image = self.left_image
        self.prior_nose = self.nose = self.left_image_nose
        self.x -= self.speed

    def move_right(self):
        self.prior_image = self.image = self.right_image
        self.prior_nose = self.nose = self.right_image_nose
        self.x += self.speed

    def shoot(self):
        shoot_sound = choice((sounds.shoot_1, sounds.shoot_2))
        shoot_sound.play()
        bullet = Bullet(self.rect.centerx, self.rect.top)
        self.game.bullets.add(bullet)

    def jump(self):
        self.excess_y = self.CENTER_X - (self.y - 273)
        self.velocity_y = self.JUMP_STRENGTH
        self.on_ground = False
        self.jumping = True
        sounds.jump.play()
        

    def update(self):

        keys = pygame.key.get_pressed()
            
        if keys[K_LEFT]:
            self.move_left()
        if keys[K_RIGHT]:
            self.move_right()
        if keys[K_SPACE] or keys[K_UP]:
            self.prior_image = self.image = self.shoot_image
            self.prior_nose = self.nose = self.shoot_image_nose

        self.velocity_y += self.GRAVITY
        self.y += self.velocity_y
        
        #Gravity update
        if self.velocity_y > self.GRAVITY:
            self.falling = True 
            self.jumping = False
        else:
            self.falling = False
        
        #Alter images depending on whether the sprite is jumping, else revert to default
        if self.jumping:
            match self.image:
                case self.left_image:
                    self.image = self.left_jump_image
                    self.nose  = self.left_jump_image_nose
                case self.right_image:
                    self.image = self.right_jump_image
                    self.nose  = self.right_jump_image_nose
                case self.shoot_image:
                    self.image = self.shoot_jump_image
                    self.nose  = self.shoot_jump_image_nose
        else:
            self.image = self.prior_image
            self.nose = self.prior_nose
            
        #end game state check
        if self.y > self.SCREEN_HEIGHT - self.rect.height:
            self.y = self.SCREEN_HEIGHT - self.rect.height
            self.velocity_y = 0
            self.on_ground = True
        
        #Ensures the sprite does not disappear when they go outside the bounds.
        #If they do they reappear on the opposite side
        if self.x > self.SCREEN_WIDTH:
            self.x = 0
        elif self.x < 0:
            self.x = self.SCREEN_WIDTH

        self.rect.topleft = (self.x, self.y)

        
        if self.y < self.CENTER_Y - self.rect.height:
            
            
            difference = int((self.y - self.CENTER_Y) - self.previous_y_difference)
            self.previous_y_difference = int(self.y - self.CENTER_Y)
            
            for platform in self.game.platforms.sprites():
                platform.rect.y -= difference

            for platform in self.game.movable_platforms.sprites():
                platform.rect.y -= difference
            
            #print(difference, self.previous_y_difference, int(self.y), self.previous_y_difference - self.y)
            self.rect.y = (self.SCREEN_HEIGHT // 2) - self.rect.height
            
       

        #Set the rect x and y depending on all this.
        

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        if self.nose:
            screen.blit(self.nose, self.rect)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 10), pygame.SRCALPHA)  # Creating a transparent surface
        pygame.draw.circle(self.image, colours.BLACK, (5, 5), 6)
        pygame.draw.circle(self.image, colours.BULLET, (5, 5), 4)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        self.rect.y -= 15
        if self.rect.bottom < 0:
            self.kill()