# *********************************************************
# Program: main.py
# Course: PSP0101 PROBLEM SOLVING AND PROGRAM DESIGN
# Class: TL9L
# Year: 2023/24 Trimester 1
# Names: CHEW XIN NING | JONATHAN KHOO WEI XIANG | MEOR HAZIMI BIN MEOR MOHAMMAD FARED
# IDs: 1221109287 | 1221109226 | 1221109249
# Emails: 1221109287@student.mmu.edu.my | 1221109226@student.mmu.edu.my | 1221109249@student.mmu.edu.my
# Phones: 011-5925 3822 | 018-227 3888 | 019-752 1755
# *********************************************************

import pygame
import sys
import importlib


pygame.init()

SW, SH = 750,750
FPS = 60
FONT_SIZE = 40
BIG_FONT_SIZE = 60

screen = pygame.display.set_mode((SW,SH))
pygame.display.set_caption("Main Menu - Super Snake!")
clock = pygame.time.Clock()

big_font = pygame.font.Font("font.ttf", BIG_FONT_SIZE)
font = pygame.font.Font("font.ttf", FONT_SIZE)

options = ["Normal", "Mystery Block", "Teleportation", "Obstacles", "Mirrored", "Dual", "Quit"]
selected_option = 0

def draw_menu():
    screen.fill("black")

    title_text = big_font.render("SUPER SNAKE!", True, "green" )
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
                if selected_option == 0:
                    print("Selected: Normal")
                    import normalmod
                elif selected_option == 1:
                    print("Selected: Mystery Block")
                    import mysteryblockmode
                elif selected_option == 2:
                    print("Selected: Teleportation")
                    import teleportationmod
                elif selected_option == 3:
                    print("Selected: Obstacles")
                    import obstaclesmod
                elif selected_option == 4:
                    print("Selected: Mirrored")
                    import mirrored
                elif selected_option == 5:
                    print("Selected: Dual")
                    import dualmod
                elif selected_option == 6:
                    pygame.quit()
                    sys.exit()

    draw_menu()
    pygame.display.update()
    clock.tick(8)