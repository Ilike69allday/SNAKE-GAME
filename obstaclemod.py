import pygame
import sys
import random

pygame.init()

SW, SH = 750,750
BLOCK_SIZE = 25 
FONT = pygame.font.Font("font.ttf",BLOCK_SIZE*2)

screen = pygame.display.set_mode ((SW, SH))
pygame.display.set_caption("Super Snake!")
clock = pygame.time.Clock()
score = 0

class Snake:
    def __init__(self):
        self.x ,self.y = BLOCK_SIZE, BLOCK_SIZE
        self.xdir = 1
        self.ydir = 0
        self.head = pygame.Rect(self.x,self.y, BLOCK_SIZE,BLOCK_SIZE)
        self.body = [pygame.Rect(self.x-BLOCK_SIZE,self.y, BLOCK_SIZE,BLOCK_SIZE)]
        self.dead = False 

    def update(self):
        global apple, score, obstacle

        for square in self.body:
            if self.head.x == square.x and self.head.y == square.y:
                self.dead = True
            if self.head.x not in range(0, SW) or self.head.y not in range(0, SH):
                self.dead = True
            for obs in obstacle:
                if self.head.x == obs.x and self.head.y == obs.y:
                    self.dead = True

        if self.dead:
            self.x, self.y = BLOCK_SIZE, BLOCK_SIZE
            self.head = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)
            self.body = [pygame.Rect(self.x-BLOCK_SIZE, self.y, BLOCK_SIZE, BLOCK_SIZE)]
            self.xdir = 1
            self.ydir = 0
            self.dead = False
            score = 0
            apple = Apple()
            obstacle = [Obstacle()]

        self.body.append(self.head)
        for i in range(len(self.body)-1):
            self.body[i].x, self.body[i].y = self.body[i+1].x , self.body[i+1].y
        self.head.x += self.xdir * BLOCK_SIZE
        self.head.y += self.ydir * BLOCK_SIZE
        self.body.remove(self.head)

class Apple:
    def __init__(self):
        self.spawn_new_apple()

    def spawn_new_apple(self):
        self.x = int(random.randint(0, SW)/BLOCK_SIZE) *BLOCK_SIZE
        self.y = int(random.randint(0, SH)/BLOCK_SIZE) *BLOCK_SIZE
        self.rect = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)

    def update(self):
        for obs in obstacle:
            if self.x == obs.x and self.y == obs.y:
                self.spawn_new_apple()
        pygame.draw.rect(screen, "red", self.rect)

        
class Obstacle:
    def __init__(self):
        self.x = int(random.randint(0, SW)/BLOCK_SIZE) *BLOCK_SIZE
        self.y = int(random.randint(0, SH)/BLOCK_SIZE) *BLOCK_SIZE
        self.rect = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)

    def update(self):
        pygame.draw.rect(screen, "white", self.rect)

def drawGrid():
    for x in range (0,SW,BLOCK_SIZE):
        for y in range (0,SH,BLOCK_SIZE):
            rect = pygame.Rect(x,y,BLOCK_SIZE,BLOCK_SIZE)
            pygame.draw.rect(screen,"#3c3c3b",rect, 1)

score_text = FONT.render("1", True, "white")
score_rect = score_text.get_rect(center=(SW/2.05, SH/20))

drawGrid()

snake = Snake()

apple = Apple()

obstacle = [Obstacle()]

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

    snake.update()
    
    screen.fill("black")
    drawGrid()
    
    apple.update()

    for obs in obstacle:
        obs.update()

    score_text = FONT.render(f"{score}", True, "white")

    pygame.draw.rect(screen,"green", snake.head)

    for square in snake.body:
        pygame.draw.rect(screen, "green" , square)

    screen.blit(score_text, score_rect)

    if snake.head.x == apple.x and snake.head.y == apple.y:
        snake.body.append(pygame.Rect(square.x, square.y, BLOCK_SIZE, BLOCK_SIZE))
        apple = Apple()
        score += 1 

        obstacle.append(Obstacle())


    pygame.display.update()
    clock.tick(8)