import pygame
import numpy as np

# Window size
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# Colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Frames per second
FPS = 60

# Rectangles settings
RECTANGLE_SPEED = 1
NUM_RECTANGLES = 7

pygame.init()
pygame.display.set_caption("20191659 최이정")
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

collision_sound = pygame.mixer.Sound('assets/chingsound.wav')

class Rectangle:
    def __init__(self, x, y, width, height, color=BLACK):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.dx = np.random.choice([-RECTANGLE_SPEED, RECTANGLE_SPEED])
        self.dy = np.random.choice([-RECTANGLE_SPEED, RECTANGLE_SPEED])

    def move(self):
        self.x += self.dx
        self.y += self.dy
        if not 0 <= self.x <= WINDOW_WIDTH - self.width:
            self.dx *= -1
        if not 0 <= self.y <= WINDOW_HEIGHT - self.height:
            self.dy *= -1

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

def collision_rectangle(r1, r2):
    left1 = r1.x
    right1 = r1.x + r1.width
    left2 = r2.x
    right2 = r2.x + r2.width
    if (right1 < left2) or (right2 < left1): 
        xoverlap = False
    else:
        xoverlap = True

    top1 = r1.y
    bottom1 = r1.y + r1.height
    top2 = r2.y
    bottom2 = r2.y + r2.height
    if (bottom1 < top2) or (bottom2 < top1):
        yoverlap = False
    else:
        yoverlap = True

    if xoverlap and yoverlap:
        return True
    else:
        return False

def reset_color(rectangles):
    for rectangle in rectangles:
        rectangle.color = BLACK

def check_collisions(rectangles):
    for i in range(NUM_RECTANGLES):
        for j in range(i+1, NUM_RECTANGLES):
            if collision_rectangle(rectangles[i], rectangles[j]):
                rectangles[i].color = RED
                rectangles[j].color = RED
                collision_sound.play()

def main():
    rectangles = [Rectangle(np.random.randint(0, WINDOW_WIDTH), np.random.randint(0, WINDOW_HEIGHT), 50, 30) for _ in range(NUM_RECTANGLES)]
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        reset_color(rectangles)

        for rectangle in rectangles:
            rectangle.move()

        check_collisions(rectangles)
        screen.fill((255, 255, 255))

        for rectangle in rectangles:
            rectangle.draw()
        
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
