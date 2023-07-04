# import required libraries
import pygame
import numpy as np
from datetime import datetime

# set the game window size
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800

# define colors using RGB (Red, Green, Blue) codes
BLACK = (0, 0, 0)
DARK_GREY = (64, 64, 64)
WHITE = (240, 230, 210)
RED = (204, 0, 0)

# set the frames per second (FPS)
FPS = 60

# initialize pygame
pygame.init()
# set the window's caption
pygame.display.set_caption("20191659 최이정")
# set the size of the window
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
# create a clock object
clock = pygame.time.Clock()

# load the bell sound file
bell_sound = pygame.mixer.Sound('assets/mixkit-clock-bells-hour-signal-1069.wav')
# load the tick-tock sound file
ticktock_sound = pygame.mixer.Sound('assets/clock-ticking-natural-room-verb-17249.mp3')

# get the current time
prev_hour = datetime.now().hour
prev_sec = datetime.now().second
prev_min = datetime.now().minute

# set clock attributes
center = (WINDOW_WIDTH/2 ,WINDOW_HEIGHT/2) # clock center
radius = 300 # clock radius
arm_len = 270 # clock arm length
start_pos = np.array([0, -arm_len])
angle_per_hour = 30
angle = 0
num_pos = [None] # position of numbers

# compute the location for the clock numbers
for i in range(12):
    angle += angle_per_hour
    rad = np.deg2rad(angle)
    rot_mat = np.array([[np.cos(rad), -np.sin(rad)],
                        [np.sin(rad), np.cos(rad)]]) # Rotation matrix
    trans_pos  = rot_mat @ start_pos.T # Transformation
    pos = trans_pos .T # Transpose
    pos[0] += center[0]
    pos[1] += center[1]
    num_pos.append(pos)

# define a class for the arms of the clock
class clockArm:
    def __init__(self, color, thickness, arm_len):
        self.color = color
        self.thickness = thickness
        self.arm_len = arm_len
        self.location = [0, 0]

    # function to update the location of the arm
    def update(self, degree):
        rad = np.deg2rad(degree)
        rot_mat = np.array([[np.cos(rad), -np.sin(rad)],
                            [np.sin(rad), np.cos(rad)]]) # Rotation matrix
        trans_pos = rot_mat @ (start_pos * self.arm_len).T # Transformation
        pos = trans_pos.T # transpose
        pos[0] += center[0]
        pos[1] += center[1]
        self.location = pos

    # function to draw the arm
    def draw(self):
        pygame.draw.line(screen, self.color, center, self.location, self.thickness)

# create objects for the hour, minute, and second arms of the clock
hour_arm = clockArm(BLACK, 10, 0.5)
min_arm = clockArm(DARK_GREY, 5, 0.8)
sec_arm = clockArm(RED, 2, 1.0)

# define the main function
def main():
    global prev_hour, prev_sec, prev_min
    done = False    

    while not done: 
        # check for pygame events
        for event in pygame.event.get():
            # if the event is a 'Quit', exit the while loop
            if event.type == pygame.QUIT:
                done = True 

        # get the current time
        now = datetime.now()

        # update the arms' locations based on the current time
        hour_arm.update((now.hour % 12 + now.minute / 60) * 30)
        min_arm.update(now.minute * 6)
        sec_arm.update(now.second * 6)
        # play the bell sound if the hour has changed
        if now.minute != prev_min:
            ticktock_sound.stop()  # stop the "ticktock" sound
            bell_sound.play()
            prev_min = now.minute

        # play the tick-tock sound if the second has changed
        elif now.second != prev_sec:
            ticktock_sound.play()
            prev_sec = now.second

        # fill the screen with the white color
        screen.fill(WHITE)

        # draw the clock circle
        pygame.draw.circle(screen, BLACK, center, radius, 5) 

        # draw the minute and hour lines
        for i in range(60):
            inner = np.array([np.sin(np.deg2rad(i*6)), -np.cos(np.deg2rad(i*6))]) * (radius - 10)
            outer = np.array([np.sin(np.deg2rad(i*6)), -np.cos(np.deg2rad(i*6))]) * radius
            line_color = BLACK if i % 5 == 0 else DARK_GREY  # Hour or minute line
            pygame.draw.line(screen, line_color, center + inner, center + outer, 3 if i % 5 == 0 else 1)

        # draw the numbers on the clock
        font = pygame.font.Font('assets/Ubuntu-Bold.ttf', 30)
        for i in range(1, 13):
            num_surface = font.render(str(i), True, BLACK)
            num_rect = num_surface.get_rect(center = num_pos[i])
            screen.blit(num_surface, num_rect)

        # draw the arms of the clock
        hour_arm.draw()
        min_arm.draw()
        sec_arm.draw()

        # draw a small circle at the center of the clock
        pygame.draw.circle(screen, BLACK, center, 7)
        
        # update the display
        pygame.display.flip()
        # limit the speed of the game to the specified FPS
        clock.tick(FPS)

    # quit pygame
    pygame.quit()

if __name__ == "__main__":
    main()
