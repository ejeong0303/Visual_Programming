import pygame
import numpy as np

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 800
triangle = [[350, 200], [250, 350], [450, 350]]
GREEN = (0, 255, 0)

ntriangles = 1000
triangles = []
colors = []
for i in range(ntriangles):
    r = np.random.randint(0, 256)
    g = np.random.randint(0, 256)
    b = np.random.randint(0, 256)
    colors.append((r, g, b))
    tri = []
    for k in range (3):
        x = np.random.randint(0, WINDOW_WIDTH)
        y = np.random.randint(0, WINDOW_HEIGHT)
        tri.append((x,y))
    triangles.append(tri)


pygame.init()
pygame.display.set_caption("최이정 20191659")
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

done = False
while True: #run forever
    #1.event check
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    #2. clear the screen
    screen.fill((255,190,120))

    #3. draw things!
    #맨 뒤의 숫자가 line thickness
    pygame.draw.polygon(screen, GREEN, triangle, 3)

    for k in range(len(triangles)):
        tri = triangles[k]
        color = colors[k]
        pygame.draw.polygon(screen, color, tri)
    
    if done == True:
        #do something
        break
        pass
        
    pygame.display.flip() #double buffering
    clock.tick(60) #60 frames per second

#
pygame.quit()
