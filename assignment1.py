import pygame
import numpy as np

def getRegularPolygon(N, Radius = 100, tx = 200, ty = 300):
    vert = []
    for i in range(N):
        degree = i * 360./N
        radian = degree * 2. * np.pi /360
        x = Radius * np.cos(radian) + tx
        y = Radius * np.sin(radian) + ty
        vert.append((x,y))
    return vert

WINDOW_WIDTH = 1600
WINDOW_HEIGHT = 800

pygame.init()
pygame.display.set_caption("최이정 20191659")
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

done = False
nshapes = 200
while not done: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    screen.fill((0,0,0)) # clear screen

    for _ in range(nshapes):
        color = (np.random.randint(0, 256), np.random.randint(0, 256), np.random.randint(0, 256))
        if np.random.random() < 0.5:  # Draw either circle or rectangle
            pos = (np.random.randint(0, WINDOW_WIDTH), np.random.randint(0, WINDOW_HEIGHT))
            radius = np.random.randint(10, 100)
            pygame.draw.circle(screen, color, pos, radius)
        else:
            top_left = (np.random.randint(0, WINDOW_WIDTH), np.random.randint(0, WINDOW_HEIGHT))
            dimensions = (np.random.randint(10, 100), np.random.randint(10, 100))
            pygame.draw.rect(screen, color, pygame.Rect(top_left, dimensions))

    if done:
        break

    pygame.display.flip()
    clock.tick(5)

pygame.quit()
