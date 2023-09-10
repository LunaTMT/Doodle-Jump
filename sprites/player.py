import pygame
from pygame.locals import *
import assets.colours as colours
import assets.sounds as sounds
from random import choice, randint
from sprites.power_ups.jetpack import Jetpack
from sprites.power_ups.propeller import Propeller
from sprites.power_ups.shield import Shield
from sprites.power_ups.spring_shoes import SpringShoes
import texture


class Player(pygame.sprite.Sprite):

    high_score = 0

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
        self.default_y = self.y = -900
        self.previous_y_difference = int(self.y - self.CENTER_Y)

        self.speed = 5 
        
        self.left_image = pygame.image.load(f"assets/images/Player/{texture.folder_name}/Body/left.png").convert_alpha()
        
        self.left_jump_image = pygame.image.load(f"assets/images/Player/{texture.folder_name}/Body/left_jump.png").convert_alpha()
        
        self.right_image = pygame.image.load(f"assets/images/Player/{texture.folder_name}/Body/right.png").convert_alpha()
        
        self.right_jump_image = pygame.image.load(f"assets/images/Player/{texture.folder_name}/Body/right_jump.png").convert_alpha()
        
        self.shoot_image = pygame.image.load(f"assets/images/Player/{texture.folder_name}/Body/shoot.png").convert_alpha()
        
        self.shoot_jump_image = pygame.image.load(f"assets/images/Player/{texture.folder_name}/Body/shoot_jump.png").convert_alpha()
      
        self.shield = pygame.image.load("assets/images/Player/shield.png").convert_alpha()
    
        self.prior_image = self.image = self.left_image
       
        
        self.original_rect = self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.center = (self.x, game.CENTER_Y)


        
        self.stars_1 = pygame.image.load("assets/images/Animations/Stars/1.png").convert_alpha()
        self.stars_2 = pygame.image.load("assets/images/Animations/Stars/2.png").convert_alpha()
        self.stars_3 = pygame.image.load("assets/images/Animations/Stars/3.png").convert_alpha()
        self.stars_location = (self.rect.x, self.rect.top-10)
        self.knocked_out_animation = [self.stars_1,  self.stars_2,  self.stars_3]
        
        
        self.rect = self.image.get_rect()
    
        self.movement_speed = 1
        self.current_position = (self.rect.x, self.rect.y)
        self.current_scale = 1.0
        self.scale_speed = 0.002
        self.image_scale = 1


        self.end_game_y = 840
        self.prior_y_velocity = 0
        self.velocity_y = 0
        self.score = 0
        self.spring_shoe_jump_count = 0

        self.using_spring_shoes = False
        self.using_jetpack = False
        self.using_propeller = False
        self.using_shield = False
        self.using_trampoline = False
        self.using_spring = False
    

        self.left = True 
        self.right = False
        self.black_hole_collided_with = None
        self.blackhole_collision = False
        self.dead_by_blackhole = False
        self.dead = False

        self.spring_collision = False
        self.trampoline_collision = False
        
        self.moved = False
        self.jumping = False
        self.falling = False
        self.check_fall = False
        self.paused = False
        self.knocked_out = False
        self.handling_events = True
        self.collision = False
        self.draw_player = True

    def handle_events(self, event):
        if not self.paused and not self.is_flying() and not self.dead:
            if ((event.type == KEYDOWN and event.key in (K_SPACE, K_UP)) or 
                (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1)):
                self.shoot()

        
    def move_left(self):
        self.prior_image = self.image = self.left_image


        self.x -= self.speed
        self.left = True
        self.right = False

    def move_right(self):
        self.prior_image = self.image = self.right_image

        self.x += self.speed
        self.right = True
        self.left = False

    def shoot(self):
        shoot_sound = choice((sounds.shoot_1, sounds.shoot_2))
        shoot_sound.play()
        bullet = Bullet(self.rect.centerx, self.rect.top)
        self.game.bullets.add(bullet)

    def jump(self, play_sound=True):
        if not self.is_flying():
            self.game.frame = 0
            self.excess_y = self.CENTER_X - (self.y - 273)
            self.velocity_y = self.JUMP_STRENGTH
            self.jumping = True

            if play_sound:
                sounds.jump.play()

            if (self.using_spring_shoes 
                and not self.is_using_booster()):

                sounds.spring.play()
                self.spring_shoe_jump_count += 1


    def is_flying(self):
        return any((self.using_jetpack, self.using_propeller))
    def is_using_booster(self):
        return any((self.using_trampoline, self.using_spring))
   
        
    def update(self):
        if not self.paused: #if we continue to update movement whilst in blackhole. Movement messes up
            self.update_movement()
            self.update_position_based_on_gravity()
            self.update_directional_image()
            self.update_score()
            self.update_maximum_tiles_allowed()
            
            self.fall_check()
            self.y_boundary_check()
            self.x_boundary_check()
            self.spring_shoe_check()

            self.update_rect()
            self.update_other_sprites_based_upon_player_jump_difference()
        
        elif self.blackhole_collision:
            self.blackhole_check()
        
        
    """UDATE"""
    """-------"""
    def update_movement(self):
        if self.handling_events and not self.dead:
            keys = pygame.key.get_pressed()
            mouse_buttons = pygame.mouse.get_pressed()
            
            if keys[K_LEFT]:
                self.move_left()
            if keys[K_RIGHT]:
                self.move_right()
            if (keys[K_SPACE] or keys[K_UP] or mouse_buttons[0]) and not self.is_flying():
                self.prior_image = self.image = self.shoot_image
        
    def update_position_based_on_gravity(self):
 
        if not self.blackhole_collision:
            self.velocity_y += self.GRAVITY
            self.y += self.velocity_y

            #Gravity update
            if (self.velocity_y > self.GRAVITY) and not self.falling:  
                self.falling = True 
                self.fall_y = self.y
                self.end_game_y = self.y + 450 + self.image.get_height() #if self.moved else (-self.rect.bottom + 840))
                self.using_jetpack = False
                self.using_propeller = False
                self.using_trampoline = False
                self.using_spring = False
                self.jumping = False
            elif (self.velocity_y < self.GRAVITY):
                self.falling = False
            else:
                pass
    def update_directional_image(self): 
        #Alter images depending on whether the sprite is jumping, else revert to default

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
          
        
    def update_score(self):
        if self.y < -900:
            self.score = max(self.score, abs(self.y) - 900) 
        Player.high_score = max(Player.high_score, self.score)

    def update_maximum_tiles_allowed(self):
        self.game.enemy_weight = self.score / 100000
        if 0 <= self.score < 1000:
            self.game.max_tile_number = 25
        elif 1000 < self.score <= 10000:
            self.game.max_tile_number = 20
        elif 10000 < self.score <= 20000:
            self.game.max_tile_number = 15

        

    def fall_check(self):
        if self.y >= self.end_game_y and not self.check_fall:

            if self.y < 390:
                difference = abs(self.y) - 900
                self.y = -900
                for platform in (self.game.platforms.sprites() + self.game.movable_platforms.sprites()):
                    platform.rect.y += difference
                    if platform.power_up:
                        platform.power_up.rect.y += difference

                for sprite in (self.game.monsters.sprites() + self.game.blackholes.sprites()):
                    sprite.rect.y += difference

            if not self.black_hole_collided_with:
                sounds.fall.play()
                self.game.draw_bottom = True
            self.check_fall = True


    def y_boundary_check(self):
        if self.rect.top >= 900:
            self.rect.y = 900
            self.velocity_y = 0
            self.dead = True
            self.game.end_game = True      
    def x_boundary_check(self):
        #Ensures the sprite does not disappear when they go outside the bounds.
        #If they do they reappear on the opposite side
        if self.x > self.SCREEN_WIDTH:
            self.x = 0
        elif self.x < 0:
            self.x = self.SCREEN_WIDTH
    def spring_shoe_check(self):
        if self.using_spring_shoes and self.spring_shoe_jump_count % 5 == 0:
            self.JUMP_STRENGTH = self.game.JUMP_STRENGTH
            self.using_spring_shoes = False
    def update_rect(self):
        self.rect.topleft = (self.x, self.y)
    def update_other_sprites_based_upon_player_jump_difference(self):
        if self.y < self.CENTER_Y - self.rect.height:
            self.moved = True

            difference = int((self.y - self.CENTER_Y) - self.previous_y_difference)
            self.previous_y_difference = int(self.y - self.CENTER_Y) 
            
            for platform in self.game.platforms.sprites() + self.game.movable_platforms.sprites():
                platform.rect.y -= difference
                if platform.power_up:
                    platform.power_up.rect.y -= difference
            
            for monster in self.game.monsters.sprites():
                monster.rect.y -= difference
            
            for blackhole in self.game.blackholes.sprites():
                blackhole.rect.y -= difference

            self.rect.y = (self.SCREEN_HEIGHT // 2 - self.rect.height)
   
    def blackhole_check(self):
        
        def resize_image(scale):
            return pygame.transform.scale(self.image, (int(self.rect.width * scale), int(self.rect.height * scale)))

        blackhole_location = (self.black_hole_collided_with.rect.centerx, self.black_hole_collided_with.rect.centery)
        if self.blackhole_collision and (self.rect.x, self.rect.y) != blackhole_location:

            dx = blackhole_location[0] - self.rect.centerx
            dy = blackhole_location[1] - self.rect.centery
            distance = pygame.math.Vector2(dx, dy).length()
        
            if distance >= 5:
                direction = pygame.math.Vector2(dx, dy).normalize()
                movement_speed = 5
                self.rect.move_ip(direction * movement_speed)
         
            if self.image_scale > 0.02:
                self.image_scale -= 0.02
                self.image = resize_image(self.image_scale)
                scaled_rect = self.image.get_rect()
                scaled_rect.center = self.rect.center 
                self.rect = scaled_rect

    """-------"""

    def draw(self, screen):
        if self.draw_player:
            #pygame.draw.rect(screen, (0,0,255), self.rect)
            screen.blit(self.image, self.rect)
            

            if self.knocked_out:
                screen.blit(self.knocked_out_animation[self.game.frame % 3] , (self.rect.x, self.rect.top - 10))
            
            if self.is_flying() and self.image == self.shoot_jump_image:
                self.image = self.right_image
   

            self.draw_jetpack(screen)
            self.draw_propeller(screen)
            self.draw_shield(screen)
            self.draw_spring_shoes(screen)
                
    def draw_jetpack(self, screen):
        if self.using_jetpack:
            x = self.rect.x

            x = x-5 if self.right else x+35
 
            frame = self.game.frame
            if frame < 16:
                image = Jetpack.START_ANIMATION[frame % 3]
            elif frame < 147: 
                image = Jetpack.MAIN_BLAST[frame % 3]
            elif frame < 155:
                image = Jetpack.END_ANIMAITON[frame % 3]
            else:
                image = Jetpack.DEFAULT_ROCKET

            if self.paused:
                image = Jetpack.MAIN_BLAST[2]

            if self.right:
                image = pygame.transform.flip(image, True, False)

            screen.blit(image, (x, self.rect.y + 20))
    
    def draw_propeller(self, screen):
        if self.using_propeller:
            frame = self.game.frame
            if self.paused:
                image = Propeller.PROPELLERS[2]
            else:
                image = Propeller.PROPELLERS[frame % 4]

            screen.blit(image, (self.rect.centerx - 15, self.rect.top - 3))

    def draw_shield(self, screen):

        if self.using_shield:
            excess_x = 0
            excess_y = 0

            if self.image in (self.shoot_image, self.shoot_jump_image):
                excess_y = -5
                excess_x = -5
            elif self.image in (self.left_image, self.left_jump_image):
                excess_x = -10 
            
            screen.blit(self.shield, (self.rect.x + excess_x, 
                                      self.rect.y + excess_y))
             
    def draw_spring_shoes(self, screen):

        if self.using_spring_shoes:
            excess_x = 5 if self.right else 0
            excess_y = 3 if self.jumping else 0
            image = SpringShoes.DECOMPRESSED_IMAGE if self.jumping else SpringShoes.DEFAULT_IMAGE
            if self.right:
                image = pygame.transform.flip(image, True, False)
            screen.blit(image, (self.rect.x + 15 + excess_x , self.rect.bottom - 5 + excess_y))



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