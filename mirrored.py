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

class Snake1:
    def __init__(self):
        self.x ,self.y = SW//2, SH//2 - BLOCK_SIZE
        self.xdir = 1
        self.ydir = 0
        self.head = pygame.Rect(self.x,self.y, BLOCK_SIZE,BLOCK_SIZE)
        self.body = [pygame.Rect(self.x-BLOCK_SIZE,self.y, BLOCK_SIZE,BLOCK_SIZE)]
        self.dead = False 

    def update(self, other_snake):
        global apple, score

        for square in self.body:
            if self.head.x == square.x and self.head.y == square.y:
                self.dead = True
                other_snake.dead = True
            if self.head.x not in range(0, SW) or self.head.y not in range(0, SH):
                self.dead = True
                other_snake.dead = True

        if self.dead:
            self.x, self.y = SW//2, SH//2 - BLOCK_SIZE
            self.head = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)
            self.body = [pygame.Rect(self.x-BLOCK_SIZE, self.y, BLOCK_SIZE, BLOCK_SIZE)]
            self.xdir = 1
            self.ydir = 0
            self.dead = False
            score = 0
            apple = Apple()

        self.body.append(self.head)
        for i in range(len(self.body)-1):
            self.body[i].x, self.body[i].y = self.body[i+1].x , self.body[i+1].y
        self.head.x += self.xdir * BLOCK_SIZE
        self.head.y += self.ydir * BLOCK_SIZE
        self.body.remove(self.head)

        # Check collision with the other snake
        for square in other_snake.body:
            if self.head.x == square.x and self.head.y == square.y:
                self.dead = True
                other_snake.dead = True

class Snake2:
    def __init__(self):
        self.x ,self.y = SW//2 , SH//2
        self.xdir = -1
        self.ydir = 0
        self.head = pygame.Rect(self.x,self.y, BLOCK_SIZE,BLOCK_SIZE)
        self.body = [pygame.Rect(self.x-BLOCK_SIZE,self.y, BLOCK_SIZE,BLOCK_SIZE)]
        self.dead = False 

    def update(self, other_snake):
        global apple, score

        for square in self.body:
            if self.head.x == square.x and self.head.y == square.y:
                self.dead = True
                other_snake.dead = True
            if self.head.x not in range(0, SW) or self.head.y not in range(0, SH):
                self.dead = True
                other_snake.dead = True

        if self.dead:
            self.x, self.y = SW//2 , SH//2
            self.head = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)
            self.body = [pygame.Rect(self.x-BLOCK_SIZE, self.y, BLOCK_SIZE, BLOCK_SIZE)]
            self.xdir = -1
            self.ydir = 0
            self.dead = False
            score = 0
            apple = Apple()

        self.body.append(self.head)
        for i in range(len(self.body)-1):
            self.body[i].x, self.body[i].y = self.body[i+1].x , self.body[i+1].y
        self.head.x += self.xdir * BLOCK_SIZE
        self.head.y += self.ydir * BLOCK_SIZE
        self.body.remove(self.head)

        # Check collision with the other snake
        for square in other_snake.body:
            if self.head.x == square.x and self.head.y == square.y:
                self.dead = True
                other_snake.dead = True

class Apple:
    def __init__(self):
        self.x = int(random.randint(0, SW) / BLOCK_SIZE) * BLOCK_SIZE
        self.y = int(random.randint(0, SH) / BLOCK_SIZE) * BLOCK_SIZE
        self.rect = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)

    def update(self):
        pygame.draw.rect(screen, "red", self.rect)

def drawGrid():
    for x in range(0, SW, BLOCK_SIZE):
        for y in range(0, SH, BLOCK_SIZE):
            rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(screen, "#3c3c3b", rect, 1)

score_text = FONT.render("1", True, "white")
score_rect = score_text.get_rect(center=(SW/2.05, SH/20))

drawGrid()

snake1 = Snake1()
snake2 = Snake2()

apple = Apple()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            # Controls for both of the snakes
            if event.key == pygame.K_DOWN:
                snake1.ydir, snake1.xdir = 1, 0
                snake2.ydir, snake2.xdir = -1, 0
            elif event.key == pygame.K_UP:
                snake1.ydir, snake1.xdir = -1, 0
                snake2.ydir, snake2.xdir = 1, 0
            elif event.key == pygame.K_RIGHT:
                snake1.xdir, snake1.ydir = 1, 0
                snake2.xdir, snake2.ydir = -1, 0
            elif event.key == pygame.K_LEFT:
                snake1.xdir, snake1.ydir = -1, 0
                snake2.xdir, snake2.ydir = 1, 0

    snake1.update(snake2)
    snake2.update(snake1)

    screen.fill("black")
    drawGrid()

    apple.update()

    score_texts = FONT.render(f"{score}", True, "white")


    pygame.draw.rect(screen, "green", snake1.head)
    pygame.draw.rect(screen, "blue", snake2.head)

    for square in snake1.body:
        pygame.draw.rect(screen, "green", square)

    for square in snake2.body:
        pygame.draw.rect(screen, "blue", square)

    screen.blit(score_texts, score_rect)


    # Check if either snake eats the apple
    if snake1.head.x == apple.x and snake1.head.y == apple.y:
        snake1.body.append(pygame.Rect(square.x, square.y, BLOCK_SIZE, BLOCK_SIZE))
        snake2.body.append(pygame.Rect(square.x, square.y, BLOCK_SIZE, BLOCK_SIZE))
        apple = Apple()
        score += 1

    if snake2.head.x == apple.x and snake2.head.y == apple.y:
        snake1.body.append(pygame.Rect(square.x, square.y, BLOCK_SIZE, BLOCK_SIZE))
        snake2.body.append(pygame.Rect(square.x, square.y, BLOCK_SIZE, BLOCK_SIZE))
        apple = Apple()
        score += 1

    pygame.display.update()
    clock.tick(8)
