import Assets.sounds as sounds
import Assets.colours as colours
import pygame
import texture

from Sprites.tile import Tile


class OptionButton:

    TITLE = pygame.image.load("Assets/Images/Backgrounds/options_title.png")

    def __init__(self, game):
        self.game           = game
        self.player         = game.player
        self.CENTER_X       = game.CENTER_X
        self.CENTER_Y       = game.CENTER_Y
        self.SCREEN_WIDTH   = game.SCREEN_WIDTH
        self.SCREEN_HEIGHT  = game.SCREEN_HEIGHT

        self.image = pygame.image.load("Assets/Images/Buttons/options.png")
        self.hover_image = pygame.image.load("Assets/Images/Buttons/options_hover.png")
        
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = 300

        self.hovering = False
        self.clicked = False
        self.hide = False

        #texture tick boxes to change texture pack
        Checkbox.checkboxes = []
        self.bunny          = Checkbox(game, 0.8, 0.7, name="bunny")
        self.default        = Checkbox(game, 0.8, 0.8, name="default")
        self.doodlestein    = Checkbox(game, 0.8, 0.9, name="doodlestein")
        self.ghost          = Checkbox(game, 0.8, 1, name="ghost")
        self.ice            = Checkbox(game, 0.8, 1.1, name="ice")
        self.jungle         = Checkbox(game, 0.8, 1.2,   name="jungle")
        self.ooga           = Checkbox(game, 0.8, 1.3, name="ooga")
        self.snow           = Checkbox(game, 0.8, 1.4, name="snow")
        self.soccer         = Checkbox(game, 0.8, 1.5, name="soccer")
        self.space          = Checkbox(game, 0.8, 1.6, name="space")
        self.underwater     = Checkbox(game, 0.8, 1.7, name="underwater")

    
    def handle_events(self, event):
        mouse_pos = pygame.mouse.get_pos()

        if not self.hide:
            #Upon clicking the button change button state to clicked
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  
                if self.rect.collidepoint(mouse_pos):
                    self.clicked = True

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.clicked:
                #when clicking on options button we want to change to options menu and hide options button
                self.game.BACKGROUND_IMAGE = self.game.OPTIONS_IMAGE
                self.game.options_menu = True
                self.game.play_button.hide = True 

                self.clicked = False
                self.hide = True
        else:
            #when in options menu, handle all checkboxes to get texture choice
            for checkbox in Checkbox.checkboxes:
                checkbox.handle_events(event)
                
    def update(self):
        """Hover detection"""
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            self.hovering = True
        else:
            self.hovering = False


    def draw(self, screen):
        if not self.hide:
            #default options button
            if self.hovering:
                screen.blit(self.hover_image, (self.rect.x, self.rect.y))
            else:
                screen.blit(self.image, (self.rect.x, self.rect.y))
        else:
            #when in options menu draw associated components
            screen.blit(self.game.BACKGROUND_IMAGE, (0,0))
            screen.blit(self.TITLE, (0,0))
            for checkbox in Checkbox.checkboxes:
                checkbox.draw(screen)

            
class Checkbox:
    checkboxes = [] #List of all initialised checkbox objects

    def __init__(self, game, x_multiplier, y_multiplier, name):

        SCREEN_WIDTH = game.SCREEN_WIDTH
        SCREEN_HEIGHT = game.SCREEN_HEIGHT

        self.game = game
        self.name = name
        self.width = 40
        self.height = 40

        self.x = ((SCREEN_WIDTH - self.width) // 2) * x_multiplier
        self.y = ((SCREEN_HEIGHT - self.height) // 2) * y_multiplier
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        font = pygame.font.Font("Assets/Fonts/DoodleJump.ttf", 36)
        self.text = font.render(name.title(), True, colours.BLACK)
        self.text_rect = self.text.get_rect()
        text_width, text_height = self.text_rect.width, self.text_rect.height
   
        #center text in screen and tranlate based on multipliers
        text_x = ((SCREEN_WIDTH - text_width) // 2) * x_multiplier
        text_y = ((SCREEN_HEIGHT - text_height) // 2) * y_multiplier
        self.text_rect.x = text_x + 100
        self.text_rect.y = text_y
        
        """
        Before the game has begun the default will always have a tick
        once the texture has been changed however, the currently selected texture will be ticked
        """
        self.checked = True if name == texture.file_name else False 
        self.checkboxes.append(self)



    def draw(self, screen):
        pygame.draw.rect(screen, colours.BLACK, self.rect, 2) #Box
        screen.blit(self.text, self.text_rect) #associated text
        
        if self.checked: #When checked draw cross over box
            pygame.draw.line(screen, (0, 255, 0), (self.x, self.y), (self.x + self.width, self.y + self.height), 2)
            pygame.draw.line(screen, (0, 255, 0), (self.x + self.width, self.y), (self.x, self.y + self.height), 2)

    def toggle(self): #Switch
        self.checked = not self.checked

    def handle_events(self, event):
        mouse_pos = pygame.mouse.get_pos()
        if not self.checked:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.rect.collidepoint(mouse_pos):
                    
                    """
                    Upon selecting a checkbox we untick every other box and toggle the currently selected one
                    """
                    self.untick_others() 
                    self.toggle()  

                    #Update the current texture selected
                    texture.file_name = self.name
                    texture.folder_name = self.name.title()   
                    
                    #Update current images
                                   
                    self.game.update_top_images()
                    self.game.update_bottom_images()
                    self.game.BACKGROUND_IMAGE = pygame.image.load(f"Assets/Images/Backgrounds/Backgrounds/{texture.file_name}.png")

                    #Update all class texture pack (cls methods)
                    Tile.update_images() 

                    for power_up in Tile.POWER_UPS:
                        power_up.update_images()

                    for enemy in self.game.enemy_objects:
                        enemy.update_images()

                    #Update current menu and player sprite images
                    self.game.platforms.sprites()[0].update_current_image()
                    self.game.all_enemies[0].update_current_image()
                    self.game.player.update_image()     

                    sounds.button.play()

    def untick_others(self):
        """
        In this function we toggle every other checkbox that is not the current one in question (self)
        """
        for checkbox in self.checkboxes:
            if checkbox.checked and checkbox is not self:
                checkbox.toggle()

