import pygame
import assets.sounds as sounds

class PlayButton:
    def __init__(self, game):
        self.game = game
        self.player = game.player

        self.image = pygame.image.load("Doodle_Jump/assets/images/buttons/play.png")
        self.hover_image = pygame.image.load("Doodle_Jump/assets/images/buttons/play_highlight.png")
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = 200

        self.hovering = False
        self.clicked = False
        self.hide = False

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            self.hovering = True
        else:
            self.hovering = False
        

    def handle_events(self, event):
        if not self.hide:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  
                mouse_pos = pygame.mouse.get_pos()
                if self.rect.collidepoint(mouse_pos):
                    self.clicked = True

            
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.clicked:
                self.clicked = False
                self.hide = True
                
                self.game.main_menu = False
                self.game.play_game = True
                sounds.button.play()

    def draw(self, screen):
        if not self.hide:

            if self.hovering:
                screen.blit(self.hover_image, (self.rect.x, self.rect.y))
            else:
                screen.blit(self.image, (self.rect.x, self.rect.y))
            
        


"""When clicked, set player gravity to 0, set self.player.paused = True"""