import pygame
import sys

pygame.init()

from ui_components import Button, Textbox

WIDTH, HEIGHT= 1080, 600
SCREEN=pygame.display.set_mode((WIDTH, HEIGHT))

def main_menu():
    pygame.display.set_caption('Main menu')
    BG=pygame.image.load("one-piece-bg1.jpg").convert_alpha()
    BG = pygame.transform.scale(BG, (WIDTH, HEIGHT))

    ##title##
    title=pygame.image.load('title.png').convert_alpha()
    title_rect=title.get_rect()
    title_rect.midtop = (WIDTH // 2, 10) 

    ##buttons##

    while True:
        SCREEN.blit(BG,(0,0))
        SCREEN.blit(title, title_rect.topleft)

        sign_in_button=Button('signIn.png',(540,200),'hover_signIn.png')
        mouse_pos=pygame.mouse.get_pos()
        sign_in_button.change_image(mouse_pos)
        sign_in_button.update(SCREEN)

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()     

main_menu()        