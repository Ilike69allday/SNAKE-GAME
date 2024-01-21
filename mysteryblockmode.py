import pygame
import sys
import random

pygame.init()

SW, SH = 750, 750
BLOCK_SIZE = 25
FONT = pygame.font.Font("font.ttf", BLOCK_SIZE * 2)

screen = pygame.display.set_mode((SW, SH))
pygame.display.set_caption("Super Snake!")
clock = pygame.time.Clock()
score = 0
snake_speed_up = False
snake_slow_down = False
snake_score_double = False
snake_power_up_start_time = 0
eat_power_time = 0
spawn_time = 0

class Snake:
    def __init__(self):
        self.x, self.y = BLOCK_SIZE, BLOCK_SIZE
        self.xdir = 1
        self.ydir = 0
        self.head = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)
        self.body = [pygame.Rect(self.x - BLOCK_SIZE, self.y, BLOCK_SIZE, BLOCK_SIZE)]
        self.dead = False
        self.snake_speed_up = False
        self.snake_slow_down = False
        self.snake_score_double = False

    def update(self):
        global apple, score, powerup, clock, snake_speed_up, snake_slow_down, snake_score_double, snake_power_up_start_time, eat_power_time

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
            score = 0
            apple = Apple()
            clock.tick(8)
            snake_speed_up = False
            snake_slow_down = False
            snake_score_double = False
            eat_power_time = 0

        self.body.append(self.head)
        for i in range(len(self.body) - 1):
            self.body[i].x, self.body[i].y = self.body[i + 1].x, self.body[i + 1].y
        self.head.x += self.xdir * BLOCK_SIZE
        self.head.y += self.ydir * BLOCK_SIZE
        self.body.remove(self.head)

class Apple:
    def __init__(self):
        self.x = int(random.randint(0, SW) / BLOCK_SIZE) * BLOCK_SIZE
        self.y = int(random.randint(0, SH) / BLOCK_SIZE) * BLOCK_SIZE
        self.rect = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)

    def update(self):
        pygame.draw.rect(screen, "red", self.rect)

class Powerup:
    def __init__(self):
        self.spawn_new_powerup()

    def spawn_new_powerup(self):
        self.x = int(random.randint(0, SW - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
        self.y = int(random.randint(0, SH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
        self.rect = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)

    def draw(self):
        pygame.draw.rect(screen, "yellow", self.rect)

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

powerup_timer = pygame.USEREVENT + 1
powerup_spawn_time = 30000  # spawn one in every 30 seconds
pygame.time.set_timer(powerup_timer, powerup_spawn_time)

powerup = None  # Initialize power-up object outside the loop

snake_update_frequency = 8

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
        if event.type == powerup_timer:
            powerup_types = ["speed_up", "slow_down", "score_double"]
            selected_powerup = random.choice(powerup_types)

            # Spawn the selected power-up
            powerup = Powerup()

            # Set the snake state based on the selected power-up type
            snake.snake_speed_up = selected_powerup == "speed_up"
            snake.snake_slow_down = selected_powerup == "slow_down"
            snake.snake_score_double = selected_powerup == "score_double"
            spawn_time = pygame.time.get_ticks()

    snake.update()

    screen.fill("black")
    drawGrid()

    apple.update()

    if powerup:
        powerup.draw()

    score_text = FONT.render(f"{score}", True, "white")

    pygame.draw.rect(screen, "green", snake.head)

    for square in snake.body:
        pygame.draw.rect(screen, "green", square)

    screen.blit(score_text, score_rect)

    if snake.head.x == apple.x and snake.head.y == apple.y:
        if snake.snake_score_double == True:
            snake.body.append(pygame.Rect(square.x, square.y, BLOCK_SIZE, BLOCK_SIZE))
            apple = Apple()
            score += 2
        else:
            snake.body.append(pygame.Rect(square.x, square.y, BLOCK_SIZE, BLOCK_SIZE))
            apple = Apple()
            score += 1

    if pygame.time.get_ticks() - eat_power_time > 10000:
        snake.snake_slow_down = False
        snake.snake_speed_up = False
        snake.snake_score_double = False
        snake_update_frequency = 8
    
    if pygame.time.get_ticks() - spawn_time > 10000:
        powerup = None

    # Check for collision with power-up
    if powerup and snake.head.colliderect(powerup.rect):
        powerup = None
        if selected_powerup == "speed_up":
            snake.snake_speed_up = True
            snake_update_frequency = 30
        elif selected_powerup == "slow_down":
            snake.snake_slow_down = True
            snake_update_frequency = 4
        elif selected_powerup == "score_double":
            snake.snake_score_double = True
        eat_power_time = pygame.time.get_ticks()
        score += 3

    pygame.display.update()
    clock.tick(snake_update_frequency)
