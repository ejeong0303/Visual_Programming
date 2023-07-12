import pygame
import random
from os import path

img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'snd')

WIDTH = 480
HEIGHT = 600
FPS = 60
POWERUP_TIME = 5000
SPECIAL_MOB_EVENT = pygame.USEREVENT + 1


# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PINK = (255, 102, 204)

# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Supermario's Adventure")
clock = pygame.time.Clock()

def draw_text(surf, text, size, x, y):
    font = pygame.font.Font('FinalProject/tlpsmb.ttf', size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

font_name = pygame.font.match_font('arial')
def draw_score(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def newbossbullets():
    bb = bossBullet()
    all_sprites.add(bb)
    bossbullets.add(bb)

def newflymob():
    m = fly_Mob()
    all_sprites.add(m)
    flymobs.add(m)

def newgroundmob():
    m = ground_Mob()
    all_sprites.add(m)
    groundmobs.add(m)

def newstaymob():
    m = stay_Mob()
    all_sprites.add(m)
    staymobs.add(m)

def draw_shield_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)

def draw_boss_shield_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, RED, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)

def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)

def character_selection():
    characters = {
        'peach': pygame.transform.scale(pygame.image.load(path.join(img_dir, 'peach.png')).convert(), (100, 150)),
        'mario': pygame.transform.scale(pygame.image.load(path.join(img_dir, 'mario.png')).convert(), (150, 150)),
        'luiggi': pygame.transform.scale(pygame.image.load(path.join(img_dir, 'luiggi.png')).convert(), (150, 150)),
        'yoshi': pygame.transform.scale(pygame.image.load(path.join(img_dir, 'yoshi.png')).convert(), (150, 150)),
    }

    highlights = {
        'peach': PINK,
        'mario': RED,
        'luiggi': GREEN,
        'yoshi': YELLOW
    }

    selected = None
    hover = None
    while selected is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if 0 < x < 240:
                    if 120 < y < 270:
                        selected = 'mario'
                    elif 360 < y < 510:
                        selected = 'yoshi'
                elif 240 < x < 480:
                    if 120 < y < 270:
                        selected =  'luiggi'
                    elif 360 < y < 510:
                        selected = 'peach'

            elif event.type == pygame.MOUSEMOTION:
                x, y = pygame.mouse.get_pos()
                if 0 < x < 240:
                    if 120 < y < 270:
                        hover = 'mario'
                    elif 360 < y < 510:
                        hover = 'yoshi'
                elif 240 < x < 480:
                    if 120 < y < 270:
                        hover = 'luiggi'
                    elif 360 < y < 510:
                        hover = 'peach'
                else:
                    hover = None

        screen.fill(BLACK)
        draw_text(screen, "SELECT A PLAYER", 40, WIDTH / 2, 50)
        screen.blit(characters['peach'], (280, 360))
        screen.blit(characters['mario'], (50, 120))
        screen.blit(characters['luiggi'], (280, 120))
        screen.blit(characters['yoshi'], (50, 360))

        # draw hover highlight
        if hover is not None:
            rect_width = characters[hover].get_rect().width  # Get the width of the image
            pygame.draw.rect(screen, highlights[hover], (280 if hover in ['peach', 'luiggi'] else 50, 360 if hover in ['peach', 'yoshi'] else 120, rect_width, 150), 5)

        # draw names
        draw_text(screen, "Peach", 20, 330, 520)
        draw_text(screen, "Mario", 20, 100, 280)
        draw_text(screen, "Luiggi", 20, 330, 280)
        draw_text(screen, "Yoshi", 20, 100, 520)

        pygame.display.flip()

    return selected

