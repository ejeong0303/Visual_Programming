import pygame
import numpy as np

def getRegularPolygon(N, radius=1):
    v = np.zeros((N,2), dtype=np.float32)
    for i in range(N):
        deg = i * 360. / N
        rad = deg * np.pi / 180.
        x = radius * np.cos(rad)
        y = radius * np.sin(rad)
        v[i, 0] = x 
        v[i, 1] = y 
    return v

GREEN = (100, 200, 100)
WINDOW_WIDTH = 1800
WINDOW_HEIGHT = 1000

pygame.init() 
pygame.display.set_caption("Mouse")
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

class Polygon:
    def __init__(self, nvertices):
        self.nvertices = nvertices
        self.color = np.random.randint(0, 256, size=3)
        self.radius = 50
        #self.line_width = 8
        self.line_width = np.random.choice([0, 2, 4])
        self.polygon = getRegularPolygon(nvertices, radius=self.radius)

        self.position = np.array([100., 700.])
        self.angle = np.deg2rad(45)
        self.speed = np.array([10 * np.cos(self.angle), -10 * np.sin(self.angle)])
        self.gravity = np.array([0, .421])
        self.sound = pygame.mixer.Sound('assets/mixkit-arcade-mechanical-bling-210.wav')
        
    def update(self):
        #self.speed += self.gravity
        self.position += self.speed
        self.q = self.polygon + self.position

        if self.position[0] < 0 or self.position[0] > WINDOW_WIDTH:
            self.speed[0] *= -1.0
            self.sound.play()
        if self.position[1] < 0 or self.position[1] > WINDOW_HEIGHT:
            self.speed[1] *= -1.0
            self.sound.play()

    def draw(self, screen):
        pygame.draw.polygon(screen, self.color, self.q.astype(int), width=self.line_width)


class Bullet:
    def __init__(self):
        self.position = np.array([100., 700.])
        self.angle = np.deg2rad(45)
        self.speed = np.array([10 * np.cos(self.angle), -10 * np.sin(self.angle)])
        self.color = (255, 0, 0)
        self.radius = 5
        self.gravity = np.array([0, .421])
        # Load sound file
        self.sound = pygame.mixer.Sound('assets/mixkit-arcade-mechanical-bling-210.wav')

    def update(self):
        self.speed += self.gravity
        self.position += self.speed

        if self.position[0] - self.radius < 0:
            self.position[0] = self.radius
            self.speed[0] *= -1
            self.sound.play()
        if self.position[0] + self.radius > WINDOW_WIDTH:
            self.position[0] = WINDOW_WIDTH - self.radius
            self.speed[0] *= -1
            self.sound.play()
        if self.position[1] - self.radius < 0:
            self.position[1] = self.radius
            self.speed[1] *= -1
            self.sound.play()
        if self.position[1] + self.radius > WINDOW_HEIGHT:
            self.position[1] = WINDOW_HEIGHT - self.radius
            self.speed[1] *= -1
            self.sound.play()

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.position.astype(int), self.radius)


polygon_list = []

done = False
f = 0
while not done:
    f += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print("Mouse Button Pressed!")
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done = True
            elif event.key == pygame.K_RETURN:  # Bullet is created when Enter key is pressed
                polygon_list.append(Polygon(nvertices=np.random.randint(3, 15)))
            elif event.key == pygame.K_PAGEUP:  # Move up
                if polygon_list:
                    polygon_list[-1].speed[1] -= 1
            elif event.key == pygame.K_PAGEDOWN:  # Move down
                if polygon_list:
                    polygon_list[-1].speed[1] += 1
            elif event.key == pygame.K_HOME:  # Move left
                if polygon_list:
                    polygon_list[-1].speed[0] -= 1
            elif event.key == pygame.K_END:  # Move right
                if polygon_list:
                    polygon_list[-1].speed[0] += 1

    for p in polygon_list:
        p.update()

    screen.fill((0,0,0))

    pygame.draw.circle(screen, (255, 0, 0), (100, 700), 50)
    
    for p in polygon_list:
        p.draw(screen)
    
    #if bullet is not None:
    #    bullet.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
