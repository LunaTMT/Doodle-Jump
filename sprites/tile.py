import pygame
import random

import assets.sounds as sounds

from sprites.power_ups.propeller import Propeller
from sprites.power_ups.rocket import Rocket
from sprites.power_ups.shield import Shield
from sprites.power_ups.spring_shoes import SpringShoes
from sprites.power_ups.spring import Spring
from sprites.power_ups.trampoline import Trampoline


class Tile(pygame.sprite.Sprite):

    ID = 0

    SPRITE_SHEET = pygame.image.load("Doodle_Jump/assets/images/game-tiles.png")
    DEFAULT_IMAGE = SPRITE_SHEET.subsurface(pygame.Rect(2, 0, 58, 18))  # Extract a 32x32 sprite
    LARGE_DEFAULT_IMAGE =  pygame.image.load("Doodle_Jump/assets/images/tiles/large_default.png")
    MOVING_TILE_IMAGE  = SPRITE_SHEET.subsurface(pygame.Rect(2, 19, 58, 17)) 
    DISAPPEARING_TILE_IMAGE  = SPRITE_SHEET.subsurface(pygame.Rect(2, 55, 58, 17)) 
    SHIFTING_TILE_IMAGE  = SPRITE_SHEET.subsurface(pygame.Rect(2, 182, 58, 17)) 
    MOVEABLE_TILE_IMAGE  = SPRITE_SHEET.subsurface(pygame.Rect(150, 305, 80, 35)) 

    BROKEN_TILE_IMAGE  = SPRITE_SHEET.subsurface(pygame.Rect(2, 73, 60, 17)) 
    BROKEN_TILE_IMAGE_1  = SPRITE_SHEET.subsurface(pygame.Rect(0, 90, 62, 20)) 
    BROKEN_TILE_IMAGE_2  = SPRITE_SHEET.subsurface(pygame.Rect(0, 116, 62, 27)) 
    BROKEN_TILE_IMAGE_3  = SPRITE_SHEET.subsurface(pygame.Rect(0, 148, 62, 32)) 

    def __init__(self, game, x, y):
        super().__init__()
        self.game = game
        self.SCREEN_HEIGHT = game.SCREEN_HEIGHT
        self.SCREEN_WIDTH = game.SCREEN_WIDTH
        
        self.CENTER_X = game.CENTER_X
        self.player = game.player

        self.x = x
        self.y = y
        self.image = self.DEFAULT_IMAGE 
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.center = (self.x, self.y)
        self.power_up = None

        if not isinstance(self, BrokenTile) and Tile.ID != 0:
            self.generate_power_up()

        if isinstance(self, MoveableTile):
            self.game.movable_platforms.add(self)
        else:
            self.game.platforms.add(self)

        Tile.ID += 1


    def generate_power_up(self):
        power_ups = [None, Propeller, Rocket, Shield, SpringShoes, Spring, Trampoline]
        power_ups = [Rocket, Trampoline, Spring, Propeller, Shield, SpringShoes, None]
        power_up = random.choices(population = power_ups, weights=[0, 0, 0, 0, 10, 50, 80])[0]
        #weights=[0.5, 5, 10, 0.8, 10, 10, 80]
        if power_up:
            x = random.randint(self.rect.topleft[0] + 20 , self.rect.topright[0] - 20)
            self.power_up = power_up(self.game, self, x, self.rect.centery)

    def update(self):
        self.death_check()
        self.player_collision_check()
        self.power_up_check()

    def power_up_check(self):
        if self.power_up:
            self.power_up.update()

    def player_collision_check(self):
        collision = pygame.sprite.collide_rect(self.player, self)
        if (collision 
            and self.player.falling 
            and (self.player.rect.bottom > self.rect.top)
            and not self.player.paused):
            self.player.jump()

    def death_check(self):
        if self.rect.y > self.SCREEN_HEIGHT:
            self.game.generate_tiles(1, top=True, tile_type = type(self))
            self.kill()

    def draw(self, screen):
        screen.blit(self.image, self.rect)
                         
        if self.power_up:
            self.power_up.draw(screen)
        

