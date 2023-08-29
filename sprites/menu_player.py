from sprites.player import Player


class MenuPlayer(Player):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.velocity_y = self.JUMP_STRENGTH

    def handle_events(self, event):
        pass

    def update(self):
        self.velocity_y += self.GRAVITY
        self.y += self.velocity_y
        
        #Gravity update
        if self.velocity_y > self.GRAVITY:
            self.falling = True 
            self.jumping = False
        else:
            self.falling = False

        self.rect.topleft = (self.x, self.y)
