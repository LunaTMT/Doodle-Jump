import pygame
import sys
import random
import assets.colours as colours
import assets.sounds as sounds
from random import choice, randint

from sprites.tile import Tile, MovingTile, BrokenTile, DisappearingTile, ShiftingTile, MoveableTile
from buttons.pause_button import PauseButton
from buttons.resume_button import ResumeButton
from buttons.play_button import PlayButton
from buttons.play_again_button import PlayAgain
from buttons.menu_button import MenuButton

from sprites.player import Player
from sprites.menu_player import MenuPlayer
from sprites.monster import Monster
from sprites.blackhole import Blackhole

class Game:

    SCREEN_WIDTH = 640
    SCREEN_HEIGHT = 900
    CENTER_X = SCREEN_WIDTH // 2
    CENTER_Y = SCREEN_HEIGHT // 2
    GRAVITY = 0.4 # Adjust gravity strength
    JUMP_STRENGTH = -15  # Adjust jump strength
    
    FRAME_RATE = 60

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    BACKGROUND_IMAGE = pygame.image.load("assets/images/backgrounds/background.png")
    TOP_IMAGE =  pygame.image.load("assets/images/backgrounds/top.png").convert_alpha()
    MAIN_MENU_IMAGE = pygame.image.load("assets/images/backgrounds/main_menu.png").convert_alpha()

    SPRITE_SHEET = pygame.image.load("assets/images/start-end-tiles.png")
    GAME_OVER_TEXT_IMAGE = SPRITE_SHEET.subsurface(pygame.Rect(2, 104, 214, 75))

    END_GAME_BOTTOM_IMAGE = SPRITE_SHEET.subsurface(pygame.Rect(2, 374, 640, 137))

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
 

    def __init__(self):
        self.running = True
        self.main_menu = True
        self.play_game = False
        self.end_game = False

        self.draw_bottom = False
        pygame.init()

        self.fade_out_speed = 4
        self.fade_out_alpha = 255
        self.fade_in_speed = 1
        self.fade_in_alpha = 0

        self.enemy_weight = 0.01
        self.max_tile_number = 0

        self.frame = 0
        self.score_font = pygame.font.Font(None, 50)
        self.quadrants = ("Q1", "Q2", "Q3", "Q4")
        self.quadrant_idx = 0

        self.previous_spawn_x = 0
        self.previous_spawn_y = 0

        self.initialise_main_menu_objects()
        
    def initialise_main_menu_objects(self):
        print(Tile.ID)
        self.player = MenuPlayer(self, 110, 750)
        self.main_menu_platform = Tile(self, 140, 763)
        self.play_button = PlayButton(self)

    def initialise_game_objects(self):
        self.clear_all_sprites()

        self.resume_button = ResumeButton(self)
        self.pause_button = PauseButton(self)
        self.play_again_button = PlayAgain(self)
        self.main_menu_button = MenuButton(self)


        self.player = Player(self, self.CENTER_X, self.CENTER_Y)
        self.generate_n_tiles(n=25, top=False)
 

    def generate_random_tile(self):
        
        if Tile.total <= self.max_tile_number:
            tiles = [Tile, MovingTile, ShiftingTile, MoveableTile, DisappearingTile, BrokenTile]
            tile = random.choices(population = tiles, weights=[60, 10, 10, 2, 10, 10])[0]
            self.generate_n_tiles(n=1, top=True, tile_type=tile)

    def generate_random_enemy(self):
            enemies = [Monster, Blackhole, None]
            enemy = random.choices(population = enemies, weights=[self.enemy_weight, self.enemy_weight, 100])[0]
            if isinstance(enemy, Monster):
                self.monsters.add(enemy(self))
            elif enemy:
                self.blackholes.add(enemy(self))


    def clear_all_sprites(self):
        self.movable_platforms.empty()
        self.platforms.empty()
        self.bullets.empty()
        self.monsters.empty()
        self.blackholes.empty()
        

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if self.main_menu:
                self.play_button.handle_events(event)

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
        if self.main_menu:
            self.player.update()
            self.play_button.update()
            self.main_menu_platform.update()
        
        if self.play_game:
            self.generate_random_tile()
            self.generate_random_enemy()
            self.bullets.update()
            self.movable_platforms.update()
            self.platforms.update()
            self.player.update()
            self.monsters.update()
            self.blackholes.update()
        
        if self.end_game:
            self.play_again_button.update()
            self.main_menu_button.update()
        
    def draw(self):
        if self.main_menu:
            self.draw_main_menu()
            self.play_button.draw(self.screen)
            self.player.draw(self.screen)

        if self.play_game:
            self.screen.blit(self.BACKGROUND_IMAGE, (0, 0))

            self.bullets.draw(self.screen)
            self.player.draw(self.screen)
            
            for platform in (self.movable_platforms.sprites() + self.platforms.sprites()):
                platform.draw(self.screen)
                
            for sprite in (self.monsters.sprites() + self.blackholes.sprites()):
                sprite.draw(self.screen)
        
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
                high_score_x = (self.SCREEN_WIDTH - high_score_width) // 2

                self.screen.blit(score,      (score_x,      (self.CENTER_Y * 0.626)))
                self.screen.blit(high_score, (high_score_x, (self.CENTER_Y * 0.93)))
                
                self.screen.blit(self.YOUR_SCORE_IMAGE,      (self.YOUR_SCORE_IMAGE_x,       self.CENTER_Y * 0.5))
                self.screen.blit(self.YOUR_HIGH_SCORE_IMAGE, (self.YOUR_HIGH_SCORE_IMAGE_x, (self.CENTER_Y * 0.75)))
    
                self.play_again_button.draw(self.screen)
                self.main_menu_button.draw(self.screen)

            if self.draw_bottom and not self.player.dead_by_blackhole:
                self.screen.blit(self.END_GAME_BOTTOM_IMAGE, (0, 763))

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

    def generate_n_tiles(self, n, top=False, tile_type=Tile):
        

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

            if top:
                y = (randint((y_lower + y_lower_bound - minus), 
                             (y_higher + y_upper_bound - minus)))
            else:
                y = randint(0, 840)
            
            return (x, y)

        sprites_list = (self.platforms.sprites() + self.movable_platforms.sprites() + self.blackholes.sprites())
        
        for _ in range(n):
            x, y = get_random_quadrant_coordinates()
            new_platform = pygame.Rect(x, y, 90, 40)

            while (any(new_platform.colliderect(sprite) for sprite in sprites_list)):
                x, y = get_random_quadrant_coordinates()
                new_platform = pygame.Rect(x, y, 90, 40)


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
        self.screen.blit(score_text, (20, 20))

