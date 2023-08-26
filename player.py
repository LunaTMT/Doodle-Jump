import pygame
from pygame.locals import *
import assets.colours as colours
import assets.sounds as sounds
from random import choice, randint


GRAVITY = 0.4 # Adjust gravity strength
JUMP_STRENGTH = -15 

class Player(pygame.sprite.Sprite):

    def __init__(self, game, x, y):
        super().__init__()

        self.game = game
        self.SCREEN_HEIGHT = game.SCREEN_HEIGHT
        self.SCREEN_WIDTH = game.SCREEN_WIDTH
        self.JUMP_STRENGTH = game.JUMP_STRENGTH

        self.default_x = self.x = x
        self.default_y = self.y = y
        self.start_y = 0
        self.excess_y = 0
        self.previous_y_difference = 0

        self.speed = 5 
        
        self.left_image = pygame.image.load("Doodle_Jump/assets/images/left.png").convert_alpha()
        self.left_image_nose = pygame.image.load("Doodle_Jump/assets/images/left_nose.png").convert_alpha()

        self.left_jump_image = pygame.image.load("Doodle_Jump/assets/images/left_jump.png").convert_alpha()
        self.left_jump_image_nose = pygame.image.load("Doodle_Jump/assets/images/left_jump_nose.png").convert_alpha()
        
        self.right_image = pygame.image.load("Doodle_Jump/assets/images/right.png").convert_alpha()
        self.right_image_nose = pygame.image.load("Doodle_Jump/assets/images/right_nose.png").convert_alpha()

        self.right_jump_image = pygame.image.load("Doodle_Jump/assets/images/right_jump.png").convert_alpha()
        self.right_jump_image_nose = pygame.image.load("Doodle_Jump/assets/images/right_jump_nose.png").convert_alpha()
        
        self.shoot_image = pygame.image.load("Doodle_Jump/assets/images/shoot.png").convert_alpha()
        self.shoot_image_nose = pygame.image.load("Doodle_Jump/assets/images/shoot_nose.png").convert_alpha()
        
        self.shoot_jump_image = pygame.image.load("Doodle_Jump/assets/images/shoot_jump.png").convert_alpha()
        self.shoot_jump_image_nose = pygame.image.load("Doodle_Jump/assets/images/shoot_jump_nose.png").convert_alpha()
        
        self.prior_nose = self.nose = self.left_image_nose
        self.prior_image = self.image = self.left_image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.center = (self.x, self.y)
        
        self.velocity_y = 0
        self.on_ground = False
        self.jumping = False
        self.falling = False

    def handle_events(self, event=None):
        keys = pygame.key.get_pressed()
        if keys[K_LEFT]:
            self.move_left()
        if keys[K_RIGHT]:
            self.move_right()
        if keys[K_SPACE] or keys[K_UP]:
            self.prior_image = self.image = self.shoot_image
            self.prior_nose = self.nose = self.shoot_image_nose
        
        if event and event.type == KEYDOWN:
            if event.key in (K_SPACE, K_UP):
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
        self.excess_y = (self.SCREEN_HEIGHT // 2) - (self.y - 273)
        #print(self.excess_y)
        self.velocity_y = JUMP_STRENGTH
        self.on_ground = False
        self.jumping = True
        sounds.jump.play()
        

    def update(self):
        self.velocity_y += GRAVITY
        self.y += self.velocity_y

        #Gravity update
        if self.velocity_y > GRAVITY:
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

        
        if self.y < (self.SCREEN_HEIGHT // 2)  - self.rect.height:
            difference = (self.y - 450) - self.previous_y_difference
            self.previous_y_difference = self.y - 450

            for platform in self.game.platforms.sprites():
                platform.rect.y -= int(difference)

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