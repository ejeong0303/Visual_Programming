import pygame
import numpy as np

# Function to rotate a point around a pivot point
def rotate_point(pos, pivot, angle):
    px, py = pivot
    x, y = pos
    qx = px + np.cos(angle) * (x - px) - np.sin(angle) * (y - py)
    qy = py + np.sin(angle) * (x - px) + np.cos(angle) * (y - py)
    return qx, qy

# Define constants
WIDTH, HEIGHT = 1800, 1000
FPS = 60  # Frames per second
ANGLE_SPEED = 5 * np.pi / 180  # 5 degrees per frame in radians

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Define the rectangle points
P = np.array([[0,0], [6,0], [6,2], [0,2]])

# Translate the rectangle points to the center
P = P*20 + np.array([900 - 3*20, 500 - 1*20]) # Subtracting half of rectangle width and height for center alignment

# Define the rotation pivot as the center of the rectangle
pivot = np.array([900, 500])

# Define the windmill wings
wings = [P]
for i in range(3):
    wing = np.array([rotate_point(p, pivot, (i+1)*np.pi/2) for p in P])
    wings.append(wing)

# Game loop
clock = pygame.time.Clock()
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill((255, 255, 255))

    # Draw the windmill
    for wing in wings:
        pygame.draw.polygon(screen, (0, 0, 0), wing)

    # Rotate the wings
    wings = [np.array([rotate_point(p, pivot, ANGLE_SPEED) for p in wing]) for wing in wings]

    # Flip the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

# Quit Pygame
pygame.quit()
