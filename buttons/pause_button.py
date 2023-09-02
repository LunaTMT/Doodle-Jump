import pygame
import assets.sounds as sounds

class PauseButton:
    def __init__(self, game):
        self.game = game
        self.player = game.player
        self.monsters = game.monsters

        self.image = pygame.image.load("assets/images/buttons/pause.png")
        self.rect = self.image.get_rect()
        self.rect.x = game.SCREEN_WIDTH - self.rect.width - 10
        self.rect.y = 20

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
                    self.player.handling_events = False

                    for monster in self.monsters:
                        monster.prior_speed     = monster.speed 
                        monster.prior_speed_x   = monster.speed_x 
                        monster.prior_speed_y   = monster.speed_y 

                        pygame.mixer.pause()

                        monster.speed = 0
                        monster.speed_x = 0
                        monster.speed_y = 0
        
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