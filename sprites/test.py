import pygame
from pygame.locals import *

pygame.init()

# Set up display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Moving and Shrinking Rect")

# Define colors
red = (255, 0, 0)

# Create a rectangle
initial_rect = pygame.Rect(100, 100, 100, 100)

# Define target position and size
target_position = (400, 300)
target_size = (10, 10)

# Calculate movement direction
dx = target_position[0] - initial_rect.x
dy = target_position[1] - initial_rect.y
distance = pygame.math.Vector2(dx, dy).length()
movement_speed = 2
scale_speed = 0.005

current_position = (initial_rect.x, initial_rect.y)
current_size = (initial_rect.width, initial_rect.height)

running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    # Update position
    if current_position != target_position:
        if distance > movement_speed:
            direction = pygame.math.Vector2(dx, dy).normalize()
            current_position = (current_position[0] + direction.x * movement_speed, current_position[1] + direction.y * movement_speed)
        else:
            current_position = target_position

    # Update size
    if current_size[0] > target_size[0]:
        current_size = (current_size[0] - scale_speed, current_size[1] - scale_speed)

    # Clear the screen
    screen.fill((255, 255, 255))

    # Draw the shrinking rectangle
    if current_size[0] > 0 and current_size[1] > 0:
        current_rect = pygame.Rect(current_position[0], current_position[1], current_size[0], current_size[1])
        pygame.draw.rect(screen, red, current_rect)

    pygame.display.flip()

    if current_size[0] <= 0:
        running = False

pygame.quit()
