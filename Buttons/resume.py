import Assets.sounds as sounds
import pygame

from Buttons.pause import PauseButton

class ResumeButton(PauseButton):
    
    def __init__(self, game):
        super().__init__(game)
        self.image = pygame.image.load("Assets/Images/Buttons/resume.png").convert_alpha()
        self.pause_screen = pygame.image.load("Assets/Images/Backgrounds/pause_screen.png")
        self.hide = True

    def handle_events(self, event):    
        if not self.hide and not self.game.end_game:
            
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  
                mouse_pos = pygame.mouse.get_pos()
                if self.rect.collidepoint(mouse_pos):
                    self.clicked = True
                    
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.clicked:
                """
                When resume the game we want to set all velocities for all sprites back to what they used to be
                """
                self.game.player.velocity_y = self.player.prior_y_velocity
                self.game.player.paused = False
                self.game.player.handling_events = True

                for monster in self.game.monsters:
                    monster.unpause()

                for ufo in self.game.UFOs:
                    ufo.paused = False

                self.hide = True
                self.clicked = False

                #Now we want to show the pause button
                self.game.pause_button.hide = False
                
                pygame.mixer.unpause()
                sounds.button.play()
                


    def draw(self, screen):
        if not self.hide and not self.game.end_game:
            screen.blit(self.image, (self.rect.x, self.rect.y))
            screen.blit(self.pause_screen, (0, 0))
            
        