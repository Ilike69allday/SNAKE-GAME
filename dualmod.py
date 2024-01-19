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

class Snake:
    def __init__(self, x, y, controls):
        self.x, self.y = x, y
        self.xdir, self.ydir = 1, 0
        self.controls = controls
        self.head = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)
        self.body = [pygame.Rect(self.x - BLOCK_SIZE, self.y, BLOCK_SIZE, BLOCK_SIZE)]
        self.dead = False
        

    def update(self, other_snake):
        global apple1, apple2, score

        for square in self.body:
            if self.head.x == square.x and self.head.y == square.y:
                self.dead = True
                other_snake.dead = True
            if self.head.x not in range(0, SW) or self.head.y not in range(0, SH):
                self.dead = True
                other_snake.dead = True

        if self.dead:
            self.x, self.y = BLOCK_SIZE, BLOCK_SIZE
            self.head = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)
            self.body = [pygame.Rect(self.x - BLOCK_SIZE, self.y, BLOCK_SIZE, BLOCK_SIZE)]
            self.xdir, self.ydir = 1, 0
            self.dead = False
            score = 0
            apple1 = Apple1()
            apple2 = Apple2()

        self.body.append(self.head)
        for i in range(len(self.body) - 1):
            self.body[i].x, self.body[i].y = self.body[i + 1].x, self.body[i + 1].y
        self.head.x += self.xdir * BLOCK_SIZE
        self.head.y += self.ydir * BLOCK_SIZE
        self.body.remove(self.head)

        # Check collision with the other snake
        for square in other_snake.body:
            if self.head.x == square.x and self.head.y == square.y:
                self.dead = True
                other_snake.dead = True

class Apple1:
    def __init__(self):
        self.x = int(random.randint(0, SW) / BLOCK_SIZE) * BLOCK_SIZE
        self.y = int(random.randint(0, SH) / BLOCK_SIZE) * BLOCK_SIZE
        self.rect = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)

    def update(self):
        pygame.draw.rect(screen, "red", self.rect)

class Apple2:
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

snake1 = Snake(BLOCK_SIZE, BLOCK_SIZE, 0)
snake2 = Snake(BLOCK_SIZE * 2, BLOCK_SIZE * 2, 1)

apple1 = Apple1()
apple2 = Apple2()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            # Controls for snake 1
            if event.key == pygame.K_DOWN and snake1.controls == 0:
                snake1.ydir, snake1.xdir = 1, 0
            elif event.key == pygame.K_UP and snake1.controls == 0:
                snake1.ydir, snake1.xdir = -1, 0
            elif event.key == pygame.K_RIGHT and snake1.controls == 0:
                snake1.xdir, snake1.ydir = 1, 0
            elif event.key == pygame.K_LEFT and snake1.controls == 0:
                snake1.xdir, snake1.ydir = -1, 0

            # Controls for snake 2
            elif event.key == pygame.K_s and snake2.controls == 1:
                snake2.ydir, snake2.xdir = 1, 0
            elif event.key == pygame.K_w and snake2.controls == 1:
                snake2.ydir, snake2.xdir = -1, 0
            elif event.key == pygame.K_d and snake2.controls == 1:
                snake2.xdir, snake2.ydir = 1, 0
            elif event.key == pygame.K_a and snake2.controls == 1:
                snake2.xdir, snake2.ydir = -1, 0

    snake1.update(snake2)
    snake2.update(snake1)

    screen.fill("black")
    drawGrid()

    apple1.update()
    apple2.update()

    score_texts = FONT.render(f"{score}", True, "white")


    pygame.draw.rect(screen, "green", snake1.head)
    pygame.draw.rect(screen, "blue", snake2.head)

    for square in snake1.body:
        pygame.draw.rect(screen, "green", square)

    for square in snake2.body:
        pygame.draw.rect(screen, "blue", square)

    screen.blit(score_texts, score_rect)


    # Check if either snake eats the apple
    if snake1.head.x == apple1.x and snake1.head.y == apple1.y:
        snake1.body.append(pygame.Rect(square.x, square.y, BLOCK_SIZE, BLOCK_SIZE))
        snake2.body.append(pygame.Rect(square.x, square.y, BLOCK_SIZE, BLOCK_SIZE))
        apple1 = Apple1()
        score += 1

    if snake1.head.x == apple2.x and snake1.head.y == apple2.y:
        snake1.body.append(pygame.Rect(square.x, square.y, BLOCK_SIZE, BLOCK_SIZE))
        snake2.body.append(pygame.Rect(square.x, square.y, BLOCK_SIZE, BLOCK_SIZE))
        apple2 = Apple2()
        score += 1

    if snake2.head.x == apple1.x and snake2.head.y == apple1.y:
        snake1.body.append(pygame.Rect(square.x, square.y, BLOCK_SIZE, BLOCK_SIZE))
        snake2.body.append(pygame.Rect(square.x, square.y, BLOCK_SIZE, BLOCK_SIZE))
        apple1 = Apple1()
        score += 1

    if snake2.head.x == apple2.x and snake2.head.y == apple2.y:
        snake1.body.append(pygame.Rect(square.x, square.y, BLOCK_SIZE, BLOCK_SIZE))
        snake2.body.append(pygame.Rect(square.x, square.y, BLOCK_SIZE, BLOCK_SIZE))
        apple2 = Apple2()
        score += 1

    pygame.display.update()
    clock.tick(8)
