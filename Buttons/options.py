import pygame
import Assets.sounds as sounds
import Assets.colours as colours
import texture
from Sprites.player import Player

class OptionButton:
    def __init__(self, game):
        self.game = game
        self.player = game.player
        self.CENTER_X = game.CENTER_X
        self.CENTER_Y = game.CENTER_Y
        self.SCREEN_WIDTH = game.SCREEN_WIDTH
        self.SCREEN_HEIGHT = game.SCREEN_HEIGHT

        self.image = pygame.image.load("Assets/Images/Buttons/options.png")
        self.hover_image = pygame.image.load("Assets/Images/Buttons/options_hover.png")
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = 300

        self.hovering = False
        self.clicked = False
        self.hide = False


        checkbox_x = (self.SCREEN_WIDTH - 40) // 2
        checkbox_y = (self.SCREEN_HEIGHT - 40) // 2

        self.bunny          = Checkbox(checkbox_x, checkbox_y * 0.5, name="bunny")
        self.default        = Checkbox(checkbox_x, checkbox_y * 0.6, name="default")
        self.doodlestein    = Checkbox(checkbox_x, checkbox_y * 0.7, name="doodlestein")
        self.ghost          = Checkbox(checkbox_x, checkbox_y * 0.8, name="ghost")
        self.ice            = Checkbox(checkbox_x, checkbox_y * 0.9, name="ice")
        self.jungle         = Checkbox(checkbox_x, checkbox_y * 1,   name="jungle")
        self.ooga           = Checkbox(checkbox_x, checkbox_y * 1.1, name="ooga")
        self.snow           = Checkbox(checkbox_x, checkbox_y * 1.2, name="snow")
        self.soccer         = Checkbox(checkbox_x, checkbox_y * 1.3, name="soccer")
        self.space          = Checkbox(checkbox_x, checkbox_y * 1.4, name="space")
        self.underwater     = Checkbox(checkbox_x, checkbox_y * 1.5, name="underwater")
        
        self.large_box_y = (self.SCREEN_HEIGHT - 600) // 2

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            self.hovering = True
        else:
            self.hovering = False
        

    def handle_events(self, event):
        mouse_pos = pygame.mouse.get_pos()

        if not self.hide:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  
                if self.rect.collidepoint(mouse_pos):
                    self.clicked = True

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.clicked:
                self.clicked = False
                self.hide = True
                self.game.play_button.hide = True
                self.hide = True
        else:
            for checkbox in Checkbox.checkboxes:
    
                checkbox.handle_events(event)
                
                

    def draw(self, screen):
        if not self.hide:
            if self.hovering:
                screen.blit(self.hover_image, (self.rect.x, self.rect.y))
            else:
                screen.blit(self.image, (self.rect.x, self.rect.y))
        else:
            pygame.draw.rect(screen, colours.BLACK, (self.CENTER_X, self.large_box_y, 200, 600))

            for checkbox in Checkbox.checkboxes:
                checkbox.draw(screen)

            
class Checkbox:

    checkboxes = []

    def __init__(self, x, y, name):
        self.x = x
        self.y = y
        self.name = name
        
        self.width = 40
        self.height = 40

        self.rect = pygame.Rect(x, y, 40, 40)
        self.checked = False

        self.checkboxes.append(self)

    def draw(self, screen):
        # Draw the checkbox border
        pygame.draw.rect(screen, colours.BLACK, self.rect, 2)

        # If checked, draw a tick mark
        if self.checked:
            pygame.draw.line(screen, (0, 255, 0), (self.x, self.y), (self.x + self.width, self.y + self.height), 2)
            pygame.draw.line(screen, (0, 255, 0), (self.x + self.width, self.y), (self.x, self.y + self.height), 2)

    def toggle(self):
        self.checked = not self.checked

    def handle_events(self, event):
        mouse_pos = pygame.mouse.get_pos()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.rect.collidepoint(mouse_pos):
                    self.untick_others()
                    self.toggle()  
                    texture.file_name = self.name
                    texture.folder_name = self.name.title()    

                    sounds.button.play()

    def untick_others(self):
        for checkbox in self.checkboxes:
            if checkbox.checked:
                checkbox.toggle()




"""When clicked, set player gravity to 0, set self.player.paused = True"""
