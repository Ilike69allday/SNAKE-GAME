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
import os

current_directory = os.getcwd()
print(current_directory)

pygame.init()

SW, SH = 750,750 
FONT_SIZE = 40
BIG_FONT_SIZE = 60

screen = pygame.display.set_mode((SW,SH)) # Screen Display Size same as Others
pygame.display.set_caption("Main Menu - Super Snake!") # Title
clock = pygame.time.Clock()

# Fonts different Sizes
big_font = pygame.font.Font((current_directory + "\\font.ttf"), BIG_FONT_SIZE)
font = pygame.font.Font((current_directory + "\\font.ttf"), FONT_SIZE)

# List for options to choose from
options = ["Normal", "Mystery Block", "Teleportation", "Obstacles", "Mirrored", "Dual", "Quit"]
selected_option = 0

def draw_menu():
    screen.fill("black") # Fills screen with black

    title_text = big_font.render("SUPER SNAKE!", True, "green" ) # Render 
    title_rect = title_text.get_rect(center=(SW // 2, SH // 8)) # Position in the middle, 1/8 of the screen's height
    screen.blit(title_text, title_rect) # Draw text in screen 

    for i in range(len(options)):
         option = options[i] # i refers to option
         text = font.render(option, True, "white") # Render 
         text_rect = text.get_rect(center=(SW // 2, SH // 4 + i * FONT_SIZE)) # Positioning in middle, and vertically space out
         screen.blit(text, text_rect) # Draw text in screen

         if i == selected_option: 
             pygame.draw.rect(screen, "white", text_rect, 2) # Draw rectangle, border pixel is 2

    start_text = font.render("PRESS ENTER TO START", True, "white") # Render
    start_rect = start_text.get_rect(center=(SW // 2, SH // 4 + (len(options) + 3) * FONT_SIZE)) # Positioning below Options
    screen.blit(start_text, start_rect) # Draw text

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # Window Close Button
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            # When KeyUp, For exmepla, selected is 5, when up key the formula will be (5-1)%6, the remainder is 4 == selected option.
            if event.key == pygame.K_UP:
                selected_option = (selected_option - 1) % len(options) 
            # When KeyDown, For exmeple, selected is 2, when down key the formula will be (2+1)%6, the remainder is 3 == selected option.
            elif event.key == pygame.K_DOWN:
                selected_option = (selected_option + 1) % len(options)
            elif event.key == pygame.K_RETURN:
                # If Enter is Clicked, it will trigger based on your selected option, and import to another python file.
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
                    print("Selected: Quit")
                    pygame.quit()
                    sys.exit()

    draw_menu()
    pygame.display.update()
    clock.tick(8)