class Player(pygame.sprite.Sprite):
    def __init__(self, character, bullet_img):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(path.join(img_dir, f'{character}.png')).convert()
        self.image = pygame.transform.scale(self.image, (70, 70))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 20
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.bullet_img = bullet_img
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 20
        self.speedx = 0
        self.speedy = 0
        self.shield = 100
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        self.power = 1
        self.power_time = pygame.time.get_ticks()

    def update(self):
        # timeout for powerups
        if self.power >= 2 and pygame.time.get_ticks() - self.power_time > POWERUP_TIME:
            self.power -= 1
            self.power_time = pygame.time.get_ticks()
        
        if self.rect.bottom == HEIGHT - 100:
            self.speedy = 3
            
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -8
        if keystate[pygame.K_RIGHT]:
            self.speedx = 8
        if keystate[pygame.K_UP]:
            self.speedy = -2
            jump_sound.play()
        if keystate[pygame.K_DOWN]:
            self.speedy = 4
        if keystate[pygame.K_SPACE]:
            self.shoot()
        if keystate[pygame.K_d]:
            self.shoot()
        if keystate[pygame.K_f]:
            self.shoot()

        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > HEIGHT - 20:
            self.rect.bottom = HEIGHT - 20
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.colliderect(platform1.rect) and self.rect.bottom < platform1.rect.bottom:
            self.rect.bottom = platform1.rect.top
        if self.rect.colliderect(platform2.rect) and self.rect.bottom < platform2.rect.bottom:
            self.rect.bottom = platform2.rect.top
    

    def powerup(self):
        self.power += 1
        self.power_time = pygame.time.get_ticks()

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            keystate = pygame.key.get_pressed()
            if self.power == 1:
                bullet = Bullet(self.rect.centerx, self.rect.bottom, self.bullet_img)
                if keystate[pygame.K_d]:
                    bullet = Bullet(self.rect.centerx, self.rect.bottom, self.bullet_img, speedx=-10, speedy=0)
                elif keystate[pygame.K_f]:
                    bullet = Bullet(self.rect.centerx, self.rect.bottom, self.bullet_img, speedx=10, speedy=0)
                all_sprites.add(bullet)
                bullets.add(bullet)
                shoot_sound.play()
            if self.power >= 2:
                bullet1 = Bullet(self.rect.left, self.rect.centery, self.bullet_img)
                bullet2 = Bullet(self.rect.right, self.rect.centery, self.bullet_img)
                if keystate[pygame.K_d]:
                    bullet1 = Bullet(self.rect.centerx, self.rect.bottom, self.bullet_img, speedx=-10, speedy=0)
                    bullet2 = Bullet(self.rect.centerx, self.rect.bottom, self.bullet_img, speedx=-10, speedy=0)
                elif keystate[pygame.K_f]:
                    bullet1 = Bullet(self.rect.centerx, self.rect.bottom, self.bullet_img, speedx=10, speedy=0)
                    bullet2 = Bullet(self.rect.centerx, self.rect.bottom, self.bullet_img, speedx=10, speedy=0)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
                shoot_sound.play()

    def hide(self):
        # hide the player temporarily
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 200)

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        #self.speedx = 1
    def update(self):

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
            #self.speedx = -1
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > HEIGHT - 20:
            self.rect.bottom = HEIGHT - 20
        if self.rect.top < 0:
            self.rect.top = 0
class Bowser(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = pygame.image.load(path.join(img_dir, "bowser2.png")).convert_alpha()
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 5)  # position the boss
        self.radius = int(self.rect.width * .85 / 2)
        self.shield = 100
        self.speedx = 2
        self.last_shot = pygame.time.get_ticks()
        self.shoot_delay = 1000  # the boss will shoot every 1 second
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()

    def update(self):
        if not self.hidden:
            # move the boss mob towards the player
            player = pygame.sprite.spritecollideany(self, player_group)  # find the player sprite
            if player:
                if player.rect.centerx < self.rect.centerx:
                    self.speedx = -2  # move left
                elif player.rect.centerx > self.rect.centerx:
                    self.speedx = 2  # move right
                else:
                    self.speedx = 0  # stop moving if already at the same x position

            self.rect.x += self.speedx
            # change direction if hit the edge
            if self.rect.right > WIDTH or self.rect.left < 0:
                self.speedx *= -1

            # boss shoots bullet
            now = pygame.time.get_ticks()
            if now - self.last_shot > self.shoot_delay:
                self.last_shot = now
                bossbullet = bossBullet(self.rect.centerx, self.rect.bottom, boss_bullet_image, speedx=0, speedy=10)
                all_sprites.add(bossbullet)
                bossbullets.add(bossbullet)
            
        # unhide if hidden
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT / 5

    def hide(self):
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 200)

