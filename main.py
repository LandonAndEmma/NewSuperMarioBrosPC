import pygame
import sys
pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()
FPS = 60
SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 400
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('New Super Mario Bros. PC')
icon = pygame.image.load("icon.png")
pygame.display.set_icon(icon)
class Block(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.images = [pygame.image.load(f'Sprites/Mario/Idle/{i}.png').convert_alpha() for i in range(1, 28)]
        self.index = 0
        self.image = pygame.transform.scale(self.images[self.index], (112, 136))
        self.rect = self.image.get_rect(center=(400, 400))
        self.velocity = pygame.math.Vector2(0, 0)
        self.gravity = 0.4
        self.jumping = False
        self.animation_time = 8
        self.current_time = 15
        self.images_right = [pygame.image.load(f'Sprites/Mario/Walking/Right/{i}.png').convert_alpha() for i in range(1, 15)]
        self.images_left = [pygame.image.load(f'Sprites/Mario/Walking/Left/{i}.png').convert_alpha() for i in range(1, 15)]
        self.images_jump = [pygame.image.load('Sprites/Mario/Jumping/Right/1.png').convert_alpha()]
        self.images_jumpL = [pygame.image.load('Sprites/Mario/Jumping/Left/1.png').convert_alpha()]
        self.jump_velocity = -13
        self.is_jumping = False
        self.running = False
        self.running_animation_time = 10
    def update(self):
        self.current_time += 1
        if self.current_time >= self.animation_time and not self.is_jumping:
            self.current_time = 20
            self.index = (self.index + 1) % len(self.images)
            self.image = self.images[self.index]
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.velocity.x = 2.5
            if self.is_jumping:
                self.animate_jump()
            else:
                self.animate_right()
            self.running = True
        elif keys[pygame.K_LEFT]:
            self.velocity.x = -2.5
            if self.is_jumping:
                self.animate_jumpL()
            else:
                self.animate_left()
            self.running = True
        elif self.is_jumping and not self.running:
            self.animate_jump()
        else:
            self.velocity.x = 0
            if not self.is_jumping:
                self.animate_idle()
            self.running = False
        if keys[pygame.K_UP] and not self.is_jumping:
            pygame.mixer.Channel(1).play(pygame.mixer.Sound("Sounds/Jump.wav"))
            self.is_jumping = True
            self.velocity.y = self.jump_velocity
            self.animate_jump()

        if self.rect.bottom >= SCREEN_HEIGHT - ground_height and self.velocity.y >= 0:
            self.velocity.y = 0
            self.rect.bottom = SCREEN_HEIGHT - ground_height
            self.is_jumping = False
        self.velocity.y += self.gravity
        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y
        if not self.is_jumping and self.running:
            if self.velocity.x > 0:
                self.animate_right()
            else:
                self.animate_left()
        border = 694
        if self.rect.left < border:
            self.rect.left = border
        elif self.rect.right > SCREEN_WIDTH - border:
            self.rect.right = SCREEN_WIDTH - border
        self.velocity.y += self.gravity
        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.velocity.y = 0
            self.jumping = False
    def animate_left(self):
        self.current_time += 1
        if self.current_time >= self.animation_time:
            self.current_time = 0
            self.index = (self.index + 1) % len(self.images_left)
            self.image = self.images_left[self.index]
    def animate_right(self):
        self.current_time += 1
        if self.current_time >= self.animation_time:
            self.current_time = 0
            self.index = (self.index + 1) % len(self.images_right)
            self.image = self.images_right[self.index]
    def animate_idle(self):
        self.current_time += 1
        if self.current_time >= self.animation_time:
            self.current_time = 0
            if self.is_jumping:
                self.index = (self.index + 1) % len(self.images)
                self.image = self.images[self.index]
            else:
                self.index = (self.index + 1) % len(self.images)
                self.image = self.images[self.index]
    def animate_jump(self):
        self.current_time += 1
        if self.current_time >= self.animation_time:
            self.current_time = 0
            self.index = (self.index + 1) % len(self.images_jump)
            self.image = self.images_jump[self.index]
    def animate_jumpL(self):
        self.current_time += 1
        if self.current_time >= self.animation_time:
            self.current_time = 0
            self.index = (self.index + 1) % len(self.images_jumpL)
            self.image = self.images_jumpL[self.index]
all_sprites = pygame.sprite.Group()
block = Block()
all_sprites.add(block)
scroll = 0
ground_image = pygame.image.load("Sprites/ground.png").convert_alpha()
ground_width = ground_image.get_width()
ground_height = ground_image.get_height()
bg_images = [pygame.image.load(f"Sprites/plx-{i}.png").convert_alpha() for i in range(1, 4)]
bg_width = bg_images[0].get_width()
def draw_bg():
    for x in range(6):
        for i in bg_images:
            offset = (x * bg_width) - (scroll % bg_width)
            screen.blit(i, (offset, 0))
def draw_ground():
    global lava_rect
    flag_image = pygame.image.load("Sprites/FlagPole.png").convert_alpha()
    flag_width = flag_image.get_width()
    flag_height = flag_image.get_height()
    lava_image = pygame.image.load("Sprites/Lava.png").convert_alpha()
    lava_width = lava_image.get_width()
    lava_height = lava_image.get_height()
    lava_rect = lava_image.get_rect()
    for x in range(5):
        screen.blit(ground_image, ((x * ground_width) - scroll * 2.5, SCREEN_HEIGHT - ground_height))
    for x in range(5, 6):
        screen.blit(lava_image, ((x * lava_width) - scroll * 2.5, SCREEN_HEIGHT - lava_height + 2))
    for x in range(6, 40):
        screen.blit(ground_image, ((x * ground_width) - scroll * 2.5, SCREEN_HEIGHT - ground_height))
    for x in range(25, 26):
        screen.blit(flag_image, ((x * flag_width) - scroll * 2.5, SCREEN_HEIGHT - flag_height - ground_height))
pygame.mixer.music.load("Music/Forest.wav")
pygame.mixer.music.play(-1)
run = True
start_time = pygame.time.get_ticks()
reached_end = False
clear_music_playing = False
while run:
    clock.tick(FPS)
    draw_bg()
    draw_ground()
    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT] and scroll > 0:
        scroll -= 5
    if key[pygame.K_RIGHT] and scroll < 3000:
        scroll += 5
    if scroll >= 3000 and not reached_end:
        reached_end = True
    if reached_end:
        if not clear_music_playing:
            pygame.mixer.music.stop()
            pygame.mixer.Channel(0).play(pygame.mixer.Sound("Music/Course Clear.wav"))
            clear_music_playing = True
        endingimage = pygame.image.load("Sprites/Finish.png").convert_alpha()
        endingimagewidth = endingimage.get_width()
        endingimageheight = endingimage.get_height()
        screen.blit(endingimage, (SCREEN_WIDTH / 2 - endingimagewidth / 2, SCREEN_HEIGHT / 2 - endingimageheight))
        scroll = 3000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            sys.exit()
    all_sprites.update()
    all_sprites.draw(screen)
    pygame.display.update()
