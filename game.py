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
    title_surface = pygame.Surface((1080, 100), pygame.SRCALPHA)
    title_surface.fill((128, 128, 128, 128))

    font = pygame.font.SysFont("arial", 60)  
    title_text = font.render("Main Menu", True, (255, 255, 255))
    title_text_rect = title_text.get_rect(center=(WIDTH//2,50))

    ##buttons##

    sign_in_button=Button()

    while True:
        SCREEN.blit(BG,(0,0))

        SCREEN.blit(title_surface, (0, 0))
        SCREEN.blit(title_text, title_text_rect)

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()     

main_menu()        