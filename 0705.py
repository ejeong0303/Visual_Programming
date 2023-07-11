import pygame
import numpy as np

# Pygame settings
screen_size = (800, 600)
FPS = 60
center = np.array(screen_size) / 2

# Clock hand settings
hour_hand_vertices = np.array([[0, 0], [6, 0], [6, 2], [0, 2]], dtype=np.float64) * 20
hour_hand_vertices += center
minute_hand_vertices = hour_hand_vertices.copy()

# Rotation speed settings
hour_rotation_speed = 360 / 12 / FPS
minute_rotation_speed = 360 / FPS

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
hour_angle = 0
minute_angle = 0
while running:
    # Event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Rotate the clock hands
    rotated_hour_hand_vertices = rotate_points(hour_hand_vertices, hour_angle, center)
    rotated_minute_hand_vertices = rotate_points(minute_hand_vertices, minute_angle, center)
    hour_angle -= hour_rotation_speed  # subtract because rotation is clockwise
    minute_angle -= minute_rotation_speed  # subtract because rotation is clockwise

    # Redraw the screen
    screen.fill((255, 255, 255))
    pygame.draw.polygon(screen, (0, 255, 0), rotated_hour_hand_vertices)
    pygame.draw.polygon(screen, (255, 0, 0), rotated_minute_hand_vertices)
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

pygame.quit()
