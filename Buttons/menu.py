import pygame
import Assets.sounds as sounds
from Sprites.player import Player

class MenuButton:
    SPRITE_SHEET = pygame.image.load("Assets/Images/start-end-tiles.png")
    DEFAULT_IMAGE = SPRITE_SHEET.subsurface(pygame.Rect(3, 99, 222, 80))
    HOVER_IMAGE = SPRITE_SHEET = pygame.image.load("Assets/Images/Buttons/menu_hover.png")

    def __init__(self, game, x=None, y=None, x_multiplier=1, y_multiplier=1):
        self.game = game
        self.player = game.player
        self.CENTER_X = game.CENTER_X
        self.CENTER_Y = game.CENTER_Y
        self.SCREEN_HEIGHT = game.SCREEN_HEIGHT
        self.SCREEN_WIDTH = game.SCREEN_WIDTH

        self.alpha = 0
        self.image = self.DEFAULT_IMAGE
        self.hover_image = self.HOVER_IMAGE
        
        self.rect = self.image.get_rect()
        
        # Get the dimensions of the image
        image_width, image_height = self.DEFAULT_IMAGE.get_size()

        if x == None:
            x = ((self.SCREEN_WIDTH - image_width) // 2 ) 
        if y == None:
            y = ((self.SCREEN_HEIGHT - image_height) // 2 ) 
            
        self.rect.x = x * x_multiplier
        self.rect.y = y * y_multiplier

        self.hovering = False
        self.clicked = False
        self.hide = False

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        self.hovering = True if self.rect.collidepoint(mouse_pos) else False

        
    def handle_events(self, event):
        if not self.hide:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  
                mouse_pos = pygame.mouse.get_pos()
                if self.rect.collidepoint(mouse_pos):
                    self.clicked = True

            
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.clicked:
                self.clicked = False
                self.hide = True
        
                self.game.player = Player(self.game, self.CENTER_X, self.CENTER_Y)
                self.game.BACKGROUND_IMAGE = self.game.MAIN_MENU_IMAGE
                self.game.main_menu = True
                self.game.options_menu = False
                self.game.play_game = False
                self.game.end_game = False
                self.game.fade_out_alpha = 255
                
                self.game.clear_all_sprites()
                self.game.initialise_main_menu_objects()

                sounds.button.play()

    def draw(self, screen):
        if not self.hide:
            if self.hovering:
                screen.blit(self.hover_image, (self.rect.x, self.rect.y))
            else:
                screen.blit(self.image, (self.rect.x, self.rect.y))
            

        


"""When clicked, set player gravity to 0, set self.player.paused = True"""