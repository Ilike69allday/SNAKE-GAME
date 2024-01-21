import pygame
import sys
import random
import time

pygame.init()

SW, SH = 750, 750
BLOCK_SIZE = 25 
FONT = pygame.font.Font("font.ttf", BLOCK_SIZE * 2)

screen = pygame.display.set_mode((SW, SH))
pygame.display.set_caption("Super Snake!")
clock = pygame.time.Clock()
score = 0

class Snake:
    def __init__(self):
        self.x, self.y = BLOCK_SIZE, BLOCK_SIZE
        self.xdir = 1
        self.ydir = 0
        self.head = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)
        self.body = [pygame.Rect(self.x - BLOCK_SIZE, self.y, BLOCK_SIZE, BLOCK_SIZE)]
        self.dead = False 
        self.invisible = False
        self.invisible_duration = 5  # seconds
        self.invisible_counter = 0

    def update(self, powerup_active):
        global apple, score

        for square in self.body:
            if self.head.x == square.x and self.head.y == square.y:
                self.dead = True
            if self.head.x not in range(0, SW) or self.head.y not in range(0, SH):
                self.dead = True

        if self.dead:
            self.x, self.y = BLOCK_SIZE, BLOCK_SIZE
            self.head = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)
            self.body = [pygame.Rect(self.x - BLOCK_SIZE, self.y, BLOCK_SIZE, BLOCK_SIZE)]
            self.xdir = 1
            self.ydir = 0
            self.dead = False
            self.invisible = False
            self.invisible_counter = 0
            score = 0
            apple = Apple()

        self.body.append(self.head)
        for i in range(len(self.body) - 1):
            self.body[i].x, self.body[i].y = self.body[i + 1].x, self.body[i + 1].y
        self.head.x += self.xdir * BLOCK_SIZE
        self.head.y += self.ydir * BLOCK_SIZE
        self.body.remove(self.head)

        self.update_invisibility()

        if powerup_active and self.head.colliderect(powerup.rect):
            self.activate_powerup()
            powerup.reset()

    def update_invisibility(self):
        if self.invisible:
            self.invisible_counter -= 1
            if self.invisible_counter <= 0:
                self.invisible = False

    def activate_powerup(self):
        self.invisible = True
        self.invisible_counter = self.invisible_duration * 8  # Adjust duration based on your tick rate

class Apple:
    def __init__(self):
        self.x = int(random.randint(0, SW) / BLOCK_SIZE) * BLOCK_SIZE
        self.y = int(random.randint(0, SH) / BLOCK_SIZE) * BLOCK_SIZE
        self.rect = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)

    def update(self):
        pygame.draw.rect(screen, "red", self.rect)

class Powerup:
    def __init__(self):
        self.active = False
        self.duration = 10  # seconds
        self.counter = 0
        self.rect = None

    def spawn(self):
        self.active = True
        self.counter = self.duration * 8  # Adjust duration based on your tick rate
        self.rect = pygame.Rect(
            random.randint(0, SW // BLOCK_SIZE - 1) * BLOCK_SIZE,
            random.randint(0, SH // BLOCK_SIZE - 1) * BLOCK_SIZE,
            BLOCK_SIZE,
            BLOCK_SIZE)

    def reset(self):
        self.active = False
        self.counter = 0
        self.rect = None

    def update(self):
        if self.active:
            self.counter -= 1
            if self.counter <= 0:
                self.reset()

powerup = Powerup()

def drawGrid():
    for x in range(0, SW, BLOCK_SIZE):
        for y in range(0, SH, BLOCK_SIZE):
            rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(screen, "#3c3c3b", rect, 1)

score_text = FONT.render("1", True, "white")
score_rect = score_text.get_rect(center=(SW / 2.05, SH / 20))

drawGrid()

snake = Snake()

apple = Apple()

powerup_spawn_time = time.time()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                snake.ydir = 1
                snake.xdir = 0
            elif event.key == pygame.K_UP:
                snake.ydir = -1
                snake.xdir = 0
            elif event.key == pygame.K_RIGHT:
                snake.xdir = 1
                snake.ydir = 0
            elif event.key == pygame.K_LEFT:
                snake.xdir = -1
                snake.ydir = 0

    current_time = time.time()

    if current_time - powerup_spawn_time >= 30 and not powerup.active:
        powerup.spawn()
        powerup_spawn_time = current_time

    snake.update(powerup.active)

    screen.fill("black")
    drawGrid()
    
    apple.update()
    powerup.update()

    if powerup.active:
        pygame.draw.rect(screen, "yellow", powerup.rect)

    score_text = FONT.render(f"{score}", True, "white")

    if not snake.invisible:
        pygame.draw.rect(screen, "green", snake.head)

    for square in snake.body:
        if not snake.invisible:
            pygame.draw.rect(screen, "green", square)

    screen.blit(score_text, score_rect)

    if snake.head.x == apple.x and snake.head.y == apple.y:
        snake.body.append(pygame.Rect(square.x, square.y, BLOCK_SIZE, BLOCK_SIZE))
        apple = Apple()
        score += 1

    pygame.display.update()
    clock.tick(8)
