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
    GRAVITY = 0.4 
    JUMP_STRENGTH = -15  
    
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    #BACKGROUND IMAGES
    MAIN_MENU_IMAGE = BACKGROUND_IMAGE = pygame.image.load("Assets/Images/Backgrounds/main_menu.png").convert_alpha()
    OPTIONS_IMAGE = pygame.image.load("Assets/Images/Backgrounds/options.png").convert_alpha()
    PLAY_GAME_IMAGE = pygame.image.load(f"Assets/Images/Backgrounds/Backgrounds/{texture.file_name}.png")

    #TOP IMAGES
    TOP_SHEET = pygame.image.load(f"Assets/Images/Backgrounds/Tops/{texture.file_name}.png")
    TOP_IMAGE =  TOP_SHEET.subsurface(pygame.Rect(0, 0, 640, 92))

    #END GAME IMAGES
    END_GAME_SPRITE_SHEET = pygame.image.load("Assets/Images/start-end-tiles.png")
 
    GAME_OVER_TEXT_IMAGE = END_GAME_SPRITE_SHEET.subsurface(pygame.Rect(2, 209, 433, 157))
    GAME_OVER_TEXT_IMAGE_x = CENTER_X - (GAME_OVER_TEXT_IMAGE.get_width() // 2)


    END_GAME_BOTTOM_IMAGE = pygame.image.load(f"Assets/Images/Backgrounds/Bottoms/{texture.file_name}.png")
    END_GAME_BOTTOM_IMAGE_Y = SCREEN_HEIGHT - END_GAME_BOTTOM_IMAGE.get_height()

    YOUR_SCORE_IMAGE = END_GAME_SPRITE_SHEET.subsurface(pygame.Rect(795, 339, 218, 40))
    YOUR_SCORE_IMAGE_width, YOUR_SCORE_IMAGE_height = YOUR_SCORE_IMAGE.get_size()
    YOUR_SCORE_IMAGE_x = (SCREEN_WIDTH - YOUR_SCORE_IMAGE_width) // 2
    YOUR_SCORE_IMAGE_y = (SCREEN_HEIGHT - YOUR_SCORE_IMAGE_height) // 2

    YOUR_HIGH_SCORE_IMAGE = END_GAME_SPRITE_SHEET.subsurface(pygame.Rect(677, 393, 310, 56))
    YOUR_HIGH_SCORE_IMAGE_width, YOUR_HIGH_SCORE_IMAGE_height = YOUR_HIGH_SCORE_IMAGE.get_size()
    YOUR_HIGH_SCORE_IMAGE_x = (SCREEN_WIDTH - YOUR_HIGH_SCORE_IMAGE_width) // 2
    YOUR_HIGH_SCORE_IMAGE_y = (SCREEN_HEIGHT - YOUR_HIGH_SCORE_IMAGE_height) // 2
    
    END_GAME_IMAGES = (YOUR_SCORE_IMAGE, YOUR_HIGH_SCORE_IMAGE)

 
    pygame.display.set_caption("Doodle Jump")
    clock = pygame.time.Clock()

    def __init__(self):
        self.running = True
        self.main_menu = True
        self.options_menu = False
        self.play_game = False
        self.end_game = False


        pygame.init()

        self.movable_platforms = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.monsters = pygame.sprite.Group()
        self.blackholes = pygame.sprite.Group()
        self.UFOs = pygame.sprite.Group()
        
        self.all_enemies = [self.monsters, self.blackholes, self.UFOs]
        self.all_platforms = [self.movable_platforms, self.platforms]

        self.fade_out_speed = 3
        self.fade_out_alpha = 255

        self.frame = 0
        self.score_font = pygame.font.Font(None, 50)
        self.quadrants = ("Q1", "Q2", "Q3", "Q4")
        self.quadrant_idx = 0

        self.previous_spawn_x = 0
        self.previous_spawn_y = 0

  
        self.tile_objects = [Tile, MovingTile, ShiftingTile, MoveableTile, DisappearingTile, BrokenTile, ExplodingTile]
        self.enemy_objects = [Monster, Blackhole, UFO]
       

        self.initialise_main_menu_objects()
        
     # getter method
    
    @property
    def all_enemies(self):
        return [enemy for group in self._all_enemies for enemy in group.sprites()]
    
    @all_enemies.setter
    def all_enemies(self, value):
        self._all_enemies = value
    
    @property
    def all_platforms(self):
        return [platform for group in self._all_platforms for platform in group.sprites()]
    

    @all_platforms.setter
    def all_platforms(self, value):
        self._all_platforms = value
            
    """Initialise/Reinitialise Functions"""
    def initialise_main_menu_objects(self):
        self.player = MenuPlayer(self, 110, 750)

        self.platforms.add(Tile(self, 115, 763))
        self.UFOs.add(UFO(self, x=450, y=200))
        
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
    
    def initialise_game_weights(self):
        self.max_tile_number = 25
        self.tile_weights = [9999999, 5, 5, 1, 5, 5, 5] 

        self.max_enemy_number = 1
        self.enemy_weight = 0.001

    """Generator Functions """
    def generate_random_tile(self):
        if Tile.total <= self.max_tile_number:
            #print(self.tile_weights)
            tile = random.choices(population=self.tile_objects, weights=self.tile_weights)[0]
            self.generate_n_tiles(top=True, tile_type=tile)

    def generate_random_enemy(self):
        if len(self.all_enemies) < self.max_enemy_number:
            if not self.player.paused:
                enemy = random.choices(population=self.enemy_objects + [None], weights=[self.enemy_weight, self.enemy_weight, self.enemy_weight, 100])[0]
                if enemy is Monster:
                    self.monsters.add(enemy(self))
                elif enemy is Blackhole:
                    self.blackholes.add(enemy(self))   
                elif enemy is UFO:
                    self.UFOs.add(enemy(self))
                else:
                    pass

    def generate_n_tiles(self, n=1, top=False, tile_type=Tile):
        
        def get_quadrant_range(quadrant):
            match quadrant:
                case "Q1":
                    return ((0, 320),   (0, 450))
                case "Q2":
                    return ((320, 640), (0, 450))
                case "Q3":
                    return ((0, 320),   (450, 900))
                case "Q4":
                    return ((320, 640), (450, 900))
        def get_random_quadrant_coordinates():
            current_quadrant = self.quadrants[self.quadrant_idx % 4]
            x_range, y_range = get_quadrant_range(current_quadrant)
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
                case "Q2":
                    x_upper_bound = -60
                    y_lower_bound = 20
                case "Q3":
                    x_lower_bound = 60
                    y_upper_bound = -20
          
                case "Q4":
                    x_upper_bound = -60
                    y_upper_bound = -20
            
                
            x = randint(x_lower + x_lower_bound, x_higher + x_upper_bound)
            y = (randint((y_lower  - y_lower_bound -  900), 
                         (y_higher  - y_upper_bound - 900)))
        
            return (x, y)

        for _ in range(n):
            valid = False
            while not valid:
                valid = True
                x, y = get_random_quadrant_coordinates() if top else (randint(65, self.SCREEN_WIDTH-65), randint(-450, self.SCREEN_HEIGHT-25)) 
                new_platform = pygame.Rect(x, y, 60, 20)
                center1 = new_platform.center

                for sprite in (self.all_platforms + self.all_enemies):
                    center2 = sprite.rect.center
                    distance = sqrt((center1[0] - center2[0]) ** 2 + (center1[1] - center2[1]) ** 2)

                    if new_platform.colliderect(sprite.rect) or distance < 120:
                        valid = False
                        break

            tile_type(self, x, y)
            self.quadrant_idx += 1


    def clear_all_sprites(self):
        self.movable_platforms.empty()
        self.platforms.empty()
        self.bullets.empty()
        self.monsters.empty()
        self.blackholes.empty()
        self.UFOs.empty()
        


    def draw_top(self):
        self.screen.blit(self.TOP_IMAGE, (0, 0))

        score_text = self.score_font.render(str(int(self.player.score)), True, colours.BLACK)
        self.screen.blit(score_text, (30, 18))

        self.pause_button.draw(self.screen)
        self.resume_button.draw(self.screen)
        
    def draw_end_game_screen(self):
        self.draw_top()

        score = self.score_font.render(str(int(self.player.score)), True, colours.BLACK)
        score_x = (self.SCREEN_WIDTH - score.get_width()) // 2

        high_score = self.score_font.render(str(int(Player.high_score)), True, colours.BLACK)  
        high_score_x = self.CENTER_X - (high_score.get_width() // 2)

        self.screen.blit(score,      (score_x,      (self.CENTER_Y * 0.826)))
        self.screen.blit(high_score, (high_score_x, (self.CENTER_Y * 1.13)))
        
        self.screen.blit(self.YOUR_SCORE_IMAGE,      (self.YOUR_SCORE_IMAGE_x,       self.CENTER_Y * 0.7))
        self.screen.blit(self.YOUR_HIGH_SCORE_IMAGE, (self.YOUR_HIGH_SCORE_IMAGE_x, (self.CENTER_Y * 0.95)))
        self.screen.blit(self.GAME_OVER_TEXT_IMAGE, (self.GAME_OVER_TEXT_IMAGE_x, 140))

        self.play_again_button.draw(self.screen)
        self.main_menu_button.draw(self.screen)

    @classmethod
    def update_top_images(cls):
        cls.TOP_SHEET = pygame.image.load(f"Assets/Images/Backgrounds/Tops/{texture.file_name}.png")
        cls.TOP_IMAGE =  cls.TOP_SHEET.subsurface(pygame.Rect(0, 0, 640, 92))

    @classmethod
    def update_bottom_images(cls):
        cls.END_GAME_BOTTOM_IMAGE = pygame.image.load(f"Assets/Images/Backgrounds/Bottoms/{texture.file_name}.png")
        cls.END_GAME_BOTTOM_IMAGE_Y = cls.SCREEN_HEIGHT - cls.END_GAME_BOTTOM_IMAGE.get_height()

    
    """Main game loop functions
    
    For each of the three functions there are 3 games states that comprise the entire game:
    - main_menu
    - play_game
    - end_game
    
    Each function comrpises the games elements for that given state.
    For example:
    The main menu state will contain all objects that are relevant to the main menu.
    Such as the play and options buttons as well as the unmovable player and the ufo in the top right.

    The handle events function will handle all events made by the player for the objects of that given state
    highlighting over the play button is a user event and causes the button image to change (highlight image)

    The update function updates all objects for every frame of the game running.
    For example for each frame the player is affected by gravity and his y coordinate should be updated for every frame 

    The draw functions simply blits to the screen the associated images/shapes for these objects
    For example the play button image, the player image 
    """
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if self.main_menu:
                self.play_button.handle_events(event)
                self.options_button.handle_events(event)
                
                if self.options_menu:
                    self.main_menu_button.handle_events(event)

            elif self.play_game:
                self.pause_button.handle_events(event)
                self.resume_button.handle_events(event)
                self.player.handle_events(event)
                
                for platform in self.movable_platforms:
                        platform.handle_events(event)
            
            elif self.end_game:
                self.play_again_button.handle_events(event)
                self.main_menu_button.handle_events(event)
    
    def update(self):

        if self.main_menu:
            self.player.update()
            self.platforms.update()
            self.UFOs.update()
            
            self.play_button.update()
            self.options_button.update()
            if self.options_menu: self.main_menu_button.update()

        elif self.play_game:
 
            self.generate_random_tile()
            self.generate_random_enemy()

            self.bullets.update()
            self.movable_platforms.update()
            self.platforms.update()
            self.player.update()
            self.monsters.update()
            self.blackholes.update()
            self.UFOs.update()

        elif self.end_game:
            self.play_again_button.update()
            self.main_menu_button.update()
        
    def draw(self):
        self.screen.blit(self.BACKGROUND_IMAGE, (0, 0))

        if self.main_menu:

            if not self.options_menu:        
                self.play_button.draw(self.screen)
          
            self.options_button.draw(self.screen)
            
            self.player.draw(self.screen)
            self.UFOs.draw(self.screen)
            for platform in self.all_platforms:
                platform.draw(self.screen)

        
            if self.options_menu:
                self.main_menu_button.draw(self.screen)
            

        if self.play_game:

            self.bullets.draw(self.screen)
            self.player.draw(self.screen)
            
            for platform in self.all_platforms:
                platform.draw(self.screen)

            for enemy in self.all_enemies:
                enemy.draw(self.screen)

            self.draw_top()
            
        if self.end_game:
            
            """
            Only once all the sprites have faded do we end the 'play_game' state 
            This line of code saves having to redraw every sprite in the 'end_game' condition
            Instead we simply end the play_game state when their alpha is at 0, i.e. are inivisible.
            """
            if self.fade_out_alpha == 0:
                self.play_game = False
                self.draw_end_game_screen()
                pygame.mixer.stop()     
            
            if self.fade_out_alpha != 0:
                self.fade_out_alpha -= self.fade_out_speed

            #If the player falls to the bottom we want to draw the bottom image to demonstrate falling into the abyss
            if not self.player.dead_by_suction:
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
