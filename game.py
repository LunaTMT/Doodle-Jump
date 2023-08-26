import pygame
from pygame.locals import *
import sys
import assets.colours as colours
import assets.sounds as sounds
from random import choice, randint

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRAVITY = 0.3 # Adjust gravity strength
JUMP_STRENGTH = -10  # Adjust jump strength

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Doodle Jump")
clock = pygame.time.Clock()
pygame.init()
pygame.mixer.init()

all_sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()


class Game:
    def __init__(self):
        self.running = True
        
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.platform1 = Platform(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 40)
        self.platform2 = Platform(SCREEN_WIDTH // 2 + 100, SCREEN_HEIGHT - 80)

       
        for i in range(30):

            platform = Platform(randint(0, SCREEN_WIDTH), randint(0, SCREEN_HEIGHT))
            
            collision = pygame.sprite.spritecollide(platform, platforms, False, pygame.sprite.collide_mask)
            if collision:
                print("Collision")
            else:
                all_sprites.add(platform)
                platforms.add(platform)

        all_sprites.add(self.player)
        all_sprites.add(self.platform1)
        all_sprites.add(self.platform2)

        platforms.add(self.platform1)
        platforms.add(self.platform2)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            self.player.handle_events(event)

        self.player.handle_events()
        
        collisions = pygame.sprite.spritecollide(self.player, platforms, False, pygame.sprite.collide_mask)
        if collisions and self.player.falling:
            self.player.jump()


    def update(self):
        all_sprites.update()
        

    def draw(self):
        screen.fill(colours.WHITE)
        all_sprites.draw(screen)
        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            clock.tick(60)

        pygame.quit()
        sys.exit()

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y

        sprite_sheet = pygame.image.load("Doodle_Jump/assets/images/game-tiles.png").convert_alpha()
        self.image = sprite_sheet.subsurface(pygame.Rect(0, 0, 58, 18))  # Extract a 32x32 sprite
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.center = (self.x, self.y)

    def update(self):
        if self.rect.bottom < 0:
            self.kill()

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.x = x
        self.y = y
        self.width = 50
        self.height = 50
        self.color = (0, 255, 0)
        self.speed = 5  
        
        self.left_image = pygame.image.load("Doodle_Jump/assets/images/left.png").convert_alpha()
        self.left_jump_image = pygame.image.load("Doodle_Jump/assets/images/left_jump.png").convert_alpha()

        self.right_image = pygame.image.load("Doodle_Jump/assets/images/right.png").convert_alpha()
        self.right_jump_image = pygame.image.load("Doodle_Jump/assets/images/right_jump.png").convert_alpha()

        self.shoot_image = pygame.image.load("Doodle_Jump/assets/images/shoot_jump.png").convert_alpha()
        self.shoot_jump_image = pygame.image.load("Doodle_Jump/assets/images/shoot.png").convert_alpha()

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
        
        if event and event.type == KEYDOWN:
            if event.key in (K_SPACE, K_UP):
                self.shoot()
                



    def move_left(self):
        self.prior_image = self.image = self.left_image
        self.x -= self.speed

    def move_right(self):
        self.prior_image = self.image = self.right_image
        self.x += self.speed

    def shoot(self):
        shoot_sound = choice((sounds.shoot_1, sounds.shoot_2))
        shoot_sound.play()
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)

    def jump(self):
        self.velocity_y = JUMP_STRENGTH
        self.on_ground = False
        self.jumping = True
        sounds.jump.play()

    def update(self):
        self.velocity_y += GRAVITY
        self.y += self.velocity_y
        
        if self.velocity_y > GRAVITY:
            self.falling = True 
            self.jumping = False
        else:
            self.falling = False
        
    
        if self.jumping:
            match self.image:
                case self.left_image:
                    self.image = self.left_jump_image
                case self.right_image:
                    self.image = self.right_jump_image
                case self.shoot_image:
                    self.image = self.shoot_jump_image
        else:
            self.image = self.prior_image
            
            
        if self.y > SCREEN_HEIGHT - self.rect.height:
            self.y = SCREEN_HEIGHT - self.rect.height
            self.velocity_y = 0
            self.on_ground = True
            
        self.rect.topleft = (self.x, self.y)

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 10), pygame.SRCALPHA)  # Creating a transparent surface
        pygame.draw.circle(self.image, colours.BLACK, (5, 5), 6)
        pygame.draw.circle(self.image, colours.BULLET, (5, 5), 4)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        self.rect.y -= 10
        if self.rect.bottom < 0:
            self.kill()