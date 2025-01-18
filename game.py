import pygame
import sys
from perlin_noise import PerlinNoise
import random


pygame.init()

from ui_components import Button, Textbox

WIDTH, HEIGHT= 1080, 600
SCREEN=pygame.display.set_mode((WIDTH, HEIGHT))

FPS=60
clock=pygame.time.Clock()

GRID_SIZE = 25
CELL_SIZE = WIDTH // GRID_SIZE

def main_menu():
    pygame.display.set_caption('Main menu')
    BG=pygame.image.load("main-menu-bg.png").convert_alpha()
    BG = pygame.transform.scale(BG, (WIDTH, HEIGHT))

    ##title##
    title=pygame.image.load('main-title.png').convert_alpha()
    title_rect=title.get_rect()
    title_rect.midtop = (WIDTH // 2, 10) 

    ##buttons##
    sign_in_button=Button('signIn.png',(540,350),'hover_signIn.png')
    register_button=Button('register.png',(540,450),'register-hover.png')
        

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
    BG=pygame.image.load("sign-in-bg.png").convert_alpha()
    BG = pygame.transform.scale(BG, (WIDTH, HEIGHT))

    ##title##
    title=pygame.image.load('sign-in-title.png').convert_alpha()
    title_rect=title.get_rect()
    title_rect.midtop = (WIDTH // 2, 10) 

    username_tag=pygame.image.load('username-tag.png').convert_alpha()
    username_tag_rect=username_tag.get_rect()
    username_tag_rect.midtop=((WIDTH//2)-150, 250)
    password_tag=pygame.image.load('password-tag.png').convert_alpha()
    password_tag_rect=password_tag.get_rect()
    password_tag_rect.midtop=((WIDTH//2)-150, 350)

    username_input=Textbox(200, 35, ((WIDTH//2)-50, 275),'Enter Username...')
    password_input=Textbox(200, 35, ((WIDTH//2)-50, 375),'Enter Password...')

    submit_button=Button('submit-button.png',((WIDTH//2)-20, 525),'submit-button-hover.png')

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
    BG=pygame.image.load("sign-in-bg.png").convert_alpha()
    BG = pygame.transform.scale(BG, (WIDTH, HEIGHT))

    ##title##
    title=pygame.image.load('register-title.png').convert_alpha()
    title_rect=title.get_rect()
    title_rect.midtop = (WIDTH // 2, 10) 

    username_tag=pygame.image.load('username-tag.png').convert_alpha()
    username_tag_rect=username_tag.get_rect()
    username_tag_rect.midtop=((WIDTH//2)-150, 250)
    password_tag=pygame.image.load('password-tag.png').convert_alpha()
    password_tag_rect=password_tag.get_rect()
    password_tag_rect.midtop=((WIDTH//2)-150, 350)

    username_input=Textbox(200, 35, ((WIDTH//2)-50, 275),'Enter Username...')
    password_input=Textbox(200, 35, ((WIDTH//2)-50, 375),'Enter Password...')

    submit_button=Button('submit-button.png',((WIDTH//2)-20, 525),'submit-button-hover.png')

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
    def generate_dungeon():
        seed=random.randint(0,10000)
        noise=PerlinNoise(10,seed)
        dungeon=[]
        for y in range (GRID_SIZE):
            row=[]
            for x in range (GRID_SIZE):
                tile=noise((x/GRID_SIZE, y/GRID_SIZE))
                if tile>-0.05:
                    row.append(0)
                else:
                    row.append(1)    
            dungeon.append(row) 

            

        return dungeon    

    def draw_dungeon(dungeon):
        for y, row in enumerate(dungeon):
            for x, cell in enumerate(row):
                color = (128,128,128) if cell == 1 else (0,0,0)
                rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(SCREEN, color, rect)     

    dungeon=generate_dungeon()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Draw the dungeon
        SCREEN.fill((0, 0, 0))  # Clear the screen
        draw_dungeon(dungeon)

        pygame.display.flip()  # Update the display
        clock.tick(FPS)

    pygame.quit()
    sys.exit()            


#main_menu()
game()        