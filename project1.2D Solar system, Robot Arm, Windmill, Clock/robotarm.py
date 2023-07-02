import pygame
import numpy as np

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 800

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

def Rmat(deg):
    rad = np.deg2rad(deg)
    c = np.cos(rad)
    s = np.sin(rad)
    R = np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])
    return R

def Tmat(a, b):
    H = np.eye(3)
    H[0, 2] = a
    H[1, 2] = b
    return H

pygame.init()

pygame.display.set_caption("20191659 최이정")

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

clock = pygame.time.Clock()

rec = np.array([[0, 0, 1], [150, 0, 1], [150, 30, 1], [0, 30, 1]])
rec = rec.T

joint1 = np.array([15, 15, 1])  # Joint position of the first arm
joint2 = np.array([135, 15, 1])  # Joint position of the second arm
# Calculate the position of the third joint based on the second joint position
joint3 = np.array([joint2[0] - 120, joint2[1], 1])  # Joint position of the third arm

Rspeed1 = 3  # Rotation speed of the first arm
Rspeed2 = 3  # Rotation speed of the second arm
Rspeed3 = 3  # Rotation speed of the third arm

# Gripper characteristics
gripper_width = 30  # width of the gripper jaw (can be adjusted as needed)
gripper_height = 15  # height of the gripper jaw (can be adjusted as needed)
gripper_open = False  # state of the gripper
gripper_distance = 0  # distance between the jaws
gripper_speed = 1  # speed of opening/closing the jaws

gripper1 = np.array([[150, 15, 1], [160 + gripper_height, 15, 1], [160 + gripper_height, 15 - gripper_width / 2, 1], [150, 15 - gripper_width / 2, 1]]).T
gripper2 = np.array([[150, -15, 1], [160 + gripper_height, -15, 1], [160 + gripper_height, -15 + gripper_width / 2, 1], [150, -15 + gripper_width / 2, 1]]).T

done = False

font = pygame.font.Font(None, 24)  # Font for the instructions

# New lines: Preparing your instruction texts
instr1 = font.render("Move First arm: press a/b", True, BLACK)
instr2 = font.render("Move Second arm: press c/d", True, BLACK)
instr3 = font.render("Move Third arm: press e/f", True, BLACK)
instr4 = font.render("open/close Grippers: press q/w", True, BLACK)

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    screen.fill(WHITE)

    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_a]:
        Rspeed1 -= 1
        text = font.render("First Arm: Rotate Counter Clockwise", True, BLACK)
        screen.blit(text, (10, 10))
    if keys[pygame.K_b]:
        Rspeed1 += 1
        text = font.render("First Arm: Rotate Clockwise", True, BLACK)
        screen.blit(text, (10, 10))
    if keys[pygame.K_c]:
        Rspeed2 -= 1
        text = font.render("Second Arm: Rotate Counter Clockwise", True, BLACK)
        screen.blit(text, (10, 10))
    if keys[pygame.K_d]:
        Rspeed2 += 1
        text = font.render("Second Arm: Rotate Clockwise", True, BLACK)
        screen.blit(text, (10, 10))
    if keys[pygame.K_e]:
        Rspeed3 -= 1
        text = font.render("Third Arm: Rotate Counter Clockwise", True, BLACK)
        screen.blit(text, (10, 10))
    if keys[pygame.K_f]:
        Rspeed3 += 1
        text = font.render("Third Arm: Rotate Clockwise", True, BLACK)
        screen.blit(text, (10, 10))
    if keys[pygame.K_q]:
        gripper_open = True
    if keys[pygame.K_w]:
        gripper_open = False
    
    H1 = Tmat(500 - joint1[0], 400 - joint1[1]) @ Rmat(Rspeed1)
    Trec1 = H1 @ rec
    Tjoint1 = H1 @ joint1
    pygame.draw.polygon(screen, BLACK, Trec1[0:2, :].T, 4)
    pygame.draw.circle(screen, RED, Tjoint1[:2], 3)

    Tjoint2 = H1 @ joint2
    pygame.draw.circle(screen, RED, Tjoint2[:2], 3)

    H2 = Tmat(Tjoint2[0], Tjoint2[1]) @ Rmat(Rspeed2) @ Tmat(-Tjoint2[0], -Tjoint2[1]) @ H1
    Trec2 = H2 @ rec

    # Update the position of the third joint based on the second joint position
    Tjoint3 = H2 @ joint3

    pygame.draw.polygon(screen, BLACK, Trec2[0:2, :].T, 4)
    pygame.draw.circle(screen, RED, Tjoint3[:2], 3)

    H3 = Tmat(Tjoint3[0], Tjoint3[1]) @ Rmat(Rspeed3) @ Tmat(-Tjoint3[0], -Tjoint3[1]) @ H2
    Trec3 = H3 @ rec

    pygame.draw.polygon(screen, BLACK, Trec3[0:2, :].T, 4)

    # Update the position of the jaws based on the state of the gripper
    if gripper_open:
        gripper_distance = min(gripper_distance + gripper_speed, gripper_width / 2)  # cannot exceed the half width of the jaw
    else:
        gripper_distance = max(gripper_distance - gripper_speed, 0)  # cannot be less than 0

    # Update the positions of the jaws
    gripper1[1, 2] = 15 - gripper_distance  # update the y-coordinate of the bottom points of the first jaw
    gripper2[1, 2] = -15 + gripper_distance  # update the y-coordinate of the top points of the second jaw

    # Apply the transformation matrices to the jaws
    Tgripper1 = H3 @ gripper1
    Tgripper2 = H3 @ gripper2

    # Draw the jaws on the screen
    pygame.draw.polygon(screen, BLACK, Tgripper1[0:2, :].T, 4)
    pygame.draw.polygon(screen, BLACK, Tgripper2[0:2, :].T, 4)
    
    # New lines: Adding the instructions to the screen
    screen.blit(instr4, (10, WINDOW_HEIGHT - 90))
    screen.blit(instr1, (10, WINDOW_HEIGHT - 70))
    screen.blit(instr2, (10, WINDOW_HEIGHT - 50))
    screen.blit(instr3, (10, WINDOW_HEIGHT - 30))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
