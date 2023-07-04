import pygame
import imageio
import numpy as np

# Window size
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# Colors
BLACK = (0, 0, 0)

# Frames per second
FPS = 60

pygame.init()
pygame.mixer.init()
pygame.display.set_caption("20191659 최이정")
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

mushroom_img = imageio.imread('assets/mushroom1.png')

def rotate(im, deg):
    imr = np.zeros(im.shape, dtype = np.uint8)
    # imr = np.zeros_like(im) 
    rad = np.deg2rad(deg)
    c = np.cos(rad)
    s = np.sin(rad)

    h, w = im.shape[:2] # extract width and height of image
    cy, cx = h//2, w//2 # calculate the center of the image

    for y in range(im.shape[0]):
        for x in range(im.shape[1]):
            xr = c*(x-cx) - s*(y-cy) + cx # adjust rotated image to the center
            yr = s*(x-cx) + c*(y-cy) + cy
            ixr = int(xr)
            iyr = int(yr)

            if ixr < 0 or iyr < 0 or ixr >= imr.shape[1] or iyr >= imr.shape[0]:
                continue
            else:
                imr[iyr, ixr] = im[y, x]

    return imr

im25 = rotate(mushroom_img, 25)
im30 = rotate(mushroom_img, 30)
im45 = rotate(mushroom_img, 45)
im90 = rotate(mushroom_img, 90)
im180 = rotate(mushroom_img, 180)

imageio.imwrite('assets/mushroom25.png', im25)
imageio.imwrite('assets/mushroom30.png', im30)
imageio.imwrite('assets/mushroom45.png', im45)
imageio.imwrite('assets/mushroom90.png', im90)
imageio.imwrite('assets/mushroom180.png', im180)

def main():
    done = False    
    img25 = pygame.image.load('assets/mushroom25.png')
    img30 = pygame.image.load('assets/mushroom30.png')
    img45 = pygame.image.load('assets/mushroom45.png')
    img90 = pygame.image.load('assets/mushroom90.png')
    img180 = pygame.image.load('assets/mushroom180.png')

    while not done: 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True 

        screen.fill(BLACK)

        screen.blit(img25, (50, 50))
        screen.blit(img30, (150, 150))
        screen.blit(img45, (250, 250))
        screen.blit(img90, (350, 350))
        screen.blit(img180, (450, 450))
        
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
