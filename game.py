import pygame
import sys
from perlin_noise import PerlinNoise
from sprites import *
import random
from screen_stuff import*
from sqlite import*


pygame.mixer.init()
pygame.init()


from ui_components import Button, Textbox

WIDTH, HEIGHT= 1080, 600
SCREEN=pygame.display.set_mode((WIDTH, HEIGHT))

FPS=60
clock=pygame.time.Clock()

keybinds=['W','A','S','D','K']
font = pygame.font.Font(None, 36)




def main_menu():

    pygame.display.set_caption('Main menu')
    BG=pygame.image.load("bgs/main-menu-bg.png").convert_alpha()
    BG = pygame.transform.scale(BG, (WIDTH, HEIGHT))

    ##title##
    title=pygame.image.load('titles/main-title.png').convert_alpha()
    title_rect=title.get_rect()
    title_rect.midtop = (WIDTH // 2, 10) 

    ##buttons##
    sign_in_button=Button('buttons/signIn.png',(540,350),\
                          'buttons/hover_signIn.png')
    register_button=Button('buttons/register.png',(540,450),\
                           'buttons/register-hover.png')
        
    while True:
        SCREEN.blit(BG,(0,0))
        SCREEN.blit(title, title_rect.topleft)
        mouse_pos=pygame.mouse.get_pos()
        
        for button in [sign_in_button, register_button]:
            ##drawing buttons##
            button.change_image(mouse_pos)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type==pygame.MOUSEBUTTONDOWN:
                ##checking for button input and#
                #  redirecting to appropirate window##
                if sign_in_button.check_input(mouse_pos):
                    sign_in_menu()
                elif register_button.check_input(mouse_pos):
                    register_menu()
        pygame.display.update()     

def sign_in_menu():
    global  highscores
    global username
    pygame.display.set_caption('Sign In')
    SCREEN.fill((0,0,0))
    BG=pygame.image.load("bgs/sign-in-bg.png").convert_alpha()
    BG = pygame.transform.scale(BG, (WIDTH, HEIGHT))

    ##title##
    title=pygame.image.load('titles/sign-in-title.png').convert_alpha()
    title_rect=title.get_rect()
    title_rect.midtop = (WIDTH // 2, 10) 

    ##all the tags#
    username_tag=pygame.image.load('buttons/username-tag.png').convert_alpha()
    username_tag_rect=username_tag.get_rect()
    username_tag_rect.midtop=((WIDTH//2)-150, 250)
    password_tag=pygame.image.load('buttons/password-tag.png').convert_alpha()
    password_tag_rect=password_tag.get_rect()
    password_tag_rect.midtop=((WIDTH//2)-150, 350)

    ##input oxes to take username and password##
    username_input=Textbox(200, 35, ((WIDTH//2)-50, 275),'Enter Username...')
    password_input=Textbox(200, 35, ((WIDTH//2)-50, 375),'Enter Password...')

    ##buttons##
    submit_button=Button('buttons/submit-button.png',((WIDTH//2)-20, 525),'buttons/submit-button-hover.png')
    home_button=Button('buttons/home.png',(0,0),'buttons/hover_home.png')
    home_button.rect.topleft=(5,0)

    while True:
        mouse_pos=pygame.mouse.get_pos()
        ##drawing everthing to window##
        SCREEN.blit(BG,(0,0))
        SCREEN.blit(title, title_rect.topleft)
        
        SCREEN.blit(username_tag, username_tag_rect.topleft)
        SCREEN.blit(password_tag, password_tag_rect.topleft)

        username_input.draw(SCREEN)
        password_input.draw(SCREEN)

        submit_button.change_image(mouse_pos)
        submit_button.update(SCREEN)

        home_button.change_image(mouse_pos)
        home_button.update(SCREEN)

        for event in pygame.event.get():
            ##get user input##
            username_input.handle_text(event)
            password_input.handle_text(event)
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()  
            if event.type==pygame.MOUSEBUTTONDOWN:
                if submit_button.check_input(mouse_pos):
                    username=username_input.get_text()
                    password=password_input.get_text()
                    open_database()
                    ##valudating if user exists##
                    if check_user_exists(username,password):
                        highscores=get_highscores(username)
                        game_menu()
                    else:
                        result=7
                        ##otherwise appropirate error message shown##
                        error_message(SCREEN,font,result)
                        pygame.time.delay(1000) 
                elif home_button.check_input(mouse_pos):
                    ##ability to go back if accidently pressed on window##
                    main_menu()            
        pygame.display.update()        

def register_menu():
    global  highscores
    global username
    logged_in=False
    pygame.display.set_caption('Register')
    SCREEN.fill((0,0,0))
    BG=pygame.image.load("bgs/sign-in-bg.png").convert_alpha()
    BG = pygame.transform.scale(BG, (WIDTH, HEIGHT))

    ##title##
    title=pygame.image.load('titles/register-title.png').convert_alpha()
    title_rect=title.get_rect()
    title_rect.midtop = (WIDTH // 2, 10) 
    ##all tags##
    username_tag=pygame.image.load('buttons/username-tag.png').convert_alpha()
    username_tag_rect=username_tag.get_rect()
    username_tag_rect.midtop=((WIDTH//2)-150, 250)
    password_tag=pygame.image.load('buttons/password-tag.png').convert_alpha()
    password_tag_rect=password_tag.get_rect()
    password_tag_rect.midtop=((WIDTH//2)-150, 350)
    ##user input ##
    username_input=Textbox(200, 35, ((WIDTH//2)-50, 275),'Enter Username...')
    password_input=Textbox(200, 35, ((WIDTH//2)-50, 375),'Enter Password...')
    #buttons##
    submit_button=Button('buttons/submit-button.png',((WIDTH//2)-20, 525),'buttons/submit-button-hover.png')
    home_button=Button('buttons/home.png',(0,0),'buttons/hover_home.png')
    home_button.rect.topleft=(5,0)

    while not logged_in:
        mouse_pos=pygame.mouse.get_pos()
        ##drawing to screen##
        SCREEN.blit(BG,(0,0))
        SCREEN.blit(title, title_rect.topleft)
        
        SCREEN.blit(username_tag, username_tag_rect.topleft)
        SCREEN.blit(password_tag, password_tag_rect.topleft)

        username_input.draw(SCREEN)
        password_input.draw(SCREEN)

        submit_button.change_image(mouse_pos)
        submit_button.update(SCREEN)

        home_button.change_image(mouse_pos)
        home_button.update(SCREEN)

        for event in pygame.event.get():
            ##getting user data##
            username_input.handle_text(event)
            password_input.handle_text(event)
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()  
            if event.type==pygame.MOUSEBUTTONDOWN:
                if submit_button.check_input(mouse_pos):
                    username=username_input.get_text()
                    password=password_input.get_text()
                    open_database()
                    ##various validations for username and password##
                    ##if conditions not met then appropirate error shown##
                    if username==''or password=='':
                        result=1
                    elif len(username)<5:
                        result=3
                    elif len(password)<5:
                        result=4
                    elif not(any(char.isdigit() for char in password)):
                        result=5
                    elif not(any(char.isupper() for char in password)) or not(any(char.islower() for char in password)):
                        result=6 
                    elif not add_user_details(username,password):
                        result=2
                    else:
                        result=0         
                    if result==0:
                        highscores=get_highscores(username)
                        game_menu()
                    error_message(SCREEN,font,result)
                    pygame.time.delay(1000) 
                elif home_button.check_input(mouse_pos):
                    main_menu()          
        pygame.display.update()         

def game_menu():
    global highscores
    pygame.display.set_caption('Game menu')
    BG=pygame.image.load("bgs/game-menu.png").convert_alpha()
    BG = pygame.transform.scale(BG, (WIDTH, HEIGHT))
    

    ##title##
    title=pygame.image.load('titles/game-menu-bg.png').convert_alpha()
    title_rect=title.get_rect()
    title_rect.midtop = (WIDTH // 2, 5) 
    ##buttons to redirect elsewhere##
    play_button=Button('buttons/play-default.png',(WIDTH//2,300),'buttons/play-hover.png')
    settings_button=Button('buttons/settings-default.png',(WIDTH//2,385),'buttons/settings-hover.png')
    highscores_button=Button('buttons/highscores-default.png',(WIDTH//2,470),'buttons/highscores-hover.png')
    sign_out_button=Button('buttons/sign-out-default.png',(WIDTH//2,555),'buttons/sign-out-hover.png')

    while True:
        SCREEN.blit(BG,(0,0))
        SCREEN.blit(title, title_rect.topleft)
        mouse_pos=pygame.mouse.get_pos()
        ##changing button hovering/default#
        for button in [play_button, settings_button,highscores_button,sign_out_button]:
            button.change_image(mouse_pos)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type==pygame.MOUSEBUTTONDOWN:
                ##redirecting to various windows##
                if play_button.check_input(mouse_pos):
                    game() 
                elif sign_out_button.check_input(mouse_pos):
                    main_menu()
                elif highscores_button.check_input(mouse_pos):
                    leaderboard() 
                elif settings_button.check_input(mouse_pos):
                    settings()             
        pygame.display.update()          

def leaderboard():
    global highscores
    global username
    pygame.display.set_caption('Highscores')
    BG=pygame.image.load("bgs/leaderborad-bg.png").convert_alpha()
    BG = pygame.transform.scale(BG, (WIDTH, HEIGHT))
    #title#
    title=pygame.image.load('titles/highscores-title.png').convert_alpha()
    title_rect=title.get_rect()
    title_rect.midtop = (WIDTH // 2, 0) 

    home_button=Button('buttons/home.png',(0,0),'buttons/hover_home.png')
    home_button.rect.topleft=(5,0)

    highscore_surfaces = []
    highscore_rects = []
    ##preparing to draw all highscores on screen##
    for i in range(5): 
        highscore_surface = font.render(f"{i+1}) ${highscores[i]}", True, (255, 215, 0))
        highscore_rect = highscore_surface.get_rect(topleft=(WIDTH // 4, 220 + i * 40)) 

        highscore_surfaces.append(highscore_surface)
        highscore_rects.append(highscore_rect)


    while True:
        mouse_pos=pygame.mouse.get_pos()
        SCREEN.blit(BG,(0,0))
        SCREEN.blit(title, title_rect.topleft)
        ##drawing highscores on screen##
        for surface, rect in zip(highscore_surfaces, highscore_rects):
            SCREEN.blit(surface, rect)

        home_button.change_image(mouse_pos)
        home_button.update(SCREEN)

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type==pygame.MOUSEBUTTONDOWN:
                if home_button.check_input(mouse_pos):
                    game_menu()    
        pygame.display.update() 

def settings():
    global keybinds
    pygame.display.set_caption('Settings')
    BG=pygame.image.load("bgs/settings-bg.png").convert_alpha()
    BG = pygame.transform.scale(BG, (WIDTH, HEIGHT))
    #titles#
    title=pygame.image.load('titles/settings-title.png').convert_alpha()
    title=pygame.transform.scale(title,(449,162))
    title_rect=title.get_rect()
    title_rect.midtop = (WIDTH // 2, 0) 

    home_button=Button('buttons/home.png',(0,0),'buttons/hover_home.png')
    home_button.rect.topleft=(5,0)
    #all tags to tell user what key bind they are changing##
    up_key_tag=pygame.image.load('buttons/up-key-tag.png').convert_alpha()
    up_key_tag=pygame.transform.scale(up_key_tag,(128,68))
    up_key_tag_rect=up_key_tag.get_rect()
    up_key_tag_rect.midtop=((WIDTH//2)-100, 160)
   
    down_key_tag=pygame.image.load('buttons/down-key-tag.png').convert_alpha()
    down_key_tag=pygame.transform.scale(down_key_tag,(128,68))
    down_key_tag_rect=down_key_tag.get_rect()
    down_key_tag_rect.midtop=((WIDTH//2)-100, 230)
  
    left_key_tag=pygame.image.load('buttons/left-key-tag.png').convert_alpha()
    left_key_tag=pygame.transform.scale(left_key_tag,(128,68))
    left_key_tag_rect=left_key_tag.get_rect()
    left_key_tag_rect.midtop=((WIDTH//2)-100, 300)

    right_key_tag=pygame.image.load('buttons/right-key-tag.png').convert_alpha()
    right_key_tag=pygame.transform.scale(right_key_tag,(128,68))
    right_key_tag_rect=right_key_tag.get_rect()
    right_key_tag_rect.midtop=((WIDTH//2)-100, 370)
    
    attack_key_tag=pygame.image.load('buttons/attack-tag.png').convert_alpha()
    attack_key_tag=pygame.transform.scale(attack_key_tag,(128,68))
    attack_key_tag_rect=attack_key_tag.get_rect()
    attack_key_tag_rect.midtop=((WIDTH//2)-100, 440)
    ##change keybind inputs##
    up_key_input=Textbox(35, 35, ((WIDTH//2), 175),str(keybinds[0]))
    down_key_input=Textbox(35, 35, ((WIDTH//2), 245),str(keybinds[1]))
    left_key_input=Textbox(35, 35, ((WIDTH//2), 315),str(keybinds[2]))
    right_key_input=Textbox(35, 35, ((WIDTH//2), 385),str(keybinds[3]))
    attack_key_input=Textbox(35, 35, ((WIDTH//2), 455),str(keybinds[4]))

    submit_button=Button('buttons/submit-button.png',((WIDTH//2)-40, 560),'buttons/submit-button-hover.png')

    while True:
        mouse_pos=pygame.mouse.get_pos()
        SCREEN.blit(BG,(0,0))
        SCREEN.blit(title, title_rect.topleft)
        #drawing all tags##
        SCREEN.blit(up_key_tag, up_key_tag_rect.topleft)
        SCREEN.blit(down_key_tag, down_key_tag_rect.topleft)
        SCREEN.blit(left_key_tag, left_key_tag_rect.topleft)
        SCREEN.blit(right_key_tag, right_key_tag_rect.topleft)
        SCREEN.blit(attack_key_tag, attack_key_tag_rect.topleft)

        submit_button.change_image(mouse_pos)
        submit_button.update(SCREEN)

        home_button.change_image(mouse_pos)
        home_button.update(SCREEN)
        ##drawing the key user pressed so they know new key bind##
        for input in [up_key_input,down_key_input,left_key_input,right_key_input,attack_key_input]:
            input.draw(SCREEN)

        for event in pygame.event.get():
            if event.type==pygame.MOUSEBUTTONDOWN:
                if home_button.check_input(mouse_pos):
                    game_menu()
                elif submit_button.check_input(mouse_pos):
                    ##converts all to upper so not case sensitive##
                    up_key=(up_key_input.get_text()).upper()
                    down_key=(down_key_input.get_text()).upper()
                    left_key=(left_key_input.get_text()).upper()
                    right_key=(right_key_input.get_text()).upper()
                    down_key=(down_key_input.get_text()).upper()
                    attack_key=(attack_key_input.get_text()).upper()
                    ##checking if 1 key does multiple things if so not allowing##
                    for key in[up_key,down_key,left_key,right_key,attack_key]:
                        if key in keybinds:
                            result=8
                            error_message(SCREEN,font,result)
                            pygame.time.delay(1000) 
                        else:
                            ##changing keybinds list so it can be updated later for player movement##
                            new_keys=[]
                            if up_key=='':
                                new_keys.append(keybinds[0])
                            else:
                                new_keys.append(up_key) 
                            if down_key=='':
                                new_keys.append(keybinds[1])
                            else:
                                new_keys.append(down_key) 
                            if left_key=='':
                                new_keys.append(keybinds[2])
                            else:
                                new_keys.append(left_key) 
                            if right_key=='':
                                new_keys.append(keybinds[3])
                            else:
                                new_keys.append(right_key) 
                            if attack_key=='':
                                new_keys.append(keybinds[4])
                            else:
                                new_keys.append(attack_key)
                            keybinds=new_keys  
                            print(keybinds)                      

            for input in [up_key_input,down_key_input,left_key_input,right_key_input,attack_key_input]:
                input.handle_text(event)
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()        

def game():
    global highscores
    global keybinds
    pygame.display.set_caption('Game')
    BG=(0,0,0)
    running=True
    paused=False
    font = pygame.font.Font(None, 36)
    ##loading game music##
    pygame.mixer.music.load('270.mp3')
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)
    #music state#
    music_pause=False

    ##world dimensions useful for how game is generated##
    WORLD_SIZE=2
    GRID_SIZE = 60
    CELL_SIZE = WIDTH // GRID_SIZE
    ##camera offset initailisation##
    camera_x=0
    camera_y=0

    world=[]
    level=1
    bounty=0

    ##sprite groups used for colliusion checking##
    all_terrain_group = pygame.sprite.Group()
    collideable_terrain=pygame.sprite.Group()
    all_sprites=pygame.sprite.Group()
    enemy_group=pygame.sprite.Group()
    attack_group=pygame.sprite.Group()
    consumable_group=pygame.sprite.Group()


    def next_level():
        ##function that loads levels##
        nonlocal level, enemy_num, world, all_terrain_group, collideable_terrain, all_sprites, enemy_group, attack_group, player
        for sprite in all_sprites:
            sprite.kill()
        level+=1    
        world=generate_world(world,level)
        draw_dungeon(world,all_terrain_group,all_sprites,collideable_terrain,consumable_group)

        spawn_x, spawn_y=random_spawn(world)
        player = Player(spawn_x, spawn_y)
        ##diificulty rises as levels increase##
        enemy_random_spawn(level,'marine',collideable_terrain,enemy_group,all_sprites)
        if level%10==0:##boss spawing every tenth level as requested by client##
            boss_random_spawn(level,'morgan',collideable_terrain,enemy_group,all_sprites)
        enemy_num=len(enemy_group)
        all_sprites.add(player) 

    def pause_game():
        ##paused screen##
        font = pygame.font.Font(None, 60)
        text = font.render("Paused", True, (255, 255, 255))
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
        SCREEN.blit(text, text_rect)

        resume_button=Button('buttons/resume-default.png',(WIDTH//2-100,HEIGHT//2+60),'buttons/resume-hover.png')
        quit_button=Button('buttons/quit-default.png',(WIDTH//2+100,HEIGHT//2+60),'buttons/quit-hover.png')
        mouse_pos=pygame.mouse.get_pos()

        resume_button.change_image(mouse_pos)
        resume_button.update(SCREEN)

        quit_button.change_image(mouse_pos)
        quit_button.update(SCREEN)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()  
            if event.type==pygame.MOUSEBUTTONDOWN:
                ##buttons used to either return to game or quit##
                if resume_button.check_input(mouse_pos):
                    return 'resume'
                elif quit_button.check_input(mouse_pos):
                    return 'quit'

    ##generating level 1##
    world=generate_world(world,level)
    draw_dungeon(world,all_terrain_group,all_sprites,collideable_terrain,consumable_group)

    spawn_x, spawn_y=random_spawn(world)
    player = Player(spawn_x, spawn_y)

    enemy_random_spawn(level,'marine',collideable_terrain,enemy_group,all_sprites)

    all_sprites.add(player) 
    enemy_num=len(enemy_group)

    while running:
        
        SCREEN.fill(BG)
        events=pygame.event.get()
##checking key presses##
        for event in events:
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                paused = True
            elif event.type == pygame.KEYDOWN and event.key==pygame.K_h:
                player.haki_attack(enemy_group, level)  
            elif event.type == pygame.KEYDOWN and event.key==pygame.K_m:
                music_pause=not music_pause
##music pause ability##
        if music_pause:
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()            

        if paused:
            action = pause_game()
            if action=='resume':
                paused=False
            elif action=='quit':
                highscores=sort_score(highscores,bounty)
                update_highscores(username,highscores)
                game_menu()    

        if not paused:
            if player.hp>0:
                player.health=True
            else:
                player.health=False
            
            if player.health:
                ##player animations called##
                if player.moving_left or player.moving_right or player.moving_up or player.moving_down:
                    player.update_action(1)
                elif player.can_shoot and player.can_attack():
                    player.shoot(attack_group)    
                elif player.attacking:     
                    player.update_action(2)
                else:
                    player.update_action(0)
            else:
                ##highscores handled once player dies##
                highscores=sort_score(highscores,bounty)
                update_highscores(username,highscores)
                player.update_action(3)   
                running=False
        

            player.update_animation() 
            for attack in attack_group:
                ##attack animation##
                attack.update(player,enemy_group,attack_group,level)
            
            ##handles player movemnt##
            player.movement(events, collideable_terrain,all_terrain_group, CELL_SIZE, GRID_SIZE, WORLD_SIZE,keybinds)
            for enemy in enemy_group: 
                ##handlind ai movement of enemies##
                enemy.patrol(collideable_terrain, player,attack_group, CELL_SIZE, GRID_SIZE, WORLD_SIZE)
                if not enemy.health:
                    ##score increasing##
                    if enemy.enemy_type=='marine':
                        bounty+=100
                    else:
                        bounty+=1000    
                enemy.update_animation()
                if not enemy_group:
                    enemy_num=0
            player.heal(all_terrain_group,events)
            
##moving camera is implemeted by updating camrea offset depending where the player is##
            camera_x=-player.rect.x+WIDTH//2
            camera_y=-player.rect.y+HEIGHT//2
##all terrain is moved by camera##
            for sprite in all_sprites:
                if (sprite != player) and sprite not in enemy_group:
                    SCREEN.blit(sprite.image, (sprite.rect.x + camera_x, sprite.rect.y + camera_y))

    
            player.draw(SCREEN,camera_x,camera_y)
            for enemy in enemy_group:
                ##enemy moved by camera seperately to allow them to flip##
                enemy.draw(SCREEN, camera_x,camera_y)
            for attack in attack_group:
                attack.draw(SCREEN,camera_x,camera_y)   
                ##drawing health,hunger,cooldown, score and highscore## 
            draw_healthbar(SCREEN,player)
            draw_hungerbar(SCREEN,player)
            draw_score(SCREEN,bounty,font,max(highscores))
            draw_haki_counter(SCREEN,player)
            if enemy_num==0:
                font = pygame.font.Font(None, 36) 
                text = font.render(f"Congrats! Level {level} Cleared", True, (255,215,0))
                text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2))
                SCREEN.blit(text, text_rect) 
                pygame.display.flip()
                pygame.time.delay(2000)
                next_level() 
        pygame.display.flip()
        clock.tick(FPS)

#game()
#print(bounty)
main_menu()
#game_menu()
# highscores=get_highscores('Nayan')
# highscores=sort_score(highscores,100)
#leaderboard()
#settings()