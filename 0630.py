#
# Rotate & Translate
#

import pygame
import numpy as np

def getRegularPolygon(N, radius=1):
    v = np.zeros((N,2))
    for i in range(N):
        deg = i * 360. / N
        rad = deg * np.pi / 180.
        x = radius * np.cos(rad)
        y = radius * np.sin(rad)
        v[i] = [x, y]
    return v

def getRectangle(width, height, x=0, y=0):
    points = np.array([ [0, 0], 
                        [width, 0], 
                        [width, height], 
                        [0, height]], dtype='float')
    points = points + [x, y]
    # points = np.array([ [x, y], 
    #                     [x+width, y], 
    #                     [x+width, y+height], 
    #                     [x, y+height]], dtype='float')
    return points
#

def Rmat(degree):
    radian = np.deg2rad(degree)
    c = np.cos(radian)
    s = np.sin(radian)
    R = np.array([ [c, -s, 0], 
                   [s, c, 0], 
                   [0, 0, 1]], dtype='float')
    return R 

def Tmat(tx, ty):
    T = np.array([ [1, 0, tx], 
                   [0, 1, ty], 
                   [0, 0, 1]], dtype='float')
    return T 

pygame.init()
WINDOW_WIDTH = 1800
WINDOW_HEIGHT = 1500

# 색 정의
GREEN = (100, 200, 100)

pygame.init()  # 1! initialize the whole pygame system!
pygame.display.set_caption("Mouse")
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

center1 = [100, 500.]
angle1 = 20
width1 = 300
height1 = 100
rect1 = getRectangle(width1, height1)

gap12 = 30 #

angle2 = 0
width2 = 280
height2 = 70
rect2 = getRectangle(width2, height2)

angle3 = 0
width3 = 400
height3 = 150
rect3 = getRectangle(width3, height3, x=0, y=-height3/2.)

def draw(M, points, color=(0,0,0), p0=None):
    R = M[0:2, 0:2]
    t = M[0:2, 2]

    points_transformed = ( R @ points.T ).T + t 
    pygame.draw.polygon(screen, color, points_transformed, 2)
    if p0 is not None:
        pygame.draw.line(screen, (0,0,0), p0, points_transformed[0])
#

Sun = getRegularPolygon(20, 100)
distSE = 400
Earth = getRegularPolygon(8, 70)
distEM = 130
Moon = getRegularPolygon(3, 30)


angle = 0
angleSE = 0
angleE = 0
angleM = 0
angleEM = 0

done = False
while not done:
    angle += 3
    angleSE += 1
    angleE += 5
    angleEM += 10
    angleM += 7
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print("Mouse Button Pressed!")
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_b: # capital A
                angle1 += 5
            elif event.key == pygame.K_a:
                angle1 -= 5   
            elif event.key == pygame.K_c:
                angle2 += 5
            elif event.key == pygame.K_d:
                angle2 -= 5
        #
        
    screen.fill(GREEN)
    #
    center=(WINDOW_WIDTH/2., WINDOW_HEIGHT/2.)
    Msun = Tmat(center[0], center[1]) @ Rmat(angle)
    draw(Msun, Sun, (255, 255, 100), center)

    # Mearth = Tmat(center[0], center[1]) @ Rmat(angleSE) @ Tmat(distSE, 0) # @ Rmat(-angleSE)
    # draw(Mearth, Earth, (100, 255, 250), Mearth[:2, 2])
    Mearth = Tmat(center[0], center[1]) @ Rmat(angleSE) @ Tmat(distSE, 0) @ Rmat(-angleSE) @ Rmat(angleE)
    draw(Mearth, Earth, (100, 5, 50), Mearth[:2, 2])

    Mmoon = Mearth @ Rmat(angleEM) @ Tmat(distEM, 0) @ Rmat(angleM)
    draw(Mmoon, Moon, (100, 100, 100), Mmoon[:2,2])
    


    cent = (400, 400)
    M = Tmat(cent[0], cent[1])
    draw(M, rect3, (0,0,0))
    M1 = M @ Rmat(angle)
    draw(M1, rect3, (255, 0, 0))
    M2 = M1 @ Rmat(90)
    M3 = M2 @ Rmat(90)
    M4 = M3 @ Rmat(90)
    draw(M2, rect3, (0, 255, 0))
    draw(M3, rect3, (255, 0, 250))
    draw(M4, rect3, (255, 250, 0))
    pygame.draw.circle(screen, (0,0,0), cent, 5)
    
    
    
    #
    # center=(WINDOW_WIDTH/2., WINDOW_HEIGHT/2.)
    # M = Tmat(center[0], center[1]) @ Tmat(0, -height1/2.)
    # # draw(M, rect1, (0,0,0))
    # M1 = M @ Tmat(0, height1/2.) @ Rmat(angle) @ Tmat(0, -height1/2.)  # Fan # 1
    # draw(M1, rect1, (255, 0, 0))
    # M2 = M1 @ Tmat(0, height1/2.) @ Rmat(90) @ Tmat(0, -height1/2.)
    # draw(M2, rect1, (0, 255, 0))
    # M3 = M2 @ Tmat(0, height1/2.) @ Rmat(90) @ Tmat(0, -height1/2.) # Fan # 3
    # draw(M3, rect1, (0, 0, 255))
    # M4 = M3 @ Tmat(0, height1/2.) @ Rmat(90) @ Tmat(0, -height1/2.)
    # draw(M4, rect1, (0,255, 255))
    # pygame.draw.circle(screen, (0,0,0), center, 5)
    
    
    # draw
    M1 = np.eye(3) @ Tmat(center1[0], center1[1]) @ Rmat(angle1) @ Tmat(0, -height1/2.)
    draw(M1, rect1, (255, 0, 0))
    M2 = M1 @ Tmat(width1, 0) @ Tmat(0, height1/2.) @ Tmat(gap12, 0) @ Rmat(angle2) @ Tmat(0, -height2/2.)
    draw(M2, rect2, (255, 255, 0))
    pygame.draw.circle(screen, (0,0,0), center1, 4)
    
    C = M1 @ Tmat(width1, 0) @ Tmat(0, height1/2.)
    center2 = C[0:2, 2]
    pygame.draw.circle(screen, (0,0,0), center2, 5)
    # print("C ---")
    # print(C) 
    
    C2 = C @ Tmat(gap12, 0)
    center3 = C2[0:2, 2]
    pygame.draw.circle(screen, (0,0,0), center3, 5)
    # print("C2 -----")
    # print(C2)
    
    pygame.draw.line(screen, (0,0,0), center2, center3, 1)
    
    #
    M = np.eye(3) @ Tmat(center1[0], center1[1]+400) @ Rmat(angle1) @ Tmat(0, -height1/2.)
    draw(M, rect1, (0, 255, 250))
    # pygame.draw.circle(screen, (0,0,0), center1, 4)
    
    M2 = M @ Tmat(width1, 0) @ Tmat(0, height1/2.) @ Rmat(angle2) @ Tmat(0, -height1/2.)
    draw(M2, rect1, (255, 0, 255))
    #
    
    # update screen
    pygame.display.flip()
    clock.tick(60)

# 게임 종료
pygame.quit()