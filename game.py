import pygame
import sys
import assets.colours as colours
import assets.sounds as sounds
from random import choice, randint

from tile import Tile, MovingTile, BrokenTile, DisappearingTile, ShiftingTile, MoveableTile
from buttons.pause_button import PauseButton
from buttons.resume_button import ResumeButton
from buttons.play_button import PlayButton

from sprites.player import Player
from sprites.menu_player import MenuPlayer
from sprites.monster import Monster

class Game:

    SCREEN_WIDTH = 640
    SCREEN_HEIGHT = 900
    CENTER_X = SCREEN_WIDTH // 2
    CENTER_Y = SCREEN_HEIGHT // 2
    GRAVITY = 0.4 # Adjust gravity strength
    JUMP_STRENGTH = -15  # Adjust jump strength

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    BACKGROUND_IMAGE = pygame.image.load("Doodle_Jump/assets/images/backgrounds/background.png")
    TOP_IMAGE =  pygame.image.load("Doodle_Jump/assets/images/backgrounds/top.png").convert_alpha()
    MAIN_MENU_IMAGE = pygame.image.load("Doodle_Jump/assets/images/backgrounds/main_menu.png").convert_alpha()

    pygame.display.set_caption("Doodle Jump")
    clock = pygame.time.Clock()

    all_sprites = pygame.sprite.Group()
    movable_platforms = pygame.sprite.Group()
    platforms = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    monsters = pygame.sprite.Group()


    def __init__(self):
        self.running = True
        self.main_menu = True
        self.play_game = False
        
        self.player = MenuPlayer(self, 110, 750)
        self.main_menu_platform = Tile(self, 140, 763)
        self.play_button = PlayButton(self)
        
    
        
    def initialise_game_objects(self):
        self.resume_button = ResumeButton(self)
        self.pause_button = PauseButton(self)

        
        self.monsters.add(Monster(self))
        self.generate_tiles(n=10)
        self.generate_tiles(n=1, top=False, tile_type=MovingTile)
        self.generate_tiles(n=1, top=False, tile_type=ShiftingTile)
        self.generate_tiles(n=1, top=False, tile_type=MoveableTile)
        self.generate_tiles(n=3, top=False, tile_type=DisappearingTile)
        self.generate_tiles(n=1, top=False, tile_type=BrokenTile)

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
            
    

    def update(self):
        
        
        if self.main_menu:
            self.player.update()
            self.play_button.update()
            self.main_menu_platform.update()
           

        if self.play_game:
            self.bullets.update()
            self.movable_platforms.update()
            self.platforms.update()
            self.player.update()
            self.monsters.update()

        
    def draw(self):
        if self.main_menu:
            self.draw_main_menu()
            self.play_button.draw(self.screen)
            self.player.draw(self.screen)

        if self.play_game:
            self.screen.fill(colours.WHITE)
            self.screen.blit(self.BACKGROUND_IMAGE, (0, 0))

            self.bullets.draw(self.screen)
            self.movable_platforms.draw(self.screen)
            self.platforms.draw(self.screen)
            self.player.draw(self.screen)
            self.monsters.draw(self.screen)
            
            self.draw_top()
            self.pause_button.draw(self.screen)
            self.resume_button.draw(self.screen)

        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()

    def generate_tiles(self, n, top=False, tile_type=Tile):
        
        """Need to change this function because the collision detections and spawning is working fully"""
        for _ in range(n):
            
            x, y = randint(90, self.SCREEN_WIDTH - 90), (0 if top else randint(0, self.SCREEN_HEIGHT))
            new_platform_rect = pygame.Rect(x, y, 90, 40)

            while any(new_platform_rect.colliderect(platform) for platform in  self.movable_platforms.sprites()):
                print("collision")
                x, y = randint(90, self.SCREEN_WIDTH - 90), (0 if top else randint(0, self.SCREEN_HEIGHT))
                new_platform_rect = pygame.Rect(x, y, 90, 40)

            platform = tile_type(self, x, y)
            
            if tile_type == MoveableTile:
                self.movable_platforms.add(platform)
            else:
                self.platforms.add(platform)


    def draw_top(self):
        self.screen.blit(self.TOP_IMAGE, (0, 0))
        
    def draw_main_menu(self):
        self.screen.blit(self.MAIN_MENU_IMAGE, (0, 0))
        self.main_menu_platform.draw(self.screen)



