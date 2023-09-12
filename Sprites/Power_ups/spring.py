import pygame
import Assets.sounds as sounds
import texture

class Spring(pygame.sprite.Sprite):

    SPRITE_SHEET = pygame.image.load(f"Assets/Images/Game_tiles/{texture.file_name}.png")
    SPRING = SPRITE_SHEET.subsurface(pygame.Rect(404, 99, 17, 12))  # Extract a 32x32 sprite
    SPRING_EXPANDED = SPRITE_SHEET.subsurface(pygame.Rect(404, 115, 17, 28))

    #x = random.randint(self.rect.topleft, self.rect.topright)
    #y = self.rect.top 

    def __init__(self, game, tile, x, y):
        super().__init__()
        self.game = game
        self.SCREEN_HEIGHT = game.SCREEN_HEIGHT
        self.SCREEN_WIDTH = game.SCREEN_WIDTH
        
        self.CENTER_X = game.CENTER_X
        self.player = game.player
        

        self.alpha = 255
        self.x = x
        self.y = y - 10
        self.image = self.SPRING 
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.center = (self.x, self.y)
        
        self.expanded = False
        self.collision = False

    @classmethod
    def update_images(cls):
        cls.SPRITE_SHEET = pygame.image.load(f"Assets/Images/Game_tiles/{texture.file_name}.png")
        cls.SPRING = cls.SPRITE_SHEET.subsurface(pygame.Rect(404, 99, 17, 12))  # Extract a 32x32 sprite
        cls.SPRING_EXPANDED = cls.SPRITE_SHEET.subsurface(pygame.Rect(404, 115, 17, 28))

    def update(self):
        self.death_check()
        self.player_collision_check()

    def player_collision_check(self):
        collision = self.rect.colliderect(self.game.player.rect)
        if (collision 
            and self.player.falling  
            and not self.player.dead
            and not self.expanded):

           
            self.player.using_spring = True
            self.player.JUMP_STRENGTH = -23
            self.player.jump(play_sound=False)
            
            if not self.player.using_spring_shoes:
                self.player.JUMP_STRENGTH = -15
    
            sounds.spring.play()
            self.collision = True



    def death_check(self):
        if self.rect.y > self.SCREEN_HEIGHT:
            self.kill()

    def draw(self, screen):
        if self.collision and not self.expanded:
            self.image = self.SPRING_EXPANDED
            self.rect.y -= 20
            self.expanded = True

        self.image.set_alpha(self.game.fade_out_alpha)    
        screen.blit(self.image, self.rect)