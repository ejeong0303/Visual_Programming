import pygame
import numpy as np

# Pygame settings
screen_size = (800, 600)
FPS = 60

# Windmill settings
theta_speed_degrees = 5
rect_vertices = np.array([[0, 0], [6, 0], [6, 2], [0, 2]])

# Scale and center the windmill for better visibility
scaling_factor = 50
rect_vertices *= scaling_factor
rect_vertices += np.array([screen_size[0] // 2, screen_size[1] // 2])

# Function to rotate points
def rotate_points(points, theta_degrees, center_point):
    theta_rad = np.radians(theta_degrees)
    rotation_matrix = np.array([[np.cos(theta_rad), -np.sin(theta_rad)], 
                                [np.sin(theta_rad),  np.cos(theta_rad)]])
    return np.dot(points - center_point, rotation_matrix.T) + center_point

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock()

# Game loop
running = True
angle = 0
while running:
    # Event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Rotate the rectangle
    center_point = np.mean(rect_vertices, axis=0)
    rotated_vertices = rotate_points(rect_vertices, angle, center_point)
    angle += theta_speed_degrees

    # Redraw the screen
    screen.fill((255, 255, 255))
    pygame.draw.polygon(screen, (0, 0, 0), rotated_vertices)
    pygame.draw.polygon(screen, (0, 0, 0), -rotated_vertices + 2*center_point)
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

pygame.quit()
