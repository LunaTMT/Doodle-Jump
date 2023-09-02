import pygame
from buttons.pause_button import PauseButton
import assets.sounds as sounds

class ResumeButton(PauseButton):
    
    def __init__(self, game):
        super().__init__(game)
        self.image = pygame.image.load("assets/images/buttons/resume.png").convert_alpha()
        self.pause_screen = pygame.image.load("assets/images/backgrounds/pause_screen.png")
        self.hide = True

    def handle_events(self, event):    
        if not self.hide:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  
                mouse_pos = pygame.mouse.get_pos()
                if self.rect.collidepoint(mouse_pos):
                    self.clicked = True
                    
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.clicked:
                self.game.GRAVITY = self.player.GRAVITY = 0.4
                self.player.velocity_y = self.player.prior_y_velocity
                self.player.paused = False
                self.player.handling_events = True

                for monster in self.monsters:
                    pygame.mixer.unpause()
                    monster.speed   = monster.prior_speed
                    monster.speed_x = monster.prior_speed_x 
                    monster.speed_y = monster.prior_speed_y 


                self.hide = True
                self.clicked = False
                self.game.pause_button.hide = False
                sounds.button.play()

    def draw(self, screen):
        if not self.hide:
            screen.blit(self.image, (self.rect.x, self.rect.y))
            screen.blit(self.pause_screen, (0, 0))
            
        