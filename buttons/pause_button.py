import pygame
import assets.sounds as sounds

class PauseButton:
    def __init__(self, game):
        self.game = game
        self.player = game.player

        self.image = pygame.image.load("Doodle_Jump/assets/images/buttons/pause.png")
        self.rect = self.image.get_rect()
        self.rect.x = game.SCREEN_WIDTH - self.rect.width - 10
        self.rect.y = 10

        self.clicked = False
        self.hide = False

    def handle_events(self, event):
        if not self.hide:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  
                mouse_pos = pygame.mouse.get_pos()
                if self.rect.collidepoint(mouse_pos):
                    self.game.GRAVITY = 0
                    self.player.GRAVITY = 0
                    self.player.prior_y_velocity = self.player.velocity_y
                    self.player.velocity_y = 0
                    self.player.paused = True
                    self.clicked = True

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.clicked:
                self.hide = True
                self.game.resume_button.hide = False
                self.clicked = False
                sounds.button.play()

    def draw(self, screen):
        if not self.hide:
            screen.blit(self.image, (self.rect.x, self.rect.y))
            
        


"""When clicked, set player gravity to 0, set self.player.paused = True"""