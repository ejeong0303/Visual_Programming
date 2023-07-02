import pygame
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

def Rmat(deg):
    rad = np.deg2rad(deg)
    c = np.cos(rad)
    s = np.sin(rad)
    R = np.array([[c, -s, 0], 
                  [s, c, 0], 
                  [0, 0, 1]])
    return R

class Star:
    def __init__(self, startLoc, speed):
        self.loc = np.array([*startLoc, 1.0])
        self.speed = speed
        self.color = np.random.randint(0, 256, 3)  # Random color for glitter effect
        self.reached_center = False

    def update(self):
        # Gravitational pull
        direction = np.array([WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2, 1.0]) - self.loc
        distance = np.linalg.norm(direction) + 1e-10  # Adding a small constant to avoid division by zero
        direction /= distance
        pull = 500.0 / (distance ** 2 + 1e-10)
        self.speed += pull
        self.loc += direction * self.speed
        # Rotation
        rot_center = np.array([WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2, 1.0])
        direction = self.loc - rot_center
        direction = Rmat(0.2) @ direction  # Rotate 0.2 degree per frame
        self.loc = rot_center + direction
        # Randomize color for glitter effect
        self.color = (self.color + np.random.randint(-2, 3, 3)) % 256  # Change color slightly
        # If the star is near the center, mark it as reached
        if distance < 5: 
            self.reached_center = True
        else:
            self.reached_center = False

    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.loc[0]), int(self.loc[1])), 1)

stars = [Star(np.random.rand(2) * [WINDOW_WIDTH, WINDOW_HEIGHT], 0.1) for _ in range(1000)]

pygame.mixer.music.load('assets/blackhole.mp3')  # Load the background music
pygame.mixer.music.play(-1)  # Play the music indefinitely

def main():
    done = False    

    while not done: 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True 

        screen.fill(BLACK)

        for star in stars:
            star.update()
            star.draw()
        
        reached_center_count = 0
        for star in stars:
            star.update()
            if star.reached_center:
                reached_center_count += 1
            star.draw()

        # If more than 50% of the stars have reached the center, reset the game
        if reached_center_count / len(stars) > 0.5:
            pygame.mixer.music.stop()  # Stop the current music
            #pygame.mixer.Sound('assets/explosion.mp3').play()  # Play the explosion sound
            screen.fill(BLACK)
            pygame.display.flip()
            pygame.time.wait(2000)  # Wait for 2 seconds
            stars[:] = [Star(np.random.rand(2) * [WINDOW_WIDTH, WINDOW_HEIGHT], 0.1) for _ in range(1000)]
            pygame.mixer.music.play(-1)  # Restart the background music

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()