class fly_Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(flymob_images)
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 / 2)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.bottom = random.randrange(-80, -20)
        self.speedy = random.randrange(1, 6)
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        self.swing_range = random.randrange(20, 50)
        self.swing_direction = random.choice([-1, 1])
        self.last_update = pygame.time.get_ticks()

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        self.rotate()
        self.rect.x += self.swing_direction  # Apply swinging left or right
        self.rect.y += self.speedy
        if abs(self.rect.x - self.rect.centerx) >= self.swing_range:
            self.swing_direction *= -1  # Reverse swinging direction if reached swing range
        if self.rect.top > HEIGHT + 10 or self.rect.left < -100 or self.rect.right > WIDTH + 100:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)

class ground_Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.mob_type = random.choice(["Goomba.png", "villiankoopa.png", 'koopatroopa_med.png', 'koopatroopa3_med.png'])
        self.image_orig = pygame.image.load(path.join(img_dir, self.mob_type)).convert()
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 / 2)
        self.spawn_left = random.choice([True, False])  # Randomly decide if the mob spawns from the left
        if self.spawn_left:
            self.rect.x = 0  # Spawns from left
            self.speedx = random.choice([1, 2])  # Moves to the right
        else:
            self.rect.x = WIDTH - self.rect.width  # Spawns from right
            self.speedx = random.choice([-1, -2])  # Moves to the left
        self.rect.y = HEIGHT - 60

    def update(self):
        self.rect.x += self.speedx
        if self.rect.left < 0 or self.rect.right > WIDTH:
            self.kill()
            # Add a chance to spawn a power up when a mob is killed
            if random.random() > 0.9:
                pow = Pow(self.rect.center)
                all_sprites.add(pow)
                powerups.add(pow)

class stay_Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.mob_type = random.choice(["villianflower.png", "villianflower1.png"])
        self.image_orig = pygame.image.load(path.join(img_dir, self.mob_type)).convert()
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.rect.x = random.choice([60, 420])
        self.rect.y = HEIGHT - self.rect.height

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, image, speedx=0, speedy=-10):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = speedy
        self.speedx = speedx

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        # kill if it moves off the top of the screen or off the sides
        if self.rect.bottom < 0 or self.rect.left < 0 or self.rect.right > WIDTH:
            self.kill()

class bossBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, image, speedx=0, speedy=10):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = speedy
        self.speedx = speedx

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        # kill if it moves off the top of the screen or off the sides
        if self.rect.bottom < 0 or self.rect.left < 0 or self.rect.right > WIDTH:
            self.kill()

