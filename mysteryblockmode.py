import pygame
import sys
import random
import os

current_directory = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
print(current_directory)

pygame.init()

#set up the screen size, block size and font
SW, SH = 750, 750
BLOCK_SIZE = 25
FONT = pygame.font.Font((current_directory + "\\font.ttf"), BLOCK_SIZE*2)

screen = pygame.display.set_mode((SW, SH))
pygame.display.set_caption("Mystery Block - Super Snake!")
clock = pygame.time.Clock()

#initialize the variables
score = 0
high_score=0
snake_speed_up = False
snake_slow_down = False
snake_score_double = False
snake_invisible = False
snake_power_up_start_time = 0
eat_power_time = 0
spawn_time = 0

try:
    with open('hs_mystery.txt', 'r') as file:   # Open file and r is for reading mode
        content = file.read().strip()   # Read the content and removing the trailing space
        if content:  # Check for content
            high_score = int(content)   # Convert content into highscore (int)
except (FileNotFoundError, ValueError): # File cannot be found, if content cannot be convert into int
    pass

class Snake:
    def __init__(self):
        #initialize the snake's body and position
        self.x, self.y = BLOCK_SIZE, BLOCK_SIZE
        self.xdir = 1
        self.ydir = 0
        self.head = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)
        self.body = [pygame.Rect(self.x - BLOCK_SIZE, self.y, BLOCK_SIZE, BLOCK_SIZE)]
        self.dead = False
        self.snake_speed_up = False
        self.snake_slow_down = False
        self.snake_score_double = False
        self.snake_invisible = False

    def update(self):
        global high_score, apple, score, powerup, clock, snake_speed_up, snake_slow_down, snake_score_double, snake_invisible, snake_power_up_start_time, eat_power_time

        for square in self.body:
            if self.head.x == square.x and self.head.y == square.y:
                self.dead = True
            if self.head.x not in range(0, SW) or self.head.y not in range(0, SH):
                self.dead = True
        
        #update the high score
        if score > high_score:
            high_score = score

        #restart the game when the snake is dead and reset the variable
        if self.dead:
            pygame.time.delay(2000)
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
            snake_invisible = False
            eat_power_time = 0

        #increase the length of snake's body
        self.body.append(self.head)
        for i in range(len(self.body) - 1):
            self.body[i].x, self.body[i].y = self.body[i + 1].x, self.body[i + 1].y
        self.head.x += self.xdir * BLOCK_SIZE
        self.head.y += self.ydir * BLOCK_SIZE
        self.body.remove(self.head)

#generate an apple at random position
class Apple:
    def __init__(self):
        self.x = int(random.randint(0, SW - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
        self.y = int(random.randint(0, SH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
        self.rect = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)

    def update(self):
        pygame.draw.rect(screen, "red", self.rect)

#generate a powerup at random position
class Powerup:
    def __init__(self):
        self.spawn_new_powerup()

    def spawn_new_powerup(self):
        self.x = int(random.randint(0, SW - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
        self.y = int(random.randint(0, SH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
        self.rect = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)

    def draw(self):
        pygame.draw.rect(screen, "yellow", self.rect)

#Draw the grid on the screen
def drawGrid():
    for x in range(0, SW, BLOCK_SIZE):
        for y in range(0, SH, BLOCK_SIZE):
            rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(screen, "#3c3c3b", rect, 1)

#making the score texts and position it
score_text = FONT.render("1", True, "white")
score_rect = score_text.get_rect(center=(SW / 2.05, SH / 20))

drawGrid()

snake = Snake()

apple = Apple()

powerup_timer = pygame.USEREVENT + 1
powerup_spawn_time = 30000  # a new powerup spawn in every 30 seconds
pygame.time.set_timer(powerup_timer, powerup_spawn_time)

powerup = None  # Initialize power-up object outside the loop

snake_speed = 8 #Initial snake speed

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        #change the direction of snake by using keyboard
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
            powerup_types = ["speed_up", "slow_down", "score_double", "invisibility"]
            selected_powerup = random.choice(powerup_types)

            # Spawn the selected power-up
            powerup = Powerup()

            # Set the snake state based on the selected power-up type
            snake.snake_speed_up = selected_powerup == "speed_up"
            snake.snake_slow_down = selected_powerup == "slow_down"
            snake.snake_score_double = selected_powerup == "score_double"
            snake.snake_invisible = selected_powerup == "invisibility"
            snake.snake_invisible = False
            spawn_time = pygame.time.get_ticks()

    snake.update()

    screen.fill("black")
    drawGrid()

    apple.update()

    if powerup:
        powerup.draw()

    score_text = FONT.render(f"{score}", True, "white")
    high_score_text = FONT.render(f"High Score: {high_score}", True, "white")

    # If invisible is False, will be green colour on snake head
    if not snake.snake_invisible:
        pygame.draw.rect(screen, "green", snake.head)

    # If invisible is False also, body will be green and visible
    for square in snake.body:
        if not snake.snake_invisible:
            pygame.draw.rect(screen, "green", square)

    #Display the score
    screen.blit(score_text, score_rect)
    screen.blit(high_score_text, (10, 10))

    #check if the snake eat the apple or not
    if snake.head.x == apple.x and snake.head.y == apple.y:
        #Check to see if the score double power-up is active or not
        if snake.snake_score_double == True:
            snake.body.append(pygame.Rect(square.x, square.y, BLOCK_SIZE, BLOCK_SIZE))
            apple = Apple()
            score += 2
        else:
            snake.body.append(pygame.Rect(square.x, square.y, BLOCK_SIZE, BLOCK_SIZE))
            apple = Apple()
            score += 1

    #after 10 second the snake affected by the powerup, all of the power-ups will be deactivated
    if pygame.time.get_ticks() - eat_power_time > 10000:
        snake.snake_slow_down = False
        snake.snake_speed_up = False
        snake.snake_score_double = False
        snake.snake_invisible = False
        snake_speed = 8
    
    #let the powerup only appear on screen for 10 second and it will be removed
    if pygame.time.get_ticks() - spawn_time > 10000:
        powerup = None

    # Check for collision with power-up
    if powerup and snake.head.colliderect(powerup.rect):
        powerup = None
        #Check to see which power-up to activate
        if selected_powerup == "speed_up":
            snake.snake_speed_up = True
            snake_speed = 30
        elif selected_powerup == "slow_down":
            snake.snake_slow_down = True
            snake_speed = 4
        elif selected_powerup == "score_double":
            snake.snake_score_double = True
        elif selected_powerup == "invisibility":
            snake.snake_invisible = True
        eat_power_time = pygame.time.get_ticks()
        score += 3

    with open('hs_mystery.txt', 'w') as file:   # Open file in write mode
        file.write(str(high_score)) # Must be Str due to in write mode. Convert highscore into str and update file

    pygame.display.update()
    clock.tick(snake_speed)
