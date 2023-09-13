import pygame
from pygame.locals import *
import Assets.colours as colours
import Assets.sounds as sounds
from random import choice, randint
from Sprites.Power_ups.jetpack import Jetpack
from Sprites.Power_ups.propeller import Propeller
from Sprites.Power_ups.shield import Shield
from Sprites.Power_ups.spring_shoes import SpringShoes
from Sprites.blackhole import Blackhole
from Sprites.ufo import UFO

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
        self.all_platforms = game.all_platforms
        self.enemies = game.enemies

        self.default_x = self.x = x
        self.default_y = self.y = -900
        self.previous_y_difference = int(self.y - self.CENTER_Y)

        self.speed = 5 
        
        self.left_image = pygame.image.load(f"Assets/Images/Player/{texture.folder_name}/Body/left.png").convert_alpha()
        self.left_jump_image = pygame.image.load(f"Assets/Images/Player/{texture.folder_name}/Body/left_jump.png").convert_alpha()
        
        self.right_image = pygame.image.load(f"Assets/Images/Player/{texture.folder_name}/Body/right.png").convert_alpha()
        self.right_jump_image = pygame.image.load(f"Assets/Images/Player/{texture.folder_name}/Body/right_jump.png").convert_alpha()
        
        self.shoot_image = pygame.image.load(f"Assets/Images/Player/{texture.folder_name}/Body/shoot.png").convert_alpha()
        self.shoot_jump_image = pygame.image.load(f"Assets/Images/Player/{texture.folder_name}/Body/shoot_jump.png").convert_alpha()
      
        self.shield = pygame.image.load(f"Assets/Images/Player/shield.png").convert_alpha()
    
        self.prior_image = self.image = self.right_image
        
        
        self.original_rect = self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.center = (self.x, game.CENTER_Y)


        
        self.stars_1 = pygame.image.load("Assets/Images/Animations/Stars/1.png").convert_alpha()
        self.stars_2 = pygame.image.load("Assets/Images/Animations/Stars/2.png").convert_alpha()
        self.stars_3 = pygame.image.load("Assets/Images/Animations/Stars/3.png").convert_alpha()
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
    

        self.left = False
        self.right = True
        self.suction_object_collided_with = None
        self.suction_object_collision = False
        self.dead_by_suction = False
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

    def update_image(self):
        self.image = pygame.image.load(f"Assets/Images/Player/{texture.folder_name}/Body/right.png")

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
            self.update_spawning_properties()
            
            self.fall_check()
            self.y_boundary_check()
            self.x_boundary_check()
            self.spring_shoe_check()

            self.update_rect()
            self.update_other_sprites_based_upon_player_jump_difference()
        
        elif self.suction_object_collision:
            self.suck_player_to_center_of_object()
        
        
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
 
        if not self.suction_object_collision:
            self.velocity_y += self.GRAVITY
            self.y += self.velocity_y

            #Gravity update
            if (self.velocity_y > self.GRAVITY) and not self.falling:  
                self.falling = True 
                self.fall_y = self.y
                self.end_game_y = self.y + 450 + self.image.get_height() + 10
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

    def update_spawning_properties(self):
        self.game.enemy_weight = self.score / 100000
       
 
        if 1000 < self.score <= 10000:
            self.game.tile_weights[0] = 250
            
      
        elif 10000 < self.score <= 20000:
            self.game.tile_weights[0] = 100
            self.game.max_tile_number = 20
            

        elif 20000 < self.score <= 30000:
            self.game.tile_weights[0] = 50
            self.game.max_tile_number = 17
            

        else:
            self.game.tile_weights[0] = 5
           
        


    
    def fall_check(self):
        if self.y >= self.end_game_y and not self.check_fall:

            if self.y < 390:
                difference = abs(self.y) - 900
                self.y = -900
                for group in self.all_platforms:
                    for platform in group.sprites():
                        platform.rect.y += difference
                        if platform.power_up:
                            platform.power_up.rect.y += difference

                for group in self.enemies:
                    for enemy in group.sprites():
                        enemy.rect.y += difference

            if not self.suction_object_collided_with:
                sounds.fall.play()
                
            self.check_fall = True


    def y_boundary_check(self):
        if self.rect.top >= 900:
            self.rect.y = 900
            self.velocity_y = 0
            self.dead = True
            self.game.end_game = True    
            self.game.draw_bottom = True  
    
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
            
            for group in self.all_platforms:
                for platform in group.sprites():
                    platform.rect.y -= difference
                    if platform.power_up:
                        platform.power_up.rect.y -= difference
            
            for group in self.enemies:
                for enemy in group.sprites():
                    enemy.rect.y -= difference

            self.rect.y = (self.SCREEN_HEIGHT // 2 - self.rect.height)
   
    def suck_player_to_center_of_object(self):
        
        def resize_image(scale):
            return pygame.transform.scale(self.image, (int(self.rect.width * scale), int(self.rect.height * scale)))

        if isinstance(self.suction_object_collided_with, Blackhole):
            suction_location = (self.suction_object_collided_with.rect.centerx, 
                                self.suction_object_collided_with.rect.centery)
        elif isinstance(self.suction_object_collided_with, UFO):
            suction_location = (self.suction_object_collided_with.rect.centerx, 
                                self.suction_object_collided_with.rect.top)

        
        if self.suction_object_collision and (self.rect.x, self.rect.y) != suction_location:
            dx = suction_location[0] - self.rect.centerx
            dy = suction_location[1] - self.rect.centery
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
            excess_y = 13 if texture.file_name == "ooga" else 0
 
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

            screen.blit(image, (x, self.rect.y + 20 + excess_y))
    
    def draw_propeller(self, screen):
        if self.using_propeller:

            frame = self.game.frame
            if self.paused:
                image = Propeller.PROPELLERS[2]
            else:
                image = Propeller.PROPELLERS[frame % 4]

            screen.blit(image, (self.rect.centerx - 15,
                                self.rect.top - 3))

    def draw_shield(self, screen):

        if self.using_shield:
            excess_x = 0
            excess_y = 0

            
            if texture.file_name == "ooga": 
                if self.image in (self.right_image, self.right_jump_image):
                    excess_x = -5
                if self.image in (self.shoot_image, self.shoot_jump_image):
                    excess_x = -5
                excess_y = 2
            elif self.image in (self.shoot_image, self.shoot_jump_image):
                excess_y = -5
                excess_x = -5
            elif self.image in (self.left_image, self.left_jump_image):
                excess_x = -10 
            screen.blit(self.shield, (self.rect.x + excess_x, 
                                      self.rect.y + excess_y))
             
    def draw_spring_shoes(self, screen):
        if self.using_spring_shoes:
            if self.image in (self.shoot_image, self.shoot_jump_image):
                image = SpringShoes.SHOOT_COMPRESSED if self.jumping else SpringShoes.SHOOT_IMAGE
                excess_y = 3 if self.jumping else 0
                screen.blit(image, (self.rect.x + 15, self.rect.bottom - 5 + excess_y))

            else:
                excess_x = 5 if self.right else 0
                excess_y = 3 if self.jumping else 0
                image = SpringShoes.COMPRESSED_IMAGE if self.jumping else SpringShoes.DEFAULT_IMAGE
                if self.right:
                    image = pygame.transform.flip(image, True, False)
                screen.blit(image, (self.rect.x + 15 + excess_x , self.rect.bottom - 5 + excess_y))



class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load(f"Assets/Images/Projectiles/{texture.file_name}.png")
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
    def update(self):
        self.rect.y -= 15
        if self.rect.bottom < 0:
            self.kill()
    