class Pow(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['shield','shield_gold', 'gun'])
        self.image = powerup_images[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 5

    def update(self):
        self.rect.y += self.speedy
        # kill if it moves off the top of the screen
        if self.rect.top > HEIGHT:
            self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 75

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

def show_go_screen():
    screen.blit(background, background_rect)
    draw_text(screen, "SUPERMARIO'S ADVENTURE", 30, WIDTH / 2, HEIGHT / 4)
    draw_text(screen, "Arrow keys move, Space to fire", 22,
              WIDTH / 2, HEIGHT / 2)
    draw_text(screen, "Press a key to begin", 18, WIDTH / 2, HEIGHT * 3 / 4 - 30)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False

# Load all game graphics
background = pygame.image.load(path.join(img_dir, "new1.png")).convert()
background_rect = background.get_rect()
bossbackground = pygame.image.load(path.join(img_dir, "bossbackground1.jpg")).convert()
bossbackground_rect = background.get_rect()
characterbackground = pygame.image.load(path.join(img_dir, "characterbackground.png")).convert()
player_img = pygame.image.load(path.join(img_dir, "peach.png")).convert()
player_img = pygame.transform.scale(player_img, (40, 40))
player_mini_img = pygame.transform.scale(player_img, (40, 40))
player_mini_img.set_colorkey(BLACK)
platform1_image = pygame.image.load(path.join(img_dir, "brickplatform1.png")).convert_alpha()
platform1_image = pygame.transform.scale(platform1_image, (60, 20))
platform1_image.set_colorkey(BLACK)
platform2_image = pygame.image.load(path.join(img_dir, "brickplatform2.png")).convert_alpha()
platform2_image = pygame.transform.scale(platform2_image, (40, 20))
platform2_image.set_colorkey(BLACK)

bullet_images = {
    'peach': pygame.image.load(path.join(img_dir, 'peachheart1.png')).convert(),
    'mario': pygame.image.load(path.join(img_dir, 'mariofireball1.png')).convert(),
    'luiggi': pygame.image.load(path.join(img_dir, 'luiggifireball1.png')).convert(),
    'yoshi': pygame.image.load(path.join(img_dir, 'yoshiegg1.png')).convert(),
}

specialmob_img = pygame.image.load(path.join(img_dir, "bowser.png")).convert()
boss_bullet_image = pygame.image.load(path.join(img_dir, "laserRed16.png")).convert_alpha()
boss_bullet_image.set_colorkey(BLACK)
flymob_images = []
flymob_list = ['koopatroopa1_large.png', 'koopatroopa2_large.png',
                'flygoomba.png','flygoomba.png'
            ]
for img in flymob_list:
    flymob_images.append(pygame.image.load(path.join(img_dir, img)).convert())

explosion_anim = {}
explosion_anim['lg'] = []
explosion_anim['sm'] = []
explosion_anim['player'] = []
for i in range(9):
    filename = 'regularExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    img_lg = pygame.transform.scale(img, (75, 75))
    explosion_anim['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img, (32, 32))
    explosion_anim['sm'].append(img_sm)
    filename = 'sonicExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    explosion_anim['player'].append(img)
powerup_images = {}
powerup_images['shield'] = pygame.image.load(path.join(img_dir, 'energyflower.png')).convert()
powerup_images['shield_gold'] = pygame.image.load(path.join(img_dir, 'goldflower.png')).convert()
powerup_images['gun'] = pygame.image.load(path.join(img_dir, 'MushroomMarioKart8_small1.png')).convert()
powerup_images['minimush'] = pygame.image.load(path.join(img_dir, 'MushroomMarioKart8_small2.png')).convert()
powerup_images['bigmush'] = pygame.image.load(path.join(img_dir, 'MushroomMarioKart8_big2.png')).convert()
powerup_images['goldmush'] = pygame.image.load(path.join(img_dir, 'MushroomMarioKart8_big1.png')).convert()

# Load all game sounds
jump_sound = pygame.mixer.Sound(path.join(snd_dir, 'smb_jump.wav'))
shoot_sound = pygame.mixer.Sound(path.join(snd_dir, 'smb_fireball.wav'))
shield_sound = pygame.mixer.Sound(path.join(snd_dir, 'smb_powerup.wav'))
power_sound = pygame.mixer.Sound(path.join(snd_dir, 'smb_powerup_appears.wav'))
expl_sounds = []
for snd in ['smb_coin.wav', 'smb_bump.wav']:
    expl_sounds.append(pygame.mixer.Sound(path.join(snd_dir, snd)))
player_die_sound = pygame.mixer.Sound(path.join(snd_dir, 'smb_mariodie.wav'))
player_finaldie_sound = pygame.mixer.Sound(path.join(snd_dir, 'smb_gameover.wav'))
player_powerdown_sound = pygame.mixer.Sound(path.join(snd_dir, 'smb_pipe.wav'))


pygame.mixer.music.load(path.join(snd_dir, 'super_mario_medley.mp3'))
pygame.mixer.music.set_volume(0.4)

pygame.mixer.music.play(loops=-1)
special_mob_timer = pygame.time.get_ticks()
ground_mobs_count = 2  # Start with 1 ground mobs
time_no_groundmobs = 0

# Game loop
game_over = True
bowser_appear = False
running = True
while running:
    if game_over:
        show_go_screen()
        game_over = False
        character = character_selection()
        player_img = pygame.image.load(path.join(img_dir, f'{character}.png')).convert()
        player_img = pygame.transform.scale(player_img, (40, 40))
        player_mini_img = pygame.transform.scale(player_img, (40, 40))
        player_mini_img.set_colorkey(BLACK)
        all_sprites = pygame.sprite.Group()
        flymobs = pygame.sprite.Group()
        groundmobs = pygame.sprite.Group()
        staymobs = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        bossbullets = pygame.sprite.Group()
        explosions = pygame.sprite.Group()

        platform1 = Platform(120, HEIGHT - 100, platform1_image)
        platform2 = Platform(360, HEIGHT - 100, platform2_image)
        all_sprites.add(platform1)
        all_sprites.add(platform2)

        powerups = pygame.sprite.Group()
        player = Player(character, bullet_images[character])
        all_sprites.add(player)
        player_group = pygame.sprite.Group()
        for i in range(6):
            newflymob()
        for i in range(ground_mobs_count):  
            newgroundmob()
        stay_mobs_count = random.randint(1, 2)  # Choose a random number of stay mobs to spawn
        for i in range(stay_mobs_count):
            newstaymob() 
        score = 0
        frame_since_last_ground_mob = 0
    if len(groundmobs) == 0:
        # If time_no_groundmobs is not set, set it to the current time
        if time_no_groundmobs == 0:
            time_no_groundmobs = pygame.time.get_ticks()
        # If more than 20 seconds have passed since the ground mobs became zero
        elif pygame.time.get_ticks() - time_no_groundmobs >= 20000:  # 20000 milliseconds is 20 seconds
            newgroundmob()
            ground_mobs_count += 1
            # Reset the time_no_groundmobs variable
            time_no_groundmobs = 0
    elif len(groundmobs) > 1:
        groundmob = groundmobs.sprites()[0]  # get a reference to one of the ground mobs
        groundmob.kill()  # remove it
        ground_mobs_count -= 1
    # keep loop running at the right speed
    clock.tick(FPS)

    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False

    # Update
    all_sprites.update()

    # check to see if a bullet hit a mob
    hits = pygame.sprite.groupcollide(flymobs, bullets, True, True)
    for hit in hits:
        score += 50 - hit.radius
        random.choice(expl_sounds).play()
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        if random.random() > 0.9:
            pow = Pow(hit.rect.center)
            all_sprites.add(pow)
            powerups.add(pow)
        newflymob()

    # check to see if a mob hit the player
    hits = pygame.sprite.spritecollide(player, flymobs, True, pygame.sprite.collide_circle)
    for hit in hits:
        player_powerdown_sound.play()
        player.shield -= hit.radius * 2
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
        newflymob()
        if player.shield <= 0:
            if player.lives > 1:
                player_die_sound.play()
            else: 
                player_finaldie_sound.play()
            death_explosion = Explosion(player.rect.center, 'player')
            all_sprites.add(death_explosion)
            player.hide()
            player.lives -= 1
            player.shield = 100
    
    # Check to see if a bullet hit a ground mob
    ground_hits = pygame.sprite.groupcollide(groundmobs, bullets, True, True)
    for hit in ground_hits:
        score += 50 - hit.radius
        random.choice(expl_sounds).play()
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        if random.random() > 0.9:
            pow = Pow(hit.rect.center)
            all_sprites.add(pow)
            powerups.add(pow)
        newgroundmob()

    # Check to see if a ground mob hit the player
    ground_hits = pygame.sprite.spritecollide(player, groundmobs, True, pygame.sprite.collide_circle)
    for hit in ground_hits:
        player_powerdown_sound.play()
        player.shield -= hit.radius * 2
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
        newgroundmob()
        if player.shield <= 0:
            if player.lives > 1:
                player_die_sound.play()
            else: 
                player_finaldie_sound.play()
            death_explosion = Explosion(player.rect.center, 'player')
            all_sprites.add(death_explosion)
            player.hide()
            player.lives -= 1
            player.shield = 100

    ground_hits = pygame.sprite.spritecollide(player, staymobs, True, pygame.sprite.collide_circle)
    for hit in ground_hits:
        player_powerdown_sound.play()
        player.shield -= hit.radius * 2
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
        newgroundmob()
        if player.shield <= 0:
            if player.lives > 1:
                player_die_sound.play()
            else: 
                player_finaldie_sound.play()
            death_explosion = Explosion(player.rect.center, 'player')
            all_sprites.add(death_explosion)
            player.hide()
            player.lives -= 1
            player.shield = 100

    # check to see if player hit a powerup
    hits = pygame.sprite.spritecollide(player, powerups, True, pygame.sprite.collide_circle)
    for hit in hits:
        if hit.type == 'shield':
            player.shield += random.randrange(5, 20)
            shield_sound.play()
            if player.shield >= 100:
                player.shield = 100
        if hit.type == 'shield_gold':
            player.shield += random.randrange(10, 40)  # Here, we are adding 2x more than the normal shield
            if player.shield >= 100:
                player.shield = 100
            shield_sound.play()
        if hit.type == 'gun':
            player.powerup()
            power_sound.play()
            
    if player.lives == 0 and not death_explosion.alive():
        game_over = True

    if not bowser_appear and score >= 1000:
        score = 0
    # remove all the current mobs
        for sprite in all_sprites:
            if sprite in flymobs or sprite in groundmobs or sprite in staymobs:
                sprite.kill()

    # spawn the boss mob
        bowser = Bowser()
        all_sprites.add(bowser)
        bossbullets = bossBullet(bowser.rect.centerx, bowser.rect.bottom, boss_bullet_image, speedx=0, speedy=10)
        all_sprites.add(bossbullets)
        bossbullets = pygame.sprite.Group()
        bowser_group = pygame.sprite.Group(bowser)
        all_sprites.update()
        bowser_appear = True

    if bowser_appear:
        #bowser_appear = False
    # check to see if a bullet hit the boss
        all_sprites.remove(platform1)
        all_sprites.remove(platform2)
        platform1.kill()
        platform2.kill()
        hits = pygame.sprite.groupcollide(bowser_group, bullets, False, True)
        for hit in hits:
            bowser.shield -= 10
            random.choice(expl_sounds).play()
            expl = Explosion(bowser.rect.center, 'lg')
            all_sprites.add(expl)
            
            if bowser.shield <= 0:  # if boss is dead
                bowser.kill()
                game_over = True  # finish the game

        # check to see if a bullet hit the player
        hits = pygame.sprite.spritecollide(player, bossbullets, True, pygame.sprite.collide_circle)
        for hit in hits:
            player_powerdown_sound.play()
            player.shield -= 10 
            expl = Explosion(hit.rect.center, 'sm')
            all_sprites.add(expl)
            if player.shield <= 0:
                if player.lives > 1:
                    player_die_sound.play()
                else: 
                    player_finaldie_sound.play()
                death_explosion = Explosion(player.rect.center, 'player')
                all_sprites.add(death_explosion)
                player.hide()
                player.lives -= 1
                player.shield = 100
            if player.lives == 0:
                game_over = True

    # Draw / render
    if bowser_appear:
        screen.fill(BLACK)
        screen.blit(bossbackground, background_rect)
        all_sprites.draw(screen)
        draw_shield_bar(screen, 5, 5, player.shield)
        draw_lives(screen, WIDTH - 100, 5, player.lives, player_mini_img)
        draw_boss_shield_bar(screen, WIDTH / 2 - 50, 5, bowser.shield)  # draw the boss's life bar
    
    else:
        screen.fill(BLACK)
        screen.blit(background, background_rect)
        all_sprites.draw(screen)
        draw_score(screen, str(score), 18, WIDTH / 2, 10)
        draw_shield_bar(screen, 5, 5, player.shield)
        draw_lives(screen, WIDTH - 100, 5, player.lives, player_mini_img)
    
    pygame.display.flip()

pygame.quit()