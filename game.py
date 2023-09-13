import pygame
import sys
import random
import Assets.colours as colours
import Assets.sounds as sounds
from random import choice, randint
from math import sqrt

from Sprites.tile import Tile, MovingTile, BrokenTile, DisappearingTile, ShiftingTile, MoveableTile, ExplodingTile
from Buttons.pause import PauseButton
from Buttons.resume import ResumeButton
from Buttons.play import PlayButton
from Buttons.options import OptionButton
from Buttons.play_again import PlayAgain
from Buttons.menu import MenuButton

from Sprites.player import Player
from Sprites.menu_player import MenuPlayer
from Sprites.monster import Monster
from Sprites.blackhole import Blackhole
from Sprites.ufo import UFO

import texture

class Game:

    SCREEN_WIDTH = 640
    SCREEN_HEIGHT = 900
    CENTER_X = SCREEN_WIDTH // 2
    CENTER_Y = SCREEN_HEIGHT // 2
    GRAVITY = 0.4 # Adjust gravity strength
    JUMP_STRENGTH = -15  # Adjust jump strength
    
    FRAME_RATE = 60

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    BACKGROUND_IMAGE = pygame.image.load(f"Assets/Images/Backgrounds/Backgrounds/{texture.file_name}.png")
    
    TOP_SHEET = pygame.image.load(f"Assets/Images/Backgrounds/Tops/{texture.file_name}.png")
    TOP_IMAGE =  TOP_SHEET.subsurface(pygame.Rect(0, 0, 640, 92))

    DEFAULT_MAIN_MENU_IMAGE = MAIN_MENU_IMAGE = pygame.image.load("Assets/Images/Backgrounds/main_menu.png").convert_alpha()
    OPTIONS_IMAGE = pygame.image.load("Assets/Images/Backgrounds/options.png").convert_alpha()

    

    SPRITE_SHEET = pygame.image.load("Assets/Images/start-end-tiles.png")
    GAME_OVER_TEXT_IMAGE = SPRITE_SHEET.subsurface(pygame.Rect(2, 104, 214, 75))

    END_GAME_BOTTOM_IMAGE = pygame.image.load(f"Assets/Images/Backgrounds/Bottoms/{texture.file_name}.png")
    END_GAME_BOTTOM_IMAGE_Y = SCREEN_HEIGHT - END_GAME_BOTTOM_IMAGE.get_height()

    YOUR_SCORE_IMAGE = SPRITE_SHEET.subsurface(pygame.Rect(795, 339, 218, 40))
    YOUR_SCORE_IMAGE_width, YOUR_SCORE_IMAGE_height = YOUR_SCORE_IMAGE.get_size()
    YOUR_SCORE_IMAGE_x = (SCREEN_WIDTH - YOUR_SCORE_IMAGE_width) // 2
    YOUR_SCORE_IMAGE_y = (SCREEN_HEIGHT - YOUR_SCORE_IMAGE_height) // 2

    YOUR_HIGH_SCORE_IMAGE = SPRITE_SHEET.subsurface(pygame.Rect(677, 393, 310, 56))
    YOUR_HIGH_SCORE_IMAGE_width, YOUR_HIGH_SCORE_IMAGE_height = YOUR_HIGH_SCORE_IMAGE.get_size()
    YOUR_HIGH_SCORE_IMAGE_x = (SCREEN_WIDTH - YOUR_HIGH_SCORE_IMAGE_width) // 2
    YOUR_HIGH_SCORE_IMAGE_y = (SCREEN_HEIGHT - YOUR_HIGH_SCORE_IMAGE_height) // 2


    END_GAME_IMAGES = (YOUR_SCORE_IMAGE, YOUR_HIGH_SCORE_IMAGE)

 
    pygame.display.set_caption("Doodle Jump")
    clock = pygame.time.Clock()

    movable_platforms = pygame.sprite.Group()
    platforms = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    monsters = pygame.sprite.Group()
    blackholes = pygame.sprite.Group()
    UFOs = pygame.sprite.Group()
    
    enemies = [monsters, blackholes, UFOs]
    all_platforms = [movable_platforms, platforms]

    def __init__(self):
        self.running = True
        self.main_menu = True
        self.options_menu = False
        self.play_game = False
        self.end_game = False

        self.draw_bottom = False
        pygame.init()

        self.fade_out_speed = 3
        self.fade_out_alpha = 255
        self.fade_in_speed = 2
        self.fade_in_alpha = 0

        self.enemy_weight = 0.001
        self.max_tile_number = 25
        self.tile_weights = [500, 5, 5, 1, 5, 10, 5] # Tile, MovingTile, ShiftingTile, MoveableTile, DisappearingTile, BrokenTile, ExplodingTile]

        self.frame = 0
        self.score_font = pygame.font.Font(None, 50)
        self.quadrants = ("Q1", "Q2", "Q3", "Q4")
        self.quadrant_idx = 0

        self.previous_spawn_x = 0
        self.previous_spawn_y = 0

        self.initialise_main_menu_objects()
        
    def initialise_main_menu_objects(self):
        self.player = MenuPlayer(self, 110, 750)
        self.main_menu_platform = Tile(self, 115, 763)
        self.play_button = PlayButton(self)
        self.options_button = OptionButton(self)
        self.main_menu_button = MenuButton(self, x=None, y=200)

    def initialise_game_objects(self):
        Tile.total = 0
        self.clear_all_sprites()

        self.resume_button = ResumeButton(self)
        self.pause_button = PauseButton(self)
        self.play_again_button = PlayAgain(self)
        self.main_menu_button = MenuButton(self, x_multiplier=1.75, y_multiplier=1.5)

        self.player = Player(self, self.CENTER_X, self.CENTER_Y)
        self.generate_n_tiles(n=25, top=False)
 

    def generate_random_tile(self):
        if Tile.total <= self.max_tile_number:
            tiles = [Tile, MovingTile, ShiftingTile, MoveableTile, DisappearingTile, BrokenTile, ExplodingTile]
            tile = random.choices(population=tiles, weights=self.tile_weights)[0]
            self.generate_n_tiles(top=True, tile_type=tile)

    def generate_random_enemy(self):
            if not self.player.paused:
                enemies = [Monster, Blackhole, UFO, None]
                enemy = random.choices(population = enemies, weights=[self.enemy_weight, self.enemy_weight, self.enemy_weight, 100])[0]
                if enemy is Monster:
                    self.monsters.add(enemy(self))
                elif enemy is Blackhole:
                    self.blackholes.add(enemy(self))   
                elif enemy is UFO:
                    self.UFOs.add(enemy(self))
                else:
                    pass


    def clear_all_sprites(self):
        self.movable_platforms.empty()
        self.platforms.empty()
        self.bullets.empty()
        self.monsters.empty()
        self.blackholes.empty()
        self.UFOs.empty()
        
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if self.main_menu:
                self.play_button.handle_events(event)
                self.options_button.handle_events(event)
                
                if self.options_menu:
                    self.main_menu_button.handle_events(event)

            if self.play_game:
                self.pause_button.handle_events(event)
                self.resume_button.handle_events(event)
                self.player.handle_events(event)
                
                for platform in self.movable_platforms:
                        platform.handle_events(event)
            
            if self.end_game:
                self.play_again_button.handle_events(event)
                self.main_menu_button.handle_events(event)
    
    def update(self):
        print(Tile.total)
        if self.main_menu:

            self.player.update()
            self.play_button.update()

            self.main_menu_platform.update()
            self.options_button.update()

            if self.options_menu:
                self.main_menu_button.update()

        if self.play_game:
            self.generate_random_tile()
            self.generate_random_enemy()
            self.bullets.update()
            self.movable_platforms.update()
            self.platforms.update()
            self.player.update()


            self.monsters.update()
            self.blackholes.update()
            self.UFOs.update()

        if self.end_game:
            self.play_again_button.update()
            self.main_menu_button.update()
        
    def draw(self):
        if self.main_menu:

            if not self.options_menu:
                self.draw_main_menu()
                self.play_button.draw(self.screen)
          
            self.options_button.draw(self.screen)
            self.player.draw(self.screen)
            self.main_menu_platform.draw(self.screen)

            if self.options_menu:
                self.main_menu_button.draw(self.screen)
           
        if self.play_game:
            self.screen.blit(self.BACKGROUND_IMAGE, (0, 0))

            self.bullets.draw(self.screen)
            self.player.draw(self.screen)
            
            for group in self.all_platforms:
                for platform in group.sprites():
                    platform.draw(self.screen)
                
            for group in self.enemies:
                for enemy in group.sprites():
                    enemy.draw(self.screen)

            #for sprite in self.UFOs.sprites():
            #    sprite.draw(self.screen)
        
   
            self.draw_top()
            
  
        if self.end_game:
            
           
            if self.fade_out_alpha == 0:
                self.play_game = False
                self.screen.blit(self.BACKGROUND_IMAGE, (0, 0))
                self.draw_top()
                pygame.mixer.stop()     
            
            self.fade_out_alpha -= self.fade_out_speed
            self.fade_in_alpha += self.fade_in_speed

            if self.fade_out_alpha < 0:
                self.fade_out_alpha = 0
            
            if self.fade_out_alpha == 0:

                score = self.score_font.render(str(int(self.player.score)), True, colours.BLACK)
                score_width, score_height = score.get_size()
                score_x = (self.SCREEN_WIDTH - score_width) // 2

                transparent_surface = pygame.Surface((score_width, score_height), pygame.SRCALPHA)
                transparent_surface.fill(colours.WHITE)

                high_score = self.score_font.render(str(int(Player.high_score)), True, colours.BLACK)  
                high_score_width, _ = score.get_size()
                high_score_x = self.CENTER_X - (high_score_width // 2)

                self.screen.blit(score,      (score_x,      (self.CENTER_Y * 0.626)))
                self.screen.blit(high_score, (high_score_x, (self.CENTER_Y * 0.93)))
                
                self.screen.blit(self.YOUR_SCORE_IMAGE,      (self.YOUR_SCORE_IMAGE_x,       self.CENTER_Y * 0.5))
                self.screen.blit(self.YOUR_HIGH_SCORE_IMAGE, (self.YOUR_HIGH_SCORE_IMAGE_x, (self.CENTER_Y * 0.75)))
    
                self.play_again_button.draw(self.screen)
                self.main_menu_button.draw(self.screen)

            if self.draw_bottom and not self.player.dead_by_suction:
                self.screen.blit(self.END_GAME_BOTTOM_IMAGE, (0, self.END_GAME_BOTTOM_IMAGE_Y))

        pygame.display.flip()        
 

        
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.frame += 1
            self.clock.tick(60)

        pygame.quit()
        sys.exit()

    def generate_n_tiles(self, n=1, top=False, tile_type=Tile):
        

        def get_random_quadrant_coordinates():
            current_quadrant = self.quadrants[self.quadrant_idx % 4]
            x_range, y_range = self.get_quadrant_range(current_quadrant)
            x_lower, x_higher = x_range
            y_lower, y_higher = y_range
            
            x_lower_bound = 0
            x_upper_bound = 0
            y_lower_bound = 0
            y_upper_bound = 0

            match current_quadrant:
                case "Q1":
                    x_lower_bound = 60
                    y_lower_bound = 20
                    minus = 450
                 
                case "Q2":
                    x_upper_bound = -60
                    y_lower_bound = 20
                    minus = 450
             
                case "Q3":
                    x_lower_bound = 60
                    y_upper_bound = -20
                    minus = 900
                   
                case "Q4":
                    x_upper_bound = -60
                    y_upper_bound = -20
                    minus = 900
                   
        
            x = randint(x_lower + x_lower_bound, x_higher + x_upper_bound)

            
            y = (randint((y_lower  - y_lower_bound -  minus), 
                         (y_higher  - y_upper_bound - minus)))
            
            
            return (x, y)

        for _ in range(n):
            valid = False
            while not valid:
                valid = True
                x, y = get_random_quadrant_coordinates() if top else (randint(65, self.SCREEN_WIDTH-65), randint(-450, self.SCREEN_HEIGHT-25)) 
                new_platform = pygame.Rect(x, y, 60, 20)
                center1 = new_platform.center

                for sprite in (self.platforms.sprites() + self.movable_platforms.sprites() + self.blackholes.sprites()):
                    center2 = sprite.rect.center
                    distance = sqrt((center1[0] - center2[0]) ** 2 + (center1[1] - center2[1]) ** 2)

                    if new_platform.colliderect(sprite.rect) or distance < 120:
                        valid = False
                        break

            tile_type(self, x, y)
            self.quadrant_idx += 1
        
    def get_quadrant_range(self, quadrant):
        match quadrant:
            case "Q1":
                return ((0, 320),   (0, 450))
            case "Q2":
                return ((320, 640), (0, 450))
            case "Q3":
                return ((0, 320),   (450, 900))
            case "Q4":
                return ((320, 640), (450, 900))

    def draw_top(self):
        self.screen.blit(self.TOP_IMAGE, (0, 0))
        self.draw_score()
        self.pause_button.draw(self.screen)
        self.resume_button.draw(self.screen)
        
    def draw_main_menu(self):
        self.screen.blit(self.MAIN_MENU_IMAGE, (0, 0))
        self.main_menu_platform.draw(self.screen)

    def draw_score(self):
        score_text = self.score_font.render(str(int(self.player.score)), True, colours.BLACK)
        self.screen.blit(score_text, (30, 18))


    def update_top_images(self):
        self.TOP_SHEET = pygame.image.load(f"Assets/Images/Backgrounds/Tops/{texture.file_name}.png")
        self.TOP_IMAGE =  self.TOP_SHEET.subsurface(pygame.Rect(0, 0, 640, 92))

    def update_bottom_images(self):
        self.END_GAME_BOTTOM_IMAGE = pygame.image.load(f"Assets/Images/Backgrounds/Bottoms/{texture.file_name}.png")
        self.END_GAME_BOTTOM_IMAGE_Y = self.SCREEN_HEIGHT - self.END_GAME_BOTTOM_IMAGE.get_height()
