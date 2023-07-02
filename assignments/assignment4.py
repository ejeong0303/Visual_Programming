import pygame
import numpy as np

WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 800

GRAY = (200, 200, 200)
RED = (255, 0, 0)

CannonCenter = [100, 700.]

CREATE_POLYGON_EVENT = pygame.USEREVENT + 1

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
        self.vdeg = np.random.choice([5, 10, 15, 20]) #degree/frame
        self.deg = 0

        self.sound = None

    def update(self, ):
        self.vxy += self.axy
        self.txy += self.vxy
        self.deg += self.vdeg
        R = Rmat(self.deg)
        qt = R @ self.p.T
        q = qt.T

        #self.q = self.p + self.txy  # p after motion
        self.q = q + self.txy 

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
        self.life_tick = 150
        self.color = (np.random.randint(0, 255), np.random.randint(0, 255), np.random.randint(0, 255))  # random color
        self.linewidth = 1
    def update(self):
        super().update()
        #self.life_tick -= 1
        #if self.life_tick < 20:
        #    self.color = (0, 0, 0)
    def draw(self, screen):
        #pygame.draw.polygon(screen, self.color, self.q)
        for i in range(self.nvertices):
            pygame.draw.line(screen, self.color, self.q[i], self.q[(i+2)%self.nvertices], self.linewidth)
            pygame.draw.line(screen, self.color, self.q[i], self.q[(i+4)%self.nvertices], self.linewidth)
        
        #for i in range(self.nvertices):
        #    pygame.draw.line(screen, self.color, self.q[i], self.q[(i+2)%self.nvertices], self.linewidth)

class ExplosionStar(Star):
    def __init__(self, nvertices, radius, pos, angle):
        super().__init__(nvertices, radius)
        self.txy = pos.copy()
        vxy_rad = np.deg2rad(angle)
        vxy_mag = 10
        self.vxy = np.array([np.cos(vxy_rad), np.sin(vxy_rad)]) * vxy_mag
        self.life_tick = 20
        self.color = (np.random.randint(0, 255), np.random.randint(0, 255), np.random.randint(0, 255))  # random color

    # add an update method to change color every frame
    def update(self):
        super().update()
        self.color = (np.random.randint(0, 255), np.random.randint(0, 255), np.random.randint(0, 255))

class CannonBall(RegularPolygon):
    def __init__(self, nvertices, radius):
        super().__init__(nvertices, radius)
        self.life_tick = 80

    def update(self):
        super().update()
        self.life_tick -= 1
        if self.life_tick < 20:
            self.color = (0, 0, 0)

def getRectangle(width, height, x = 0, y = 0):
    v = np.array([[x, y], 
                 [x+width, y],
                 [x+width, y+height],
                 [x, y+height]],
                 dtype = "float")
    return v

def Rmat(deg):
    theta = np.deg2rad(deg)
    c = np.cos(theta)
    s = np.sin(theta)
    R = np.array([[c,-s], [s,c]])
    return R

def R3mat(deg):
    theta = np.deg2rad(deg)
    c = np.cos(theta)
    s = np.sin(theta)
    R = np.array([[c,-s,0], [s,c,0], [0,0,1]])
    return R

def T3mat(a, b):
    t = np.eye(3)
    t[0, 2] = a
    t[1, 2] = b
    return t

