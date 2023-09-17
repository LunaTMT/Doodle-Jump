import pygame
import Assets.sounds as sounds

class PauseButton:
    def __init__(self, game):
        self.game       = game
        self.player     = game.player
        self.monsters   = game.monsters.sprites()

        self.image = pygame.image.load("Assets/Images/Buttons/pause.png")
        self.rect = self.image.get_rect()
        self.rect.x = game.SCREEN_WIDTH - self.rect.width - 30
        self.rect.y = 15

        self.clicked = False
        self.hide = False

    def handle_events(self, event):
        if not self.hide and not self.game.end_game:
            """
            Upon clicking the pause button we store prior velocities for certain sprites and set their velcoity to 0 or pause them
            """

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  
                mouse_pos = pygame.mouse.get_pos()
                if self.rect.collidepoint(mouse_pos):
                    
                    self.player.prior_y_velocity = self.player.velocity_y
                    self.player.velocity_y = 0
                    self.game.player.paused = True

                    #We must store the monster's speed so upon resuming the monster continues at the same rate prior to pausing 
                    for monster in self.game.monsters:
                        monster.pause()

                    #simply pausing ufo
                    for ufo in self.game.UFOs:
                        ufo.paused = True
                    
                    pygame.mixer.pause()
                    self.clicked = True

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.clicked:
                #When the user releases the left click we hide the button and show the resume button
                self.game.resume_button.hide = False 
                self.hide = True
                self.clicked = False
                sounds.button.play()

    def draw(self, screen):
        if not self.hide:
            screen.blit(self.image, (self.rect.x, self.rect.y))
            
  