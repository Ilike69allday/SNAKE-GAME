import pygame
import sys
import random

pygame.init()

#set up the screen size, block size and font
SW, SH = 750, 750
BLOCK_SIZE = 25
FONT = pygame.font.Font("font.ttf", BLOCK_SIZE * 2)

screen = pygame.display.set_mode((SW, SH))
pygame.display.set_caption("Super Snake!")
clock = pygame.time.Clock()

#initialize the variables
score = 0
snakeslowdown = False
slowdownstart = 0
eat_power_time = 0
spawn_time = 0

class Snake:
    def __init__(self):
        #initialize the snake's body and position
        self.x, self.y = BLOCK_SIZE, BLOCK_SIZE
        self.xdir = 1
        self.ydir = 0
        self.head = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)
        self.body = [pygame.Rect(self.x - BLOCK_SIZE, self.y, BLOCK_SIZE, BLOCK_SIZE)]
        self.dead = False
        self.snakeslowdown = False  #check if the snake is under the slowdown power up

    def update(self):
        global apple, score, powerup, clock, snakeslowdown, slowdownstart, eat_power_time

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
            clock.tick(8)  #initial speed of snake
            snakeslowdown = False
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
        self.spawn_newpowerup()

    def spawn_newpowerup(self):  #generate a powerup at random position
        self.x = int(random.randint(0, SW - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
        self.y = int(random.randint(0, SH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
        self.rect = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)

    def draw(self):
        pygame.draw.rect(screen, "yellow", self.rect)

#function used to draw the grid on screen
def drawGrid():
    for x in range(0, SW, BLOCK_SIZE):
        for y in range(0, SH, BLOCK_SIZE):
            rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(screen, "#3c3c3b", rect, 1)

#score display
score_text = FONT.render("1", True, "white")
score_rect = score_text.get_rect(center=(SW / 2.05, SH / 20))

drawGrid()
snake = Snake()
apple = Apple()

powerup_timer = pygame.USEREVENT + 1

powerup_spawn_time = 30000  # a new powerup spawn in every 30 seconds

pygame.time.set_timer(powerup_timer, powerup_spawn_time)

powerup = None  # Initialize powerup object outside the loop

snake_update_frequency = 8  #initial snake update frequency

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:  #change the direction of snake by using keyboard
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

            powerup = Powerup()
            snake.snakeslowdown = False
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

    #check if the snake eat the apple or not
    if snake.head.x == apple.x and snake.head.y == apple.y:
        snake.body.append(pygame.Rect(square.x, square.y, BLOCK_SIZE, BLOCK_SIZE))
        apple = Apple()
        score += 1

    #after 10 second the snake affected by the powerup, change back the snake's speed to initial update frequency
    if pygame.time.get_ticks() - eat_power_time > 10000:
        snake.snakeslowdown = False
        snake_update_frequency = 8
    
    #let the powerup only appear on screen for 10 second and it will be removed
    if pygame.time.get_ticks() - spawn_time >10000: 
        powerup = None

    # Check for collision with power-up
    if powerup and snake.head.colliderect(powerup.rect):
        powerup = None
        snake.snakeslowdown = True
        snake_update_frequency = 4  #slow down the speed of snake by changing clock.tick from 8 to 4
        eat_power_time = pygame.time.get_ticks()
        score += 3 

    pygame.display.update()
    clock.tick(snake_update_frequency)