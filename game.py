import pygame
import sys
from perlin_noise import PerlinNoise
from sprites import *
import random
from generation import*



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
    pygame.display.set_caption('Register')
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

    world=[]
    level=1
    global bounty
    bounty=0

    all_terrain_group = pygame.sprite.Group()
    collideable_terrain=pygame.sprite.Group()
    all_sprites=pygame.sprite.Group()
    enemy_group=pygame.sprite.Group()
    attack_group=pygame.sprite.Group()
    
    def next_level():
        nonlocal level, enemy_num, world, all_terrain_group, collideable_terrain, all_sprites, enemy_group, attack_group, player
        for sprite in all_sprites:
            sprite.kill()
        level+=1    
        world=generate_world(world)
        draw_dungeon(world,all_terrain_group,all_sprites,collideable_terrain)

        spawn_x, spawn_y=random_spawn(world)
        player = Player(spawn_x, spawn_y)

        enemy_random_spawn(level,'marine',collideable_terrain,enemy_group,all_sprites)
        if level%10==0:
            boss_random_spawn(level,'morgan',collideable_terrain,enemy_group,all_sprites)
        enemy_num=len(enemy_group)
        all_sprites.add(player) 


    world=generate_world(world)
    draw_dungeon(world,all_terrain_group,all_sprites,collideable_terrain)

    spawn_x, spawn_y=random_spawn(world)
    player = Player(spawn_x, spawn_y)

    enemy_random_spawn(level,'marine',collideable_terrain,enemy_group,all_sprites)

    all_sprites.add(player) 
    enemy_num=len(enemy_group)

    while running:

        SCREEN.fill(BG)

        if player.hp>0:
            player.health=True
        else:
            player.health=False
        
        if player.health:
            if player.moving_left or player.moving_right or player.moving_up or player.moving_down:
                player.update_action(1)
            elif player.can_shoot and player.can_attack():
                player.shoot(attack_group)    
            elif player.attacking:     
                player.update_action(2)
            else:
                player.update_action(0)
        else:
            player.update_action(3)   
            running=False
      

        player.update_animation() 
        for attack in attack_group:
            attack.update(player,enemy_group,attack_group)
        

        events=pygame.event.get()
        player.movement(events, collideable_terrain,all_terrain_group, CELL_SIZE, GRID_SIZE, WORLD_SIZE)
        for enemy in enemy_group: 
            enemy.patrol(collideable_terrain, player,attack_group, CELL_SIZE, GRID_SIZE, WORLD_SIZE)
            if not enemy.health:
                bounty+=100
            enemy.update_animation()
            if not enemy_group:
                enemy_num=0
        player.heal()
        

        camera_x=-player.rect.x+WIDTH//2
        camera_y=-player.rect.y+HEIGHT//2

        for sprite in all_sprites:
            if (sprite != player) and sprite not in enemy_group:
                SCREEN.blit(sprite.image, (sprite.rect.x + camera_x, sprite.rect.y + camera_y))

  
        player.draw(SCREEN,camera_x,camera_y)
        for enemy in enemy_group:
            enemy.draw(SCREEN, camera_x,camera_y)
        for attack in attack_group:
            attack.draw(SCREEN,camera_x,camera_y)    
        draw_healthbar(SCREEN,player)
        draw_hungerbar(SCREEN,player)
        if enemy_num==0:
            font = pygame.font.Font(None, 60) 
            text = font.render(f"Congrats! Level {level} Cleared", True, (255,215,0))
            text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2))
            SCREEN.blit(text, text_rect) 
            pygame.display.flip()
            pygame.time.delay(2000)
            next_level() 
        pygame.display.flip()
        clock.tick(FPS)

game()
print(bounty)
#main_menu()