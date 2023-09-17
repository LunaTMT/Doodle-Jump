from Sprites.player import Player

class MenuPlayer(Player):
    """
    This class is a variation on the Player class that does not allow for any event handling but
    Still allows a player to jump on a tile and to be affected by gravity
    """
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.y = 760
        self.velocity_y = self.JUMP_STRENGTH

    def handle_events(self, _):
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
