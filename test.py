import pygame
import sys

pygame.init()

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

# Create a Pygame window
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Text Highlighting Example")

font = pygame.font.Font(None, 36)
text = font.render("Highlighted Text", True, BLACK)
text_rect = text.get_rect()
text_rect.center = (screen_width // 2, screen_height // 2)

highlight_rect = text_rect.copy()
highlight_rect.inflate_ip(10, 10)  # Expand the rectangle to create a highlight effect

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(WHITE)

    # Draw the highlight rectangle first
    pygame.draw.rect(screen, YELLOW, highlight_rect)

    # Then, draw the text on top
    screen.blit(text, text_rect)

    pygame.display.flip()

pygame.quit()
sys.exit()
