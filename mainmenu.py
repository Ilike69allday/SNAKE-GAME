import pygame
import sys

pygame.init()

SW, SH = 750,750
FPS = 60
FONT_SIZE = 40
BIG_FONT_SIZE = 60

screen = pygame.display.set_mode((SW,SH))
pygame.display.set_caption("Main Menu")
clock = pygame.time.Clock()

big_font = pygame.font.Font(None, BIG_FONT_SIZE)
font = pygame.font.Font(None, FONT_SIZE)

options = ["Option 1", "Option 2", "Option 3", "Option 4", "Option 5", "Quit"]
selected_option = 0

def draw_menu():
    screen.fill("black")

    title_text = big_font.render("SUPER SNAKE", True, "green" )
    title_rect = title_text.get_rect(center=(SW // 2, SH // 8))
    screen.blit(title_text, title_rect)

    for i in range(len(options)):
         option = options[i]
         text = font.render(option, True, "white")
         text_rect = text.get_rect(center=(SW // 2, SH // 4 + i * FONT_SIZE))
         screen.blit(text, text_rect)

         if i == selected_option:
             pygame.draw.rect(screen, "white", text_rect, 2)

    start_text = font.render("PRESS ENTER TO START", True, "white")
    start_rect = start_text.get_rect(center=(SW // 2, SH // 4 + (len(options) + 3) * FONT_SIZE))
    screen.blit(start_text, start_rect)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                selected_option = (selected_option - 1) % len(options)
            elif event.key == pygame.K_DOWN:
                selected_option = (selected_option + 1) % len(options)
            elif event.key == pygame.K_RETURN:
                if selected_option == len(options) - 1:
                    pygame.quit()
                    sys.exit()
                else:
                    print(f"Selected: {options[selected_option]}")

    draw_menu()
    pygame.display.update()
    clock.tick(8)