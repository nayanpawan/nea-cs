import pygame
import sys
from perlin_noise import PerlinNoise
from sprites import *
import random



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
    BG=(0,0,0)
    running=True

    WORLD_SIZE=2
    GRID_SIZE = 60
    CELL_SIZE = WIDTH // GRID_SIZE

    camera_x=0
    camera_y=0

    map=[]


    def generate_dungeon():
        seed=random.randint(0,10000)
        noise1=PerlinNoise(2,seed)
        noise2=PerlinNoise(4,seed)
        noise3=PerlinNoise(8,seed)
        dungeon=[]
        for y in range (GRID_SIZE):
            row=[]
            for x in range (GRID_SIZE):
                tile=noise1((x/GRID_SIZE, y/GRID_SIZE))
                tile+=noise2((x/GRID_SIZE, y/GRID_SIZE))*0.5
                tile+=noise3((x/GRID_SIZE, y/GRID_SIZE))*0.25
                if tile>-0.2 and tile<0.15 or tile>0.45 and tile<0.6:
                    row.append(0)#ground
                elif tile<-0.4:
                    row.append(2)#snow
                elif tile>0.2 and tile<0.45:
                    row.append(3)#water  
                elif tile>0.15 and tile<0.2:
                    row.append(4)  #sand
                elif tile<-0.2 and tile>-0.4 or tile>0.6:
                    row.append(1)#stone   
            dungeon.append(row) 
        return dungeon 

    def generate_world():
        for y in range(WORLD_SIZE):
            row=[]
            for x in range(WORLD_SIZE):
                row.append(generate_dungeon())
            map.append(row) 
        return map    
    
    map=generate_world()

    
    
    def draw_dungeon(map):
        for b in range(WORLD_SIZE):
            for a in range(WORLD_SIZE):
                dungeon=map[a][b]
                for y, row in enumerate(dungeon):
                    for x, cell in enumerate(row):
                        terrain=Block(x,y,cell,CELL_SIZE,a,b,GRID_SIZE)
                        all_terrain_group.add(terrain)
                        all_sprites.add(terrain)

                        if cell==1 or cell==2 :
                            collideable_terrain.add(terrain)


    all_terrain_group = pygame.sprite.Group()
    collideable_terrain=pygame.sprite.Group()
    all_sprites=pygame.sprite.Group()
    
    map=generate_world()
    draw_dungeon(map)

    spawn_x, spawn_y = None, None
    for b in range(WORLD_SIZE):
        for a in range(WORLD_SIZE):
            dungeon=map[a][b]
            for y, row in enumerate(dungeon):
                for x, cell in enumerate(row):
                    if cell == 0:  
                        spawn_x = x * GRID_SIZE
                        spawn_y = y * GRID_SIZE
                        break  
                if spawn_x is not None:
                    break 

    player = Player(spawn_x, spawn_y)
    marine=Enemies('marine',50,100)


    all_sprites.add(player)  
    all_sprites.add(marine)

    def draw_healthbar(SCREEN):
        ratio=player.hp/player.max_hp
        pygame.draw.rect(SCREEN,(0,0,0),(10, 10, 300, 40))
        pygame.draw.rect(SCREEN,(255,0,0),(10, 10, 295, 35))
        pygame.draw.rect(SCREEN,(0,255,0),(10, 10, ratio*295, 35)) 

    def draw_hungerbar(SCREEN):
        ratio=player.stamina/player.max_stamina
        pygame.draw.rect(SCREEN,(0,0,0),(10, 60, 300, 40))
        pygame.draw.rect(SCREEN,(211,211,211),(10, 60, 295, 35))
        pygame.draw.rect(SCREEN,(128,84,47),(10, 60, ratio*295, 35))     



    while running:


        SCREEN.fill(BG)

        if player.hp>0:
            player.health=True
        else:
            player.health=False
        
        if player.health:
            if player.moving_left or player.moving_right or player.moving_up or player.moving_down:
                player.update_action(1)
            elif player.attacking:
                player.update_action(2)
            else:
                player.update_action(0)
        else:
            player.update_action(3)   
      

        player.update_animation() 

        events=pygame.event.get()
        player.movement(events, collideable_terrain,all_terrain_group, CELL_SIZE, GRID_SIZE, WORLD_SIZE) 
        marine.patrol(collideable_terrain, CELL_SIZE, GRID_SIZE, WORLD_SIZE)
        marine.update_animation()
        player.heal()


        camera_x=-player.rect.x+WIDTH//2
        camera_y=-player.rect.y+HEIGHT//2

        for sprite in all_sprites:
            if (sprite != player) and sprite!= marine:
                SCREEN.blit(sprite.image, (sprite.rect.x + camera_x, sprite.rect.y + camera_y))

  
        player.draw(SCREEN,camera_x,camera_y)
        marine.draw(SCREEN, camera_x,camera_y)
        draw_healthbar(SCREEN)
        draw_hungerbar(SCREEN)
        pygame.display.flip()
        clock.tick(FPS)

game()