class Cannon:
    def __init__(self):
        #self.direction_angle
        self.direction_angle = -45.
        self.position = np.array(CannonCenter, dtype = 'float')
        self.v = getRectangle(100, 20)
        self.mag = 30.
        self.sound = None
        self.p = getRectangle(200, 20)
        self.pt = self.p.T

        self.pp = getRectangle(250, 50)

    def update(self,):
        #apply a geometric transformation to self.y, so that the result becomes a desired view
        R = Rmat(self.direction_angle)
        p1 = self.p + [0, -10] #translation
        self.qt = R @ p1.T #rotation
        self.q = self.qt.T 
        self.q = self.q + self.position #translation

        M = T3mat(self.position[0], self.position[1]) @ R3mat(self.direction_angle) @ T3mat(0, -25)
        #print("M", M)
        R2x2 = M[0:2, 0:2]
        tvec = M[0:2, 2]
        self.Q = (R2x2 @ self.pp.T).T + tvec


    def draw(self, screen):
        rad = np.deg2rad(self.direction_angle)
        self.endposition = self.position + self.mag * np.array([np.cos(rad), np.sin(rad)])*3
        pygame.draw.line(screen, (0,0,0), self.position, self.endposition, 8)
        pygame.draw.polygon(screen, (0,0,0), self.q, width = 3)
        pygame.draw.circle(screen, (0, 0, 0), CannonCenter, 5)
        pygame.draw.polygon(screen, (100, 200, 250), self.Q, width = 2)

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

    pRect = getRectangle(300, 40, 400, 350) #(4,2)
    rcenter = np.array([(300)/2. + 400, (40)/2.+350])
    deg = 0.

    done = False
    while not done:

        #arm = getRectangle(100, 20)
        #angle1 = 30

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
                    c = CannonBall(nvertices=5, radius=35)
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
                for _ in range(5):  # create 5 polygons
                    p = RegularPolygon(np.random.randint(3, 11), 50)
                    p.color = np.random.randint(0, 256, size=3)
                    xi = np.random.uniform(0, WINDOW_WIDTH)
                    yi = np.random.uniform(0, 100)
                    p.txy = np.array([xi, yi])
                    p.vxy = np.zeros(shape=2)
                    p.vxy[0] = np.random.uniform(5, 11)
                    p.sound = pygame.mixer.Sound('assets/mixkit-arcade-retro-changing-tab-206.wav')
                    polygon_list.append(p)
        # 2. logic
        cannon.update()

        for c in cannonball_list:
            c.update()
        for p in polygon_list:
            p.update()

        # keep alive cannonballs only
        cannonball_list = [c for c in cannonball_list if c.life_tick > 0]

        #for c in cannonball_list:
        #    for p in polygon_list:
        #        if collision_circle(c, p):
        #           p.color = (10, 10, 10)
                   #make_firework()
        #           f = RegularPolygon
        for c in cannonball_list:
            clist = collision_check(c, polygon_list)
            if clist:
                for p in clist:
                    # remove the collided polygons from polygon_list and add to collision_list
                    polygon_list.remove(p)
                    collision_list.append(p)
        new_explosion_star_list = []
        for p in collision_list:
            for angle in range(0, 360, 45):  # angles for 8 directions
                new_explosion_star_list.append(ExplosionStar(6, 7, p.txy, angle))
        explosion_star_list.extend(new_explosion_star_list)
        collision_list.clear()  # clear the collision_list for the next frame

        # update and clean up the explosion stars
        for star in explosion_star_list:
            star.update()
            star.life_tick -= 1
        explosion_star_list = [star for star in explosion_star_list if star.life_tick > 0]

        # 3. drawing
        screen.fill(GRAY)

        
        cannon.draw(screen)

        for p in polygon_list:
            
            p.draw(screen) 

        for c in cannonball_list:
            c.draw(screen)
        
        for star in explosion_star_list:
            p.color = np.random.randint(0, 256, size=3)
            star.draw(screen)

        #M = T3mat(CannonCenter[0], CannonCenter[1] @ R3mat(angle1) @ T3mat(0, -h/2.))
        #pygame.draw.polygon(M, arm)
        
        #pygame.draw.polygon(screen, (255, 200, 210), pRect, 3)
        deg += 1
        R = Rmat(deg)
        q1 = pRect - rcenter #rcenter가 rectangle의 원점
        q2t = R @ q1.T
        q2 = q2t.T
        q3 = q2 + rcenter
        
        pygame.draw.polygon(screen, (255, 200, 210), q3)
        pygame.draw.circle(screen, (0,0,0), rcenter, 3)
        # 4.
        pygame.display.flip()
        clock.tick(30)

    pass


if __name__ == "__main__":
    main()