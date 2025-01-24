import pygame
import sys
from perlin_noise import PerlinNoise
from Player import *
import random
import noise


pygame.init()

from ui_components import Button, Textbox

WIDTH, HEIGHT= 1080, 600
SCREEN=pygame.display.set_mode((WIDTH, HEIGHT))

FPS=60
clock=pygame.time.Clock()



def main_menu():
    pygame.display.set_caption('Main menu')
    BG=pygame.image.load("bgs/main-menu-bg.png").convert_alpha()
    BG = pygame.transform.scale(BG, (WIDTH, HEIGHT))

    ##title##
    title=pygame.image.load('titles/main-title.png').convert_alpha()
    title_rect=title.get_rect()
    title_rect.midtop = (WIDTH // 2, 10) 

    ##buttons##
    sign_in_button=Button('buttons/signIn.png',(540,350),'buttons/hover_signIn.png')
    register_button=Button('buttons/register.png',(540,450),'buttons/register-hover.png')
        

    while True:
        SCREEN.blit(BG,(0,0))
        SCREEN.blit(title, title_rect.topleft)
        mouse_pos=pygame.mouse.get_pos()
        
        for button in [sign_in_button, register_button]:
            button.change_image(mouse_pos)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type==pygame.MOUSEBUTTONDOWN:
                if sign_in_button.check_input(mouse_pos):
                    sign_in_menu()
                elif register_button.check_input(mouse_pos):
                    register_menu()
        pygame.display.update()     

def sign_in_menu():
    pygame.display.set_caption('Sign In')
    SCREEN.fill((0,0,0))
    BG=pygame.image.load("bgs/sign-in-bg.png").convert_alpha()
    BG = pygame.transform.scale(BG, (WIDTH, HEIGHT))

    ##title##
    title=pygame.image.load('titles/sign-in-title.png').convert_alpha()
    title_rect=title.get_rect()
    title_rect.midtop = (WIDTH // 2, 10) 

    username_tag=pygame.image.load('buttons/username-tag.png').convert_alpha()
    username_tag_rect=username_tag.get_rect()
    username_tag_rect.midtop=((WIDTH//2)-150, 250)
    password_tag=pygame.image.load('buttons/password-tag.png').convert_alpha()
    password_tag_rect=password_tag.get_rect()
    password_tag_rect.midtop=((WIDTH//2)-150, 350)

    username_input=Textbox(200, 35, ((WIDTH//2)-50, 275),'Enter Username...')
    password_input=Textbox(200, 35, ((WIDTH//2)-50, 375),'Enter Password...')

    submit_button=Button('buttons/submit-button.png',((WIDTH//2)-20, 525),'buttons/submit-button-hover.png')

    while True:
        mouse_pos=pygame.mouse.get_pos()

        SCREEN.blit(BG,(0,0))
        SCREEN.blit(title, title_rect.topleft)
        
        SCREEN.blit(username_tag, username_tag_rect.topleft)
        SCREEN.blit(password_tag, password_tag_rect.topleft)

        username_input.draw(SCREEN)
        password_input.draw(SCREEN)

        submit_button.change_image(mouse_pos)
        submit_button.update(SCREEN)

        for event in pygame.event.get():
            username_input.handle_text(event)
            password_input.handle_text(event)
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()  
            if event.type==pygame.MOUSEBUTTONDOWN:
                if submit_button.check_input(mouse_pos):
                    username=username_input.get_text()
                    password=password_input.get_text()
                    print(username)
                    print(password)      
        pygame.display.update()        

def register_menu():
    pygame.display.set_caption('Sign In')
    SCREEN.fill((0,0,0))
    BG=pygame.image.load("bgs/sign-in-bg.png").convert_alpha()
    BG = pygame.transform.scale(BG, (WIDTH, HEIGHT))

    ##title##
    title=pygame.image.load('titles/register-title.png').convert_alpha()
    title_rect=title.get_rect()
    title_rect.midtop = (WIDTH // 2, 10) 

    username_tag=pygame.image.load('buttons/username-tag.png').convert_alpha()
    username_tag_rect=username_tag.get_rect()
    username_tag_rect.midtop=((WIDTH//2)-150, 250)
    password_tag=pygame.image.load('buttons/password-tag.png').convert_alpha()
    password_tag_rect=password_tag.get_rect()
    password_tag_rect.midtop=((WIDTH//2)-150, 350)

    username_input=Textbox(200, 35, ((WIDTH//2)-50, 275),'Enter Username...')
    password_input=Textbox(200, 35, ((WIDTH//2)-50, 375),'Enter Password...')

    submit_button=Button('buttons/submit-button.png',((WIDTH//2)-20, 525),'buttons/submit-button-hover.png')

    while True:
        mouse_pos=pygame.mouse.get_pos()

        SCREEN.blit(BG,(0,0))
        SCREEN.blit(title, title_rect.topleft)
        
        SCREEN.blit(username_tag, username_tag_rect.topleft)
        SCREEN.blit(password_tag, password_tag_rect.topleft)

        username_input.draw(SCREEN)
        password_input.draw(SCREEN)

        submit_button.change_image(mouse_pos)
        submit_button.update(SCREEN)

        for event in pygame.event.get():
            username_input.handle_text(event)
            password_input.handle_text(event)
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()  
            if event.type==pygame.MOUSEBUTTONDOWN:
                if submit_button.check_input(mouse_pos):
                    username=username_input.get_text()
                    password=password_input.get_text()
                    print(username)
                    print(password)      
        pygame.display.update()         

def game():
    pygame.display.set_caption('Game')
    BG=(128,128,128)
    running=True
    moving_left=False
    moving_right=False
    moving_up=False
    moving_down=False


    player=Player(500, 300)

    while running:
        SCREEN.fill(BG)
        player.draw(SCREEN) 
        player.movement(moving_left, moving_right, moving_up, moving_down) 
        player.update_animation() 

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_d:
                    moving_right=True
                if event.key==pygame.K_a:
                    moving_left=True
                if event.key==pygame.K_w:
                    moving_up=True
                if event.key==pygame.K_s:
                    moving_down=True
            if event.type==pygame.KEYUP:
                if event.key==pygame.K_d:
                    moving_right=False
                if event.key==pygame.K_a:
                    moving_left=False
                if event.key==pygame.K_w:
                    moving_up=False               
                if event.key==pygame.K_s:
                    moving_down=False    
             

        pygame.display.flip()
        clock.tick(FPS)

game()