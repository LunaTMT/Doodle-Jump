import pygame
pygame.init()

# Define the window dimensions
window_width = 800
window_height = 600

# Create the display surface
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Checkbox in Pygame")

class Checkbox:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.width = 20
        self.height = 20

        self.rect = pygame.Rect(x, y, 20, 20)
        self.checked = False

    def draw(self):
        # Draw the checkbox border
        pygame.draw.rect(screen, (255,255,255), self.rect, 2)

        # If checked, draw a tick mark
        if self.checked:
            pygame.draw.line(screen, (0, 255, 0), (self.x, self.y), (self.x + self.width, self.y + self.height), 2)
            pygame.draw.line(screen, (0, 255, 0), (self.x + self.width, self.y), (self.x, self.y + self.height), 2)

    def toggle(self):
        self.checked = not self.checked

checkbox = Checkbox(50, 50)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                mouse_pos = pygame.mouse.get_pos()
                if checkbox.rect.collidepoint(mouse_pos):
                    checkbox.toggle()

    screen.fill((0, 0, 0))  # Fill the screen with a black background
    checkbox.draw()  # Draw the checkbox

    pygame.display.flip()  # Update the display

pygame.quit()  # Quit Pygame when the game loop exits
