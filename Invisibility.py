import pygame
import sys
import random
import os

current_directory = os.getcwd()
print(current_directory)

pygame.init()

SW, SH = 750, 750
BLOCK_SIZE = 25 
FONT = pygame.font.Font((current_directory + "\\font.ttf"), BLOCK_SIZE*2)

screen = pygame.display.set_mode((SW, SH))
pygame.display.set_caption("Super Snake!")
clock = pygame.time.Clock()

#initialize the variables
score = 0
snake_invisible = False
snake_invisible_start_time = 0
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
        self.snake_invisible = False

    def update(self):
        global apple, score, powerup, clock, snake_invisible, snake_invisible_start_time, eat_power_time

        for square in self.body:
            if self.head.x == square.x and self.head.y == square.y:
                self.dead = True
            if self.head.x not in range(0, SW) or self.head.y not in range(0, SH):
                self.dead = True

        #restart the game when the snake is dead and reset the variable
        if self.dead:
            self.x, self.y = BLOCK_SIZE, BLOCK_SIZE
            self.head = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)
            self.body = [pygame.Rect(self.x - BLOCK_SIZE, self.y, BLOCK_SIZE, BLOCK_SIZE)]
            self.xdir = 1
            self.ydir = 0
            self.dead = False
            score = 0
            apple = Apple()
            snake_invisible = False
            eat_power_time = 0

        #increase the length of snake's body
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
        self.spawn_new_powerup() # Initializes power up

    def spawn_new_powerup(self):
        self.x = int(random.randint(0, SW - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
        self.y = int(random.randint(0, SH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
        self.rect = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE) # Positioning randomly on the map

    def draw(self):
        pygame.draw.rect(screen, "yellow", self.rect) # Draw rect out 

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

powerup_timer = pygame.USEREVENT + 1 # Create a custom event. By adding 1 will create new event
powerup_spawn_time = 30000  # which is 30 seconds
pygame.time.set_timer(powerup_timer, powerup_spawn_time) # Trigger every 30 seconds

powerup = None  # Initialize power-up object outside the loop

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
        if event.type == powerup_timer: # If is == new event 
            powerup = Powerup() # Reset powerup
            snake.snake_invisible = False # Invisible skill off
            spawn_time = pygame.time.get_ticks() # Keep track time when spawned

    snake.update()

    screen.fill("black")
    drawGrid()
    
    apple.update()

    if powerup:
        powerup.draw() # If launch powerup, draw out yellow block

    score_text = FONT.render(f"{score}", True, "white")

    if not snake.snake_invisible: # If invisiblie is False, will be green colour on snake head
        pygame.draw.rect(screen, "green", snake.head)

    for square in snake.body:
        if not snake.snake_invisible: # If invisible is False also, body will be green and visible
            pygame.draw.rect(screen, "green", square)

    screen.blit(score_text, score_rect)

    if snake.head.x == apple.x and snake.head.y == apple.y:
        snake.body.append(pygame.Rect(square.x, square.y, BLOCK_SIZE, BLOCK_SIZE))
        apple = Apple()
        score += 1

    if pygame.time.get_ticks() - eat_power_time > 10000: # If time minus 0 is bigger than 10 secs, invisible is False
        snake.snake_invisible = False
    
    if pygame.time.get_ticks() - spawn_time > 10000: # If time > 10secs, screen will have no powerup 
        powerup = None

    if powerup and snake.head.colliderect(powerup.rect):  # Check for collision with power-up
        powerup = None # Powerup disappear after snake eat
        snake.snake_invisible = True # Invisible is True
        eat_power_time = pygame.time.get_ticks() # Track time for invisible 
        score += 3 # Score add 3 after snake eats

    pygame.display.update()
    clock.tick(8)
