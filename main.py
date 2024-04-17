import pygame

pygame.init()
pygame.mixer.init()

SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 400
FPS = 60
clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('New Super Mario Bros. PC')
icon = pygame.image.load("icon.png")
pygame.display.set_icon(icon)

class Block(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.images = [pygame.image.load(f'Sprites/Mario/Idle/{i}.png').convert_alpha() for i in range(1, 28)]
        self.images_right = [pygame.image.load(f'Sprites/Mario/Walking/Right/{i}.png').convert_alpha() for i in range(1, 15)]
        self.images_left = [pygame.image.load(f'Sprites/Mario/Walking/Left/{i}.png').convert_alpha() for i in range(1, 15)]
        self.images_jump = [pygame.image.load('Sprites/Mario/Jumping/Right/1.png').convert_alpha()]
        self.images_jumpL = [pygame.image.load('Sprites/Mario/Jumping/Left/1.png').convert_alpha()]
        self.index = 0
        self.image = self.images[self.index]
        self.image = pygame.transform.scale(self.image, (112, 136))
        self.rect = self.image.get_rect(center=(400, 400))
        self.velocity = pygame.math.Vector2(0, 0)
        self.gravity = 0.4
        self.jumping = False
        self.animation_time = 8
        self.current_time = 15
        self.jump_velocity = -13
        self.is_jumping = False
        self.running = False

    def update(self):
        self.current_time += 1
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
        self.rect.left = max(border, min(self.rect.left, SCREEN_WIDTH - border))
        self.rect.bottom = max(0, min(self.rect.bottom, SCREEN_HEIGHT))

    def animate_left(self):
        self.animate(self.images_left)

    def animate_right(self):
        self.animate(self.images_right)

    def animate_idle(self):
        if self.is_jumping:
            self.animate(self.images)
        else:
            self.animate(self.images)

    def animate_jump(self):
        self.animate(self.images_jump)

    def animate_jumpL(self):
        self.animate(self.images_jumpL)

    def animate(self, image_list):
        self.current_time += 1
        if self.current_time >= self.animation_time:
            self.current_time = 0
            self.index = (self.index + 1) % len(image_list)
            self.image = image_list[self.index]

all_sprites = pygame.sprite.Group()
block = Block()
all_sprites.add(block)

scroll = 0
ground_image = pygame.image.load("Sprites/ground.png").convert_alpha()
ground_width = ground_image.get_width()
ground_height = ground_image.get_height()

lava_image = pygame.image.load("Sprites/Lava.png").convert_alpha()
lava_rect = lava_image.get_rect()

bg_images = [pygame.image.load(f"Sprites/plx-{i}.png").convert_alpha() for i in range(1, 4)]
bg_width = bg_images[0].get_width()

def draw_bg():
    for x in range(6):
        for i in bg_images:
            offset = (x * bg_width) - (scroll % bg_width)
            screen.blit(i, (offset, 0))

def draw_ground():
    flag_image = pygame.image.load("Sprites/FlagPole.png").convert_alpha()
    flag_width = flag_image.get_width()
    flag_height = flag_image.get_height()

    for x in range(5):
        screen.blit(ground_image, ((x * ground_width) - scroll * 2.5, SCREEN_HEIGHT - ground_height))

    for x in range(5, 6):
        screen.blit(lava_image, ((x * lava_rect.width) - scroll * 2.5, SCREEN_HEIGHT - lava_rect.height + 2))

    for x in range(6, 40):
        screen.blit(ground_image, ((x * ground_width) - scroll * 2.5, SCREEN_HEIGHT - ground_height))

    for x in range(25, 26):
        screen.blit(flag_image, ((x * flag_width) - scroll * 2.5, SCREEN_HEIGHT - flag_height - ground_height))

def game_over():
    game_over_image = pygame.image.load("Sprites/GameOver.png").convert_alpha()
    screen.blit(game_over_image, (SCREEN_WIDTH / 2 - game_over_image.get_width() / 2, SCREEN_HEIGHT / 2 - game_over_image.get_height() / 2))
    pygame.display.update()
    pygame.time.delay(2000)
    reset_game()

def reset_game():
    block.rect.center = (400, 400)
    all_sprites.add(block)

run = True
reached_end = False
endingimage = pygame.image.load("Sprites/Finish.png").convert_alpha()
endingimagewidth = endingimage.get_width()
endingimageheight = endingimage.get_height()

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

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    if block.rect.colliderect(lava_rect):
        pygame.mixer.Channel(1).play(pygame.mixer.Sound("Music/Lose a Life.wav"))
        game_over()

    if reached_end:
        pygame.mixer.Channel(0).play(pygame.mixer.Sound("Music/Course Clear.wav"))
        reached_end = None

    if reached_end is None:
        screen.blit(endingimage, (SCREEN_WIDTH / 2 - endingimagewidth / 2, SCREEN_HEIGHT / 2 - endingimageheight))
        scroll = 3000

    all_sprites.update()
    all_sprites.draw(screen)
    pygame.display.update()

pygame.quit()