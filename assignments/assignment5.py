import pygame
import numpy as np

WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 800

GRAY = (0, 0, 0)
RED = (255, 0, 0)

CannonCenter = [100, 700.]

CREATE_POLYGON_EVENT = pygame.USEREVENT + 1
GRAVITY = np.array([0, 0.2])  # constant downward acceleration
AIR_RESISTANCE = 0.05  # air resistance coefficient


# pygame init
pygame.init()
pygame.display.set_caption("20191659 최이정")
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

sound_effect = []
#for i in range(1,25):
#    filename = f'piano/key{i:02}.mp3'
#    print(filename)
#    s = pygame.mixer.Sound(filename)
#    sound_effect.append(s)
cannon_sound = pygame.mixer.Sound('assets/mixkit-arcade-mechanical-bling-210.wav')


def getRegularPolygonVertices(nv, r):
    v = []
    for i in range(nv):
        rad = i * 2 * np.pi / nv
        x = np.cos(rad) * r
        y = np.sin(rad) * r
        v.append([x, y])
    vnp = np.array(v)
    return vnp

def collision_circle(c, p):
    d12 = c.txy - p.txy
    d12mag = np.sqrt(d12[0] ** 2 + d12[1] **2)
    r12 = c.radius + p.radius
    if d12mag < r12:
        return True
    else:
        return False

def collision_check(c, polygon_list):
    clist = []
    for p in polygon_list:
        if collision_circle(c, p):
            clist.append(p)
    return clist


class RegularPolygon:
    def __init__(self, nvertices, radius):
        self.nvertices = nvertices
        self.radius = radius
        self.color = RED
        self.linewidth = np.random.choice([0, 3, 7])
        self.p = getRegularPolygonVertices(nvertices, radius)

        self.axy = np.array([0., 0.5])
        self.vxy = np.array([0., 0.])  # initially (0, 0)
        self.txy = np.array([0., 0.])  # p's reference location, initially at (0, 0)

        self.sound = None

    def update(self, ):
        self.vxy += self.axy
        self.txy += self.vxy
        self.q = self.p + self.txy  # p after motion

        if self.txy[0] - self.radius < 0:
            self.vxy[0] *= -1.
            self.txy[0] = self.radius

        if self.txy[0] + self.radius >= WINDOW_WIDTH:
            self.vxy[0] *= -1.
            self.txy[0] = WINDOW_WIDTH - self.radius

        if self.txy[1] + self.radius >= WINDOW_HEIGHT:
            self.vxy[1] *= -1.
            self.txy[1] = WINDOW_HEIGHT - self.radius
            if self.sound:
                self.sound.play()
            # diff = self.txy[1] + self.radius - WINDOW_HEIGHT
            # self.txy[1] -= diff

        if self.txy[1] - self.radius < 0:
            self.vxy[1] *= -1.
            self.txy[1] = self.radius

    def draw(self, screen):
        pygame.draw.polygon(screen, self.color, self.q, width=self.linewidth)
        pygame.draw.line(screen, (10, 10, 10), self.txy, self.q[0])

class Star(RegularPolygon):
    def __init__(self, nvertices, radius):
        super().__init__(nvertices, radius* 1.5)
        self.linewidth = 1
    def update(self):
        super().update()
    def draw(self, screen):
        for i in range(self.nvertices):
            pygame.draw.line(screen, self.color, self.q[i], self.q[(i+2)%self.nvertices], self.linewidth)
            pygame.draw.line(screen, self.color, self.q[i], self.q[(i+4)%self.nvertices], self.linewidth)

class ExplosionStar(Star):
    def __init__(self, nvertices, radius, pos, angle):
        super().__init__(nvertices, radius)
        self.txy = pos.copy()
        self.angle = angle  # storing initial angle
        vxy_mag = np.random.uniform(7, 12)  # random initial speed
        self.vxy = np.array([np.cos(np.deg2rad(self.angle)), np.sin(np.deg2rad(self.angle))]) * vxy_mag
        self.ax = np.array([np.cos(np.deg2rad(self.angle)), np.sin(np.deg2rad(self.angle))]) * 0.5  # acceleration in the direction of movement
        self.life_tick = 20
        self.color = (np.random.randint(0, 255), np.random.randint(0, 255), np.random.randint(0, 255))  # random color
        self.fade_rate = np.random.uniform(0.01, 0.03)  # random fade rate
        self.angular_velocity = np.random.uniform(0.05, 0.1)  # add random angular velocity

    def update(self):
        super().update()
        self.color = (np.random.randint(0, 255), np.random.randint(0, 255), np.random.randint(0, 255))
        self.color = (max(0, self.color[0] - self.fade_rate), max(0, self.color[1] - self.fade_rate), max(0, self.color[2] - self.fade_rate))  # fade color
        self.angle += self.angular_velocity  # update the angle with the angular velocity
        # update the velocity and acceleration based on the new angle
        vxy_mag = np.linalg.norm(self.vxy)
        self.vxy = np.array([np.cos(np.deg2rad(self.angle)), np.sin(np.deg2rad(self.angle))]) * vxy_mag
        ax_mag = np.linalg.norm(self.ax)
        self.ax = np.array([np.cos(np.deg2rad(self.angle)), np.sin(np.deg2rad(self.angle))]) * ax_mag

        # introduce gravity and air resistance
        self.vxy += GRAVITY
        self.vxy *= (1 - AIR_RESISTANCE)
        self.ax *= (1 - AIR_RESISTANCE)