class BrokenTile(Tile):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.image = self.BROKEN_TILE_IMAGE
        self.start = self.y
        self.velocity = [0, 0]  # Initial velocity
        self.gravity = 0.2
        self.fall = False
    
    def update(self):
        self.death_check()
        self.player_collision_check()
        self.fall_check()

    
    def fall_check(self):
        if self.fall:
            self.velocity[1] += self.gravity
            self.rect.move_ip(self.velocity[0], self.velocity[1])

            if self.velocity[1] < 2:
                self.image = self.BROKEN_TILE_IMAGE_1
            elif self.velocity[1] < 3:
                self.image = self.BROKEN_TILE_IMAGE_2
            elif self.velocity[1] < 4:
                self.image = self.BROKEN_TILE_IMAGE_3

    def player_collision_check(self):
        if not self.fall:
            collision = pygame.sprite.collide_rect(self.player, self)
            if collision and self.player.falling and not self.player.paused:
                sounds.tile_break.play()
                self.fall = True
                
class MovingTile(Tile):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.velocity = random.choice([-1, 1])  # -1 for left, 1 for right
        self.speed = random.randint(1, 4)
        self.image = self.MOVING_TILE_IMAGE
        self._generate_boudaries()
        self.paused = False

    def update(self):
        if not self.player.paused:
            self.rect.x += self.velocity * self.speed
            if self.power_up:
                self.power_up.rect.x += self.velocity * self.speed
            
            self.boundary_check()
            self.death_check()
            self.player_collision_check()
            self.power_up_check()

    def boundary_check(self):
        if self.rect.right > self.max_right:
            self.rect.right = self.max_right
            self.velocity *= -1
        
        elif self.rect.left < self.max_left:
            self.rect.left = self.max_left
            self.velocity *= -1

    def _generate_boudaries(self):
        max_left = random.randint(0, self.CENTER_X)
        max_right = random.randint(self.CENTER_X + 1, 640)
        
        while max_right - max_left < 150:
            max_left = random.randint(0, self.CENTER_X )
            max_right = random.randint(self.CENTER_X + 1 + 1, 640)
        
        self.max_left = max_left
        self.max_right = max_right

class DisappearingTile(Tile):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.image = self.DISAPPEARING_TILE_IMAGE

    def player_collision_check(self):
        collision = pygame.sprite.collide_rect(self.player, self)
        if collision and self.player.falling and not self.player.paused:
            sounds.tile_disappear.play()
            self.player.jump()
            self.game.generate_tiles(1, top=True, tile_type = type(self))
            self.kill()

class ShiftingTile(Tile):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.image = self.SHIFTING_TILE_IMAGE
        self.shift = False
        self.move_speed = 5

        self.upper_bound = self.SCREEN_WIDTH - self.rect.width 
        self.lower_bound = self.rect.width

    def update(self):
        self.death_check()
        self.player_collision_check()
        self.shift_check()
        self.power_up_check()


    def player_collision_check(self):
        collision = pygame.sprite.collide_rect(self.player, self)
        if collision and self.player.falling and not self.player.paused:
            
            target_x = random.randint(self.lower_bound, self.upper_bound)
            while self.rect.left - 50 < target_x < self.rect.right + 50:
                target_x = random.randint(self.lower_bound, self.upper_bound)

            self.target_x = target_x
            self.player.jump()
            self.shift = True

    def shift_check(self):
        if self.shift:
            if self.rect.x < self.target_x:
                self.rect.x += 5

                if self.power_up:
                    self.power_up.rect.x += 5

            elif self.rect.x > self.target_x:
                self.rect.x -= 5
            
                if self.power_up:
                    self.power_up.rect.x -= 5

            if self.target_x - 5 <= self.rect.x <= self.target_x + 5:
                self.shift = False
             
class MoveableTile(Tile):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.image = self.MOVEABLE_TILE_IMAGE
        self.moving = False
        self.moved = False
        if self.power_up:
            self.power_up.rect.x = self.rect.x + 20
            self.power_up.rect.y += 6

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not self.moved:
            if self.rect.collidepoint(event.pos):
                self.moving = True
                self.offset_x = event.pos[0] - self.rect.x
                self.offset_y = event.pos[1] - self.rect.y
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.moving:
            self.moving = False
            self.moved = True

    def update(self):
        self.death_check()
        self.player_collision_check()
        self.check_moving()
        self.power_up_check()

    
    def player_collision_check(self):
        collision = pygame.sprite.collide_rect(self.player, self)
        if collision and self.player.falling and not self.player.paused:
            self.player.jump()
           
            if self.moving:
                self.moving = False
                self.moved = True


    def check_moving(self):
        if self.moving:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            self.rect.x = mouse_x - self.offset_x
            self.rect.y = mouse_y - self.offset_y

            if self.power_up:
                self.power_up.rect.x = mouse_x - self.offset_x + 20
                self.power_up.rect.y = mouse_y - self.offset_y