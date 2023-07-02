import pygame
import os
import numpy as np
import math

# Window size
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (51, 51, 255)
ORANGE = (255, 165, 0)
GRAY = (128, 128, 128)

# FPS
FPS = 60

pygame.init()
pygame.mixer.init()
pygame.display.set_caption("20191659 최이정")
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

ufo_disappear_sound = pygame.mixer.Sound('assets/ufo.mp3')  # Load the sound

def ellipseRotate(degree, degreeSpeed, a, b, center_x, center_y):
    degree += degreeSpeed
    x = int(math.cos(degree*2*math.pi/360)*a) + center_x
    y = int(math.sin(degree*2*math.pi/360)*b) + center_y
    return degree, [x, y]

class Planet():
    def __init__(self, color, radius, speed, a, b, center_x, center_y, self_rotation_speed):
        self.color = color
        self.radius = radius
        self.degree = 0
        self.degreeSpeed = speed
        self.a = a
        self.b = b
        self.center_x = center_x
        self.center_y = center_y
        self.loc = [center_x, center_y]
        self.self_rotation_speed = self_rotation_speed
        self.self_rotation_degree = 0
    
    def update(self):
        self.degree, self.loc = ellipseRotate(self.degree, self.degreeSpeed, self.a, self.b, self.center_x, self.center_y)
        self.self_rotation_degree += self.self_rotation_speed  # Increment the rotation degree for self-rotation
    
    def draw(self):
        pygame.draw.circle(screen, self.color, self.loc, self.radius)
        # Draw a line from the center to the end of the radius based on the self-rotation
        end_x = self.loc[0] + self.radius * math.cos(math.radians(self.self_rotation_degree))
        end_y = self.loc[1] + self.radius * math.sin(math.radians(self.self_rotation_degree))
        pygame.draw.line(screen, BLACK, self.loc, (end_x, end_y))


class Moon():
    def __init__(self, color, radius, speed, distance, parent_planet, self_rotation_speed):
        self.color = color
        self.radius = radius
        self.speed = speed
        self.distance = distance
        self.parent_planet = parent_planet
        self.self_rotation_speed = self_rotation_speed
        self.self_rotation_degree = 0
    
    def update(self):
        self.self_rotation_degree += self.speed  # Increment the rotation degree for self-rotation
    
    def draw(self):
        parent_x, parent_y = self.parent_planet.loc
        x = int(parent_x + self.distance * math.cos(math.radians(self.self_rotation_degree)))
        y = int(parent_y + self.distance * math.sin(math.radians(self.self_rotation_degree)))
        pygame.draw.circle(screen, self.color, (x, y), self.radius)
        # Draw a line from the center to the end of the radius based on the self-rotation
        end_x = x + self.radius * math.cos(math.radians(self.self_rotation_degree))
        end_y = y + self.radius * math.sin(math.radians(self.self_rotation_degree))
        pygame.draw.line(screen, BLACK, (x, y), (end_x, end_y))

class Sun():
    def __init__(self, color, radius, center_x, center_y):
        self.color = color
        self.radius = radius
        self.loc = [center_x, center_y]
        self.flame_length = 20  # Length of the "flames"
        self.flame_angle = 15  # Angle between flames in degrees
        
    def draw(self):
        pygame.draw.circle(screen, self.color, self.loc, self.radius)  # Draw the sun itself

        # Draw halo
        halo_color = (255, 140, 0)  # A color for the halo (light orange)
        pygame.draw.circle(screen, halo_color, self.loc, self.radius + 10, 2)  # Draw the halo around the sun

        # Draw flames
        flame_color = (255, 69, 0)  # A color for the flames (orange red)
        for angle in range(0, 360, self.flame_angle):
            end_x = self.loc[0] + (self.radius + self.flame_length) * math.cos(math.radians(angle))
            end_y = self.loc[1] + (self.radius + self.flame_length) * math.sin(math.radians(angle))
            pygame.draw.line(screen, flame_color, self.loc, (end_x, end_y), 2)


class Star():
    def __init__(self):
        # Set initial position randomly within the window
        self.x = np.random.uniform(0, WINDOW_WIDTH)
        self.y = np.random.uniform(0, WINDOW_HEIGHT)

        # Set initial color to white
        self.color = WHITE

        # Set initial brightness randomly within a certain range
        self.brightness = np.random.uniform(70, 100)

        # Set a random change in brightness for the glitter effect
        self.delta_brightness = np.random.uniform(-2, 2)

    def update(self):
        # Change brightness for the glitter effect
        self.brightness += self.delta_brightness

        # If brightness goes out of bounds, reverse the change in brightness
        if self.brightness < 70 or self.brightness > 100:
            self.delta_brightness = -self.delta_brightness

        # Update color with new brightness
        self.color = (int(self.brightness), int(self.brightness), int(self.brightness))

    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 1)

        

