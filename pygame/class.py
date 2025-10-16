import pygame
import random

# Initialize pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Your Game Title")

# Game clock for frame rate control
clock = pygame.time.Clock()

# Game loop
running = True
while running:
    # Control frame rate (60 FPS)
    clock.tick(60)
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Game logic goes here
    
    
    # Drawing
    screen.fill((0, 0, 0))  # Clear screen with black
    
    # Draw your game objects here
    
    pygame.draw.circle(screen, (255, 0, 0), (random.randint(0, WIDTH), random.randint(0, HEIGHT)), 20)
    
    # Update display
    pygame.display.flip()

# Clean exit
pygame.quit()