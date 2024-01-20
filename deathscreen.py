import pygame
import sys

pygame.init()

SW, SH = 750, 750
FPS = 60
FONT_SIZE = 40
BIG_FONT_SIZE = 60
GAP_SIZE = 3 * FONT_SIZE  # Gap size in pixels

screen = pygame.display.set_mode((SW, SH))
pygame.display.set_caption("Death Screen")
clock = pygame.time.Clock()

big_font = pygame.font.Font(None, BIG_FONT_SIZE)
font = pygame.font.Font(None, FONT_SIZE)

game_over_text = big_font.render("GAME OVER", True, "red")
game_over_rect = game_over_text.get_rect(center=(SW // 2, SH // 8))

your_score_text = font.render("Your Score: ", True, "white")
your_score_rect = your_score_text.get_rect(center=(SW // 2, SH // 4 + FONT_SIZE))

highest_score_text = font.render("Highest Score: ", True, "white")
highest_score_rect = highest_score_text.get_rect(center=(SW // 2, SH // 4 + FONT_SIZE + GAP_SIZE))

restart_text = font.render("PRESS ENTER TO RESTART", True, "white")
restart_rect = restart_text.get_rect(center=(SW // 2, SH // 4 + 5 * FONT_SIZE + GAP_SIZE))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                print(f"Restarting the game")

    screen.fill("black")
    screen.blit(game_over_text, game_over_rect)
    screen.blit(your_score_text, your_score_rect)
    screen.blit(highest_score_text, highest_score_rect)
    screen.blit(restart_text, restart_rect)

    # Add code to display the actual score value and highest score value

    pygame.display.update()
    clock.tick(8)