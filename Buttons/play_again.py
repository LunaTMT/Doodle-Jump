import Assets.sounds as sounds
import pygame

class PlayAgain:
    SPRITE_SHEET = pygame.image.load("Assets/Images/start-end-tiles.png")
    DEFAULT_IMAGE = SPRITE_SHEET.subsurface(pygame.Rect(231, 99, 222, 80))
    HOVER_IMAGE = SPRITE_SHEET = pygame.image.load("Assets/Images/Buttons/play_again_hover.png")

    def __init__(self, game):
        self.game = game
        self.player = game.player
        self.CENTER_X = game.CENTER_X
        self.CENTER_Y = game.CENTER_Y
        self.SCREEN_HEIGHT = game.SCREEN_HEIGHT
        self.SCREEN_WIDTH = game.SCREEN_WIDTH

        self.image = self.DEFAULT_IMAGE
        self.hover_image = self.HOVER_IMAGE
        
        self.rect = self.image.get_rect()
        image_width, image_height = self.DEFAULT_IMAGE.get_size()

        # Calculate the position to blit the image in the center of the screen
        x = (self.SCREEN_WIDTH - image_width) // 2
        y = (self.SCREEN_HEIGHT - image_height) // 2
        
        self.rect.x = x * 0.25
        self.rect.y = y * 1.5

        self.hovering = False
        self.clicked = False
        self.hide = False
        
    def handle_events(self, event):
        if not self.hide:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  
                mouse_pos = pygame.mouse.get_pos()
                if self.rect.collidepoint(mouse_pos):
                    self.clicked = True

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.clicked:
                self.clicked = False
                self.hide = True

                #Game State change
                self.game.main_menu = False
                self.game.play_game = True
                self.game.end_game = False
                
                #Initialise objects and weights and reset alpha
                self.game.initialise_game_weights()
                self.game.initialise_game_objects()
                self.game.fade_out_alpha = 255
                
                sounds.button.play()

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        self.hovering = True if self.rect.collidepoint(mouse_pos) else False

    def draw(self, screen):
        if not self.hide:
            if self.hovering:
                screen.blit(self.hover_image, (self.rect.x, self.rect.y))
            else:
                screen.blit(self.image, (self.rect.x, self.rect.y))
            

        


"""When clicked, set player gravity to 0, set self.player.paused = True"""