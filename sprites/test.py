import pygame
import sys
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600

# Colors
white = (255, 255, 255)
blue = (0, 0, 255)

# Create the screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Spinning and Moving Rectangle")

# Rectangle properties
rect_size = 100
rect_x = (screen_width - rect_size) // 2
rect_y = (screen_height - rect_size) // 2
rect_rotation_speed = 2  # Degrees per frame
rect_movement_speed = 5  # Pixels per frame

# Initial rotation angle
rect_angle = 0

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill(white)

    # Rotate the rectangle
    rotated_rect = pygame.Surface((rect_size, rect_size), pygame.SRCALPHA)
    rotated_rect = pygame.transform.rotate(rotated_rect, rect_angle)
    rect_angle += rect_rotation_speed
    if rect_angle >= 360:
        rect_angle -= 360

    # Move the rectangle
    rect_x += rect_movement_speed
    if rect_x > screen_width:
        rect_x = -rect_size

    # Draw the rectangle on the screen
    pygame.draw.rect(screen, blue, (rect_x, rect_y, rect_size, rect_size))
    screen.blit(rotated_rect, (rect_x, rect_y))

    # Update the display
    pygame.display.flip()

    # Control the frame rate
    pygame.time.delay(20)

# Quit Pygame
pygame.quit()
sys.exit()