class UFO():
    def __init__(self, image, sound, speed, x, y):
        self.image = pygame.transform.scale(image, (40, 40))  # Scale the image
        self.sound = ufo_disappear_sound  # Assign sound
        self.max_speed = speed
        self.loc = [x, y]
        self.frame_counter = 0  # Frame counter for changing direction
        self.zigzag_direction = 1  # Start moving to the right
        self.visible = True  # UFO starts out visible
        self.visibility_timer = 0  # Counter for visibility toggling
        self.visibility_interval = np.random.randint(60, 180)  # Random interval between 1 and 3 seconds at 60 FPS
        self.zigzag_amplitude = 0.01  # Starting zigzag amplitude

    def update(self):
        was_visible = self.visible
        if self.visible:  # Only update position when visible
            # Update location using the zigzag pattern
            self.loc[0] += self.zigzag_direction * self.max_speed * np.random.random()  # Random speed in the direction
            self.loc[1] += self.zigzag_direction * self.zigzag_amplitude * np.sin(self.frame_counter)

            # Ensure UFO stays within window bounds
            self.loc[0] = np.clip(self.loc[0], 0, WINDOW_WIDTH - self.image.get_width())
            self.loc[1] = np.clip(self.loc[1], 0, WINDOW_HEIGHT - self.image.get_height())

            # Update frame counter and change direction if necessary
            self.frame_counter += 1
            if self.frame_counter % 100 == 0:  # Change direction every 100 frames
                self.zigzag_direction *= -1  # Switch direction
                self.zigzag_amplitude *= 1.05  # Increase the zigzag amplitude

        # Update visibility timer and toggle visibility if necessary
        self.visibility_timer += 1
        if self.visibility_timer % self.visibility_interval == 0:
            self.visible = not self.visible  # Toggle visibility
            self.visibility_interval = np.random.randint(60, 180)  # Set a new visibility interval
            self.visibility_timer = 0  # Reset visibility timer
        if was_visible and not self.visible:  # If the UFO just disappeared
            self.sound.play()  # Play the sound

    def draw(self):
        if self.visible:  # Only draw when visible
            screen.blit(self.image, self.loc)


# Load and scale UFO images
ufo_image1 = pygame.image.load('assets/ufo1.png')
ufo_image1 = pygame.transform.scale(ufo_image1, (40, 40))

ufo_image2 = pygame.image.load('assets/ufo9.png')
ufo_image2 = pygame.transform.scale(ufo_image2, (40, 40))

# Create UFOs
ufo1 = UFO(ufo_image1, ufo_disappear_sound, 7, np.random.uniform(0, WINDOW_WIDTH), np.random.uniform(0, WINDOW_HEIGHT))
ufo2 = UFO(ufo_image2, ufo_disappear_sound, 7, np.random.uniform(0, WINDOW_WIDTH), np.random.uniform(0, WINDOW_HEIGHT))

# Sun (red circle) creation
sun = Sun(RED, 50, WINDOW_WIDTH/2, WINDOW_HEIGHT/2)

# Earth (blue circle) creation
earth = Planet(BLUE, 30, 0.1, 300, 200, WINDOW_WIDTH/2, WINDOW_HEIGHT/2, 1)  # counterclockwise

# Mars (orange circle) creation
mars = Planet(ORANGE, 45, 0.07, 500, 400, WINDOW_WIDTH/2, WINDOW_HEIGHT/2, -1)  # clockwise

# Earth's Moon creation
moon = Moon(GRAY, 10, 1, 100, earth, 1)  # counterclockwise

# Mars' Moons creation
phobos = Moon(GRAY, 8, 1.5, 80, mars, 1)  # counterclockwise
deimos = Moon(GRAY, 6, 2, 120, mars, -1)  # clockwise

def main():

    # Create a list of stars
    stars = [Star() for _ in range(1000)]

    done = False    
    while not done: 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True 

        # Game logic
        earth.update()
        moon.update()
        mars.update()
        phobos.update()
        deimos.update()
        ufo1.update()
        ufo2.update()
        # Update stars
        for star in stars:
            star.update()

        # Screen filling
        screen.fill(BLACK)

        # Drawing
        for star in stars:
            star.draw()
        ufo1.draw()
        ufo2.draw()
        sun.draw()

        # Drawing Earth's orbit path
        pygame.draw.ellipse(screen, WHITE, [WINDOW_WIDTH/2 - earth.a, WINDOW_HEIGHT/2 - earth.b, 2*earth.a, 2*earth.b], 1)

        # Drawing Earth and Moon
        earth.draw()
        moon.draw()

        # Drawing Mars' orbit path
        pygame.draw.ellipse(screen, WHITE, [WINDOW_WIDTH/2 - mars.a, WINDOW_HEIGHT/2 - mars.b, 2*mars.a, 2*mars.b], 1)

        # Drawing Mars and Moons
        mars.draw()
        phobos.draw()
        deimos.draw()

        # Screen update
        pygame.display.flip()
        clock.tick(FPS)

    # Quit game
    pygame.mixer.quit()
    pygame.quit()

if __name__ == "__main__":
    main()