class CannonBall(RegularPolygon):
    def __init__(self, nvertices, radius):
        super().__init__(nvertices, radius)
        self.life_tick = 80

    def update(self):
        super().update()
        self.life_tick -= 1
        if self.life_tick < 20:
            self.color = (0, 0, 0)

class Cannon:
    def __init__(self):
        #self.direction_angle
        self.direction_angle = -45.
        self.position = np.array(CannonCenter, dtype='float')
        self.mag = 30.
        self.sound = None
        self.image = pygame.image.load('assets/cannon.png')  # Load the image
        self.image = pygame.transform.scale(self.image, (250, 250))  # You can adjust the size as needed
        self.rect = self.image.get_rect(center=self.position)
    def draw(self, screen):
        rad = np.deg2rad(self.direction_angle)
        self.endposition = self.position + self.mag * np.array([np.cos(rad), np.sin(rad)])*2
        self.rect.center = self.position  # Update the position
        screen.blit(self.image, self.rect)  # Draw the image

def main():
    cannon = Cannon()
    direction_angle = -45.
    cannon.sound = cannon_sound

    cannonball_list = []
    polygon_list = []
    explosion_star_list = []
    collision_list = []

    for i in range(10):
        p = RegularPolygon(np.random.randint(3, 11), 50)
        p.color = np.random.randint(0, 256, size=3)
        xi = np.random.uniform(0, WINDOW_WIDTH)
        yi = np.random.uniform(0, 100)
        p.txy = np.array([xi, yi])
        p.vxy = np.zeros(shape=2)
        p.vxy[0] = np.random.uniform(5, 11)
        p.sound = pygame.mixer.Sound('assets/mixkit-arcade-retro-changing-tab-206.wav')
        polygon_list.append(p)
    pygame.time.set_timer(CREATE_POLYGON_EVENT, 5000)  # 5000 milliseconds = 5 seconds
    
    p = Star(5, 60)
    p.color = np.random.randint(0, 256, size=3)
    p.linewidth = 7
    xi = np.random.uniform(0, WINDOW_WIDTH)
    yi = np.random.uniform(0, 100)
    p.txy = np.array([xi, yi])
    p.vxy = np.zeros(shape=2)
    p.vxy[0] = np.random.uniform(5, 11)
    polygon_list.append(p)

    done = False
    while not done:
        # 1. event check
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True
                elif event.key == pygame.K_UP:
                    cannon.direction_angle -= 3.
                elif event.key == pygame.K_DOWN:
                    cannon.direction_angle += 3.
                elif event.key == pygame.K_SPACE:
                    # cannon ball create
                    c = CannonBall(nvertices= 100, radius=7)
                    c.color = RED
                    if np.random.uniform(0, 10) < 0.3:
                        c.linewidth = 0
                    c.txy = cannon.position.copy()
                    vxy_rad = np.deg2rad(cannon.direction_angle)
                    vxy_mag = cannon.mag
                    c.vxy = np.array([np.cos(vxy_rad), np.sin(vxy_rad)]) * vxy_mag
                    cannonball_list.append(c)
                    cannon.sound.play()
            elif event.type == CREATE_POLYGON_EVENT:
                for _ in range(5):  # create 5 polygons every 5 secs
                    p = RegularPolygon(np.random.randint(3, 11), 50)
                    p.color = np.random.randint(0, 256, size=3)
                    xi = np.random.uniform(0, WINDOW_WIDTH) #위에서 polygon이 떨어지게
                    yi = np.random.uniform(0, 100)
                    p.txy = np.array([xi, yi])
                    p.vxy = np.zeros(shape=2) #초기속도
                    p.vxy[0] = np.random.uniform(5, 11) # range velocity 5 to 11
                    p.sound = pygame.mixer.Sound('assets/mixkit-arcade-retro-changing-tab-206.wav')
                    polygon_list.append(p)
        # 2. logic
        for c in cannonball_list:
            c.update()
        for p in polygon_list:
            p.update()

        # keep alive cannonballs only
        cannonball_list = [c for c in cannonball_list if c.life_tick > 0]

        for c in cannonball_list:
            clist = collision_check(c, polygon_list)
            if clist:
                for p in clist:
                    # remove the collided polygons from polygon_list and add to collision_list
                    polygon_list.remove(p)
                    collision_list.append(p)
        new_explosion_star_list = [] # 충돌시 explosion 담기위해 선언
        for p in collision_list:
            for angle in range(0, 360, 36):  # angles for 10 directions
                new_explosion_star_list.append(ExplosionStar(6, 5, p.txy, angle))
        explosion_star_list.extend(new_explosion_star_list)
        collision_list.clear()  # clear the collision_list for the next frame

        # update and clean up the explosion stars
        for star in explosion_star_list:
            star.update()
            star.life_tick -= 1
        explosion_star_list = [star for star in explosion_star_list if star.life_tick > 0]
        # lifetick이 0보다 큰 star만 남아있게

        # 3. drawing
        screen.fill(GRAY)

        pygame.draw.circle(screen, (0, 0, 0), CannonCenter, 10)
        cannon.draw(screen)

        for p in polygon_list:
            
            p.draw(screen) 

        for c in cannonball_list:
            c.draw(screen)
        
        for star in explosion_star_list:
            p.color = np.random.randint(0, 256, size=3)
            star.draw(screen)
        

        # 4.
        pygame.display.flip()
        clock.tick(30)

    pass


if __name__ == "__main__":
    main()