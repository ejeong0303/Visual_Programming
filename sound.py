import pygame
import os

# 게임 윈도우 크기
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 400

# 색 정의
BLACK = (0, 0, 0)

# Pygame 초기화
pygame.init()

# 윈도우 제목
pygame.display.set_caption("Sound")

# 윈도우 생성
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# 게임 화면 업데이트 속도
clock = pygame.time.Clock()

# assets 경로 설정
current_path = os.path.dirname(__file__)
assets_path = os.path.join(current_path, 'assets')

# 배경 이미지 로드
background_image = pygame.image.load(os.path.join(assets_path, 'equalizer.png'))

# 배경 음악 로드
pygame.mixer.music.load(os.path.join(assets_path, 'bgm.wav'))
pygame.mixer.music.play(-1) # 무한 반복 재생

# 효과음 로드
sound = pygame.mixer.Sound(os.path.join(assets_path, 'sound.wav'))
sound_piano = []
for i in range(24):
    k = i + 1
    name = f"piano/key{k:02}.mp3"
    print(name)
    snd = pygame.mixer.Sound(name)
    sound_piano.append(snd)

# 게임 종료 전까지 반복
done = False

# 게임 반복 구간
while not done:
    # 이벤트 반복 구간
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            #sound.play()    # 효과음 재생
            sound_piano[15].play()

    # 게임 로직 구간

    # 화면 삭제 구간

    # 윈도우 화면 채우기
    screen.fill(BLACK)

    # 화면 그리기 구간
    # 베경 이미지 그리기
    screen.blit(background_image, background_image.get_rect())

    # 화면 업데이트
    pygame.display.flip()

    # 초당 60 프레임으로 업데이트
    clock.tick(60)

# 게임 종료
pygame.